#!/usr/bin/env python3
"""Deterministic helpers for the `start` and `learn` skills. Python 3.8+, standard library only.

Usage:
  learn_tool.py doctor                       environment and workspace report (safe to run any time)
  learn_tool.py init --lang <tag> --lang-name <name> [--no-git]
                                             create the private workspace my-learning/ with settings.json
  learn_tool.py settings [--lang <tag> --lang-name <name>]
                                             print settings, or change the conversation language
  learn_tool.py new-course <slug> --track <track> --title <title>
                                             create my-learning/<slug>/course.json from the track defaults
  learn_tool.py status [<course>]            one-line summary per course
  learn_tool.py report <course>              full progress report (stages, areas, strong/weak, pace)
  learn_tool.py due <course>                 topics and flashcards due for review today
  learn_tool.py check <course>               validate course.json / program.md / progress.md / timeline.md / cards.md
  learn_tool.py sync <course>                rewrite program.md checkboxes from progress.md
  learn_tool.py session <course> <mode> <slug> [--topics a,b] [--title T] [--ext ts]
                                             create my-learning/<course>/sessions/<date>-<slug>/ with lesson.md
                                             (and practice.<ext> when --ext is given)
  learn_tool.py open [<course>]              list open (unfinished) sessions, newest first
  learn_tool.py exercises <course> [--session NAME] [--file exercises.json]
                                             validate an interactive exercise file and build a static
                                             exercises.html next to it (works offline, no server)
  learn_tool.py serve <course> [--session NAME] [--file exercises.json] [--port 8765] [--no-browser]
                                             serve the exercises on 127.0.0.1 and save answers to results.json

Run from anywhere inside the repository. The repository root is the nearest parent folder that
contains AGENTS.md and .agents/skills/learn (or pass --root). Learner data lives in <root>/my-learning
(override with --data). Output is English on purpose: the agent translates it for the learner.
"""
import argparse
import json
import os
import secrets
import threading
import time
import webbrowser
import re
import shutil
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent          # .agents/skills/learn
TRACKS_DIR = SKILL_DIR / "tracks"
TEMPLATES_DIR = SKILL_DIR / "templates"
INTERACTIVE_DIR = SKILL_DIR / "interactive"
DATA_PLACEHOLDER = "__EXERCISE_DATA__"
ITEM_TYPES = ("choice", "gap", "order", "flashcard")
GAP_RE = re.compile(r"\{\{(\d+)\}\}")
DATA_DIR_NAME = "my-learning"
SCHEMA = 1

STATUSES = ("todo", "learning", "shaky", "solid")
SESSION_MODES = ("study", "practice", "review", "test", "diagnostic")
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
EXT_RE = re.compile(r"^[A-Za-z0-9]+$")
LANG_TAG_RE = re.compile(r"^[A-Za-z]{2,3}(-[A-Za-z0-9]{2,8})*$")   # BCP 47-ish: en, en-US, zh-Hans, es-419
INTERVALS = {0: 14, 1: 30, 2: 90}  # successful reviews so far -> days; 3+ -> 180
CARD_INTERVALS = {1: 1, 2: 3, 3: 7, 4: 21, 5: 60}  # Leitner box -> days until the next review
NOTE_MAX = 80
TOPIC_RE = re.compile(r"^(\s*- \[)([ xX])(\] `)([a-z0-9][a-z0-9.\-]*)(`.*)$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

WORKSPACE_GITIGNORE = """\
# Learning sessions: disposable per-lesson workspaces (lesson.md, practice files, installed dependencies)
/*/sessions/

# Typical build outputs of demo projects
node_modules/
dist/
build/
target/
bin/
obj/
out/
__pycache__/
*.log
.env
.env.*
.DS_Store
Thumbs.db
"""

WORKSPACE_README = """\
# my-learning

Your private learning data: settings, courses, progress, timelines.

- This folder is ignored by the public engine repository, so updating the engine never touches it.
- It is its own small git repository. Every session ends with a commit here, so nothing is lost.
- To back it up or move it to another computer, ask your agent: "back up my progress".
  Use a PRIVATE repository for that: the files describe what you study and how it goes.
"""


# ---------------------------------------------------------------- paths and small helpers

def find_root(start: Path) -> Path:
    for p in [start, *start.parents]:
        if (p / "AGENTS.md").exists() and (p / ".agents" / "skills" / "learn").is_dir():
            return p
    # The script itself lives inside the repository: fall back to its location.
    guess = SKILL_DIR.parent.parent.parent
    if (guess / "AGENTS.md").exists():
        return guess
    sys.exit("error: repository root not found (AGENTS.md + .agents/skills/learn); pass --root")


def parse_date(s: str):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def known_tracks():
    if not TRACKS_DIR.is_dir():
        return []
    return sorted(p.name for p in TRACKS_DIR.iterdir() if (p / "TRACK.md").exists())


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except FileNotFoundError:
        return None, f"{path.name}: missing"
    except json.JSONDecodeError as e:
        return None, f"{path.name}: invalid JSON ({e.msg} at line {e.lineno})"


def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rel(root: Path, p: Path) -> str:
    try:
        return p.relative_to(root).as_posix()
    except ValueError:
        return p.as_posix()


def course_dirs(data: Path):
    if not data.is_dir():
        return []
    return sorted(p for p in data.iterdir() if p.is_dir() and (p / "course.json").exists())


def need_course(data: Path, course: str) -> Path:
    cdir = data / course
    if not (cdir / "course.json").exists():
        names = ", ".join(p.name for p in course_dirs(data)) or "none yet"
        sys.exit(f"error: course '{course}' not found in {DATA_DIR_NAME}/ (existing: {names})")
    return cdir


# ---------------------------------------------------------------- program / progress / cards parsing

def read_program(path: Path):
    """Return list of (line_index, checked, topic_id) and the raw lines."""
    lines = path.read_text(encoding="utf-8").splitlines()
    topics = []
    for i, line in enumerate(lines):
        m = TOPIC_RE.match(line)
        if m:
            topics.append((i, m.group(2).lower() == "x", m.group(4)))
    return topics, lines


def read_table(lines, start_line, columns, label):
    rows, errors = [], []
    for n, line in enumerate(lines, start=start_line):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and cells[0] in (columns[0], "---", "") or set("".join(cells)) <= set("-: "):
            continue
        if len(cells) != len(columns):
            errors.append(f"{label}:{n}: expected {len(columns)} columns, got {len(cells)}")
            continue
        rows.append(dict(zip(columns, cells), line=n))
    return rows, errors


def read_progress(path: Path):
    """Return (header dict, rows list of dicts, errors list)."""
    text = path.read_text(encoding="utf-8").splitlines()
    header = {}
    if not text or text[0].strip() != "---":
        return header, [], ["progress.md: missing '---' header block"]
    end = None
    for i in range(1, len(text)):
        if text[i].strip() == "---":
            end = i
            break
        if ":" in text[i]:
            key, _, value = text[i].partition(":")
            header[key.strip()] = re.split(r"\s+#", value, maxsplit=1)[0].strip()
    if end is None:
        return header, [], ["progress.md: header block is not closed with '---'"]
    rows, errors = read_table(text[end + 1:], end + 2,
                              ("id", "status", "since", "reviewed", "reviews", "note"), "progress.md")
    return header, rows, errors


def read_cards(path: Path):
    if not path.exists():
        return [], []
    return read_table(path.read_text(encoding="utf-8").splitlines(), 1,
                      ("front", "back", "example", "box", "next"), "cards.md")


def load_course(data: Path, course: str):
    cdir = need_course(data, course)
    prog, progress = cdir / "program.md", cdir / "progress.md"
    if not prog.exists() or not progress.exists():
        return cdir, None, None, None, None
    topics, lines = read_program(prog)
    header, rows, errs = read_progress(progress)
    return cdir, (topics, lines), header, rows, errs


def due_date(row):
    base = parse_date(row["reviewed"]) if row["reviewed"] != "-" else None
    base = base or (parse_date(row["since"]) if row["since"] != "-" else None)
    if base is None:
        return None
    try:
        n = int(row["reviews"])
    except ValueError:
        n = 0
    return base + timedelta(days=INTERVALS.get(n, 180))


def counts(rows):
    c = {s: 0 for s in STATUSES}
    for r in rows:
        if r["status"] in c:
            c[r["status"]] += 1
    return c


def is_due(row, today):
    return row["status"] == "solid" and (due_date(row) or today + timedelta(days=1)) <= today


def cards_due(cards, today):
    return [c for c in cards if (parse_date(c["next"]) or today + timedelta(days=1)) <= today]


# ---------------------------------------------------------------- workspace commands

def git_available():
    return shutil.which("git") is not None


def run_git(args, cwd: Path):
    try:
        r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8")
        return r.returncode, (r.stdout or "").strip(), (r.stderr or "").strip()
    except OSError as e:
        return 1, "", str(e)


def cmd_doctor(root, data, a, today):
    print(f"repository root: {root.as_posix()}")
    print(f"python:          {sys.version.split()[0]} ({sys.executable})")
    if git_available():
        _, out, _ = run_git(["--version"], root)
        print(f"git:             {out}")
        code, remote, _ = run_git(["remote", "get-url", "origin"], root)
        print(f"engine remote:   {remote if code == 0 else '-'}")
    else:
        print("git:             NOT FOUND (needed for updates and progress history)")
    print(f"tracks:          {', '.join(known_tracks()) or 'NONE (broken install?)'}")
    if not data.is_dir():
        print(f"workspace:       {DATA_DIR_NAME}/ not created yet -> run the `start` skill")
        return 0
    settings, err = read_json(data / "settings.json")
    if err:
        print(f"workspace:       {DATA_DIR_NAME}/ exists, but {err} -> run the `start` skill")
    else:
        print(f"workspace:       {DATA_DIR_NAME}/ (language: {settings.get('language_name')} "
              f"[{settings.get('language')}], since {settings.get('created')})")
    if git_available():
        if (data / ".git").exists():
            code, remote, _ = run_git(["remote", "get-url", "origin"], data)
            print(f"progress git:    yes, backup remote: {remote if code == 0 else 'none (local only)'}")
        else:
            print("progress git:    no (run: git init inside my-learning)")
    courses = course_dirs(data)
    print(f"courses:         {len(courses)}")
    for c in courses:
        meta, err = read_json(c / "course.json")
        track = meta.get("track", "?") if meta else "?"
        state = "started" if (c / "program.md").exists() else "needs diagnostic"
        print(f"  - {c.name} [{track}] {state}")
    return 0


def validate_language(tag, name):
    if not tag or not LANG_TAG_RE.match(tag):
        sys.exit(f"error: --lang must be a language tag such as en, en-US, ru, es-419, got '{tag}'")
    if not name:
        sys.exit("error: --lang-name is required, e.g. --lang-name Russian")


def cmd_init(root, data, a, today):
    validate_language(a.lang, a.lang_name)
    if (data / "settings.json").exists():
        sys.exit(f"error: {DATA_DIR_NAME}/settings.json already exists; use `settings` to change it")
    data.mkdir(parents=True, exist_ok=True)
    write_json(data / "settings.json", {
        "schema": SCHEMA,
        "language": a.lang,
        "language_name": a.lang_name,
        "created": today.isoformat(),
    })
    if not (data / ".gitignore").exists():
        (data / ".gitignore").write_text(WORKSPACE_GITIGNORE, encoding="utf-8")
    if not (data / "README.md").exists():
        (data / "README.md").write_text(WORKSPACE_README, encoding="utf-8")
    print(f"workspace created: {rel(root, data)}/ (settings.json, .gitignore, README.md)")
    if a.no_git:
        print("git: skipped (--no-git)")
    elif not git_available():
        print("git: not found, progress history disabled until git is installed")
    elif (data / ".git").exists():
        print("git: repository already present")
    else:
        code, _, err = run_git(["init", "-b", "main"], data)
        if code != 0:  # git older than 2.28 has no -b
            code, _, err = run_git(["init"], data)
            if code == 0:
                run_git(["symbolic-ref", "HEAD", "refs/heads/main"], data)
        print("git: initialized (branch main)" if code == 0 else f"git: init failed: {err}")
    return 0


def cmd_settings(root, data, a, today):
    path = data / "settings.json"
    settings, err = read_json(path)
    if err:
        sys.exit(f"error: {err}; run the `start` skill first")
    if a.lang or a.lang_name:
        validate_language(a.lang, a.lang_name)
        settings["language"], settings["language_name"] = a.lang, a.lang_name
        write_json(path, settings)
        print(f"conversation language set to {a.lang_name} [{a.lang}]")
    print(json.dumps(settings, ensure_ascii=False, indent=2))
    return 0


def cmd_new_course(root, data, a, today):
    course = a.course
    if not (data / "settings.json").exists():
        sys.exit("error: workspace not initialized; run `init` first")
    if not SLUG_RE.match(course):
        sys.exit(f"error: course slug must be lowercase letters, digits and dashes, got '{course}'")
    if a.track not in known_tracks():
        sys.exit(f"error: --track must be one of {', '.join(known_tracks())}")
    if not a.title:
        sys.exit("error: --title is required")
    cdir = data / course
    if (cdir / "course.json").exists():
        sys.exit(f"error: course '{course}' already exists")
    defaults, err = read_json(TRACKS_DIR / a.track / "course.json")
    if err:
        sys.exit(f"error: track template {err}")
    cdir.mkdir(parents=True, exist_ok=True)
    write_json(cdir / "course.json", {
        "schema": SCHEMA,
        "slug": course,
        "title": a.title,
        "track": a.track,
        "created": today.isoformat(),
        "options": defaults.get("options", {}),
    })
    print(f"course created: {rel(root, cdir)}/course.json (track: {a.track})")
    print("next: fill `options` from the track's setup.md, then run the diagnostic")
    return 0


# ---------------------------------------------------------------- course commands

def cmd_due(root, data, course, today):
    cdir, prog, header, rows, errs = load_course(data, course)
    print(f"course: {course}  today: {today}")
    if rows is None:
        print("not started (no program.md/progress.md)")
    else:
        shaky = [r["id"] for r in rows if r["status"] == "shaky"]
        due = sorted((due_date(r), r["id"]) for r in rows if is_due(r, today))
        print("shaky (always due): " + (", ".join(shaky) if shaky else "-"))
        print("solid, review due:  " + (", ".join(f"{i} (+{(today - d).days}d)" for d, i in due) if due else "-"))
    cards, _ = read_cards(cdir / "cards.md")
    if cards:
        dc = cards_due(cards, today)
        print(f"cards due: {len(dc)} of {len(cards)}" + (": " + ", ".join(c["front"] for c in dc[:30]) if dc else ""))
        if len(dc) > 30:
            print(f"  ... and {len(dc) - 30} more")
    return 0


def cmd_status(root, data, course, today):
    dirs = [need_course(data, course)] if course else course_dirs(data)
    if not dirs:
        print(f"no courses yet ({DATA_DIR_NAME}/ has none); run the `start` skill to create one")
        return 0
    for cdir in dirs:
        meta, _ = read_json(cdir / "course.json")
        tag = f"{cdir.name} [{(meta or {}).get('track', '?')}]"
        _, prog, header, rows, errs = load_course(data, cdir.name)
        if rows is None:
            print(f"{tag}: not started (diagnostic pending)")
            continue
        k = counts(rows)
        total = len(rows)
        due = sum(1 for r in rows if is_due(r, today))
        cards, _ = read_cards(cdir / "cards.md")
        card_part = f", cards due {len(cards_due(cards, today))}/{len(cards)}" if cards else ""
        print(f"{tag}: covered {total - k['todo']}/{total}, solid {k['solid']}, shaky {k['shaky']}, "
              f"learning {k['learning']}, due {due + k['shaky']}{card_part}, sessions {header.get('sessions', '?')}, "
              f"last {header.get('last_session', '-')}")
    return 0


def bar(part, whole, width=12):
    filled = round(width * part / whole) if whole else 0
    return "█" * filled + "░" * (width - filled)


def pct(part, whole):
    return f"{round(100 * part / whole)}%" if whole else "-"


def read_stages(lines):
    """Return ([(stage title, [topic ids])], {topic id: short title}) from program.md lines."""
    stages, titles, current = [], {}, None
    for line in lines:
        if line.startswith("## "):
            current = (line[3:].strip(), [])
            stages.append(current)
            continue
        m = TOPIC_RE.match(line)
        if m and current is not None:
            current[1].append(m.group(4))
            rest = m.group(5).lstrip("` ").lstrip("—–- ").strip()
            titles[m.group(4)] = rest.split(":", 1)[0].strip() or m.group(4)
    return [s for s in stages if s[1]], titles


def cmd_report(root, data, course, today):
    cdir, prog, header, rows, errs = load_course(data, course)
    meta, _ = read_json(cdir / "course.json")
    if rows is None:
        print(f"{course}: not started (no program.md/progress.md)")
        return 0
    topics, lines = prog
    stages, titles = read_stages(lines)
    by_id = {r["id"]: r for r in rows}
    k = counts(rows)
    total = len(rows)
    covered = total - k["todo"]
    due = [r for r in rows if is_due(r, today)]
    sessions = int(header["sessions"]) if header.get("sessions", "").isdigit() else 0

    print(f"Course: {(meta or {}).get('title', course)} [{(meta or {}).get('track', '?')}] · "
          f"entry level: {header.get('level', '?')} · started: {header.get('started', '?')}")
    print(f"Sessions: {sessions}, last: {header.get('last_session', '-')}")
    print()
    print("Overall")
    print(f"  covered   {bar(covered, total)} {covered}/{total} ({pct(covered, total)}), remaining {k['todo']}")
    print(f"  mastered  {bar(k['solid'], total)} {k['solid']}/{total} ({pct(k['solid'], total)}) solid")
    print(f"  quality   {pct(k['solid'], covered)} of covered topics are solid")
    print(f"  statuses  solid {k['solid']} · learning {k['learning']} · shaky {k['shaky']} · todo {k['todo']}")
    if sessions and covered:
        per_session = covered / sessions
        left = -(-k["todo"] // per_session)
        print(f"  pace      ~{per_session:.1f} topics per session; ~{int(left)} sessions to finish "
              "(rough: topics placed by the diagnostic inflate the pace)")
    print(f"  due now   {len(due) + k['shaky']} (shaky {k['shaky']}, solid on schedule {len(due)})")
    cards, _ = read_cards(cdir / "cards.md")
    if cards:
        boxes = [int(c["box"]) for c in cards if c["box"].isdigit()]
        print(f"  cards     {len(cards)} total, due {len(cards_due(cards, today))}, "
              f"in box 4-5 (well known) {sum(1 for b in boxes if b >= 4)}")
    print()

    print("By stage")
    for title, ids in stages:
        st = [by_id[i]["status"] for i in ids if i in by_id]
        n = len(st)
        cov = n - st.count("todo")
        print(f"  {bar(cov, n, 10)} {cov}/{n}  {title}  "
              f"(solid {st.count('solid')}, learning {st.count('learning')}, shaky {st.count('shaky')})")
    print()

    areas = {}
    for r in rows:
        areas.setdefault(r["id"].split(".")[0], []).append(r["status"])
    print("By area (ID prefix): solid / covered / total")
    for area, st in sorted(areas.items()):
        cov = len(st) - st.count("todo")
        shaky = f"   shaky {st.count('shaky')}" if st.count("shaky") else ""
        print(f"  {area:<14} {st.count('solid')} / {cov} / {len(st)}{shaky}")
    print()

    solid = sorted((r for r in rows if r["status"] == "solid"),
                   key=lambda r: (-int(r["reviews"]) if r["reviews"].isdigit() else 0, r["id"]))
    print(f"Strengths (solid: {len(solid)}, most reviewed first)")
    for r in solid[:10]:
        print(f"  + {r['id']} — {titles.get(r['id'], '')} (reviews: {r['reviews']})")
    if not solid:
        print("  none yet")
    print()
    weak = [r for r in rows if r["status"] == "shaky"]
    learning = [r for r in rows if r["status"] == "learning"]
    print(f"Weak spots (shaky: {len(weak)})")
    for r in weak:
        print(f"  ! {r['id']} — {titles.get(r['id'], '')}" + (f": {r['note']}" if r["note"] else ""))
    if not weak:
        print("  none")
    print(f"Not yet confirmed (learning: {len(learning)})")
    for r in learning:
        print(f"  ? {r['id']} — {titles.get(r['id'], '')}" + (f": {r['note']}" if r["note"] else ""))
    if not learning:
        print("  none")
    print()
    print("Next up: " + (header.get("next_up", "[]").strip("[]") or "-"))
    return 0


def cmd_sync(root, data, course, today):
    cdir, prog, header, rows, errs = load_course(data, course)
    if rows is None:
        sys.exit(f"error: {course} has no program.md/progress.md")
    status = {r["id"]: r["status"] for r in rows}
    topics, lines = prog
    changed = 0
    for i, checked, tid in topics:
        if tid not in status:
            continue
        want = status[tid] != "todo"
        if want != checked:
            m = TOPIC_RE.match(lines[i])
            lines[i] = f"{m.group(1)}{'x' if want else ' '}{m.group(3)}{m.group(4)}{m.group(5)}"
            changed += 1
    if changed:
        (cdir / "program.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"sync: {changed} checkbox(es) updated")
    return 0


def check_course_json(cdir: Path, course: str):
    errors = []
    meta, err = read_json(cdir / "course.json")
    if err:
        return [err], None
    for key in ("slug", "title", "track", "created", "options"):
        if key not in meta:
            errors.append(f"course.json: missing '{key}'")
    if meta.get("slug") not in (None, course):
        errors.append(f"course.json: slug is '{meta.get('slug')}', expected '{course}' (the folder name)")
    track = meta.get("track")
    if track and track not in known_tracks():
        errors.append(f"course.json: unknown track '{track}' (known: {', '.join(known_tracks())})")
    elif track:
        defaults, derr = read_json(TRACKS_DIR / track / "course.json")
        if not derr and isinstance(meta.get("options"), dict):
            for key in defaults.get("options", {}):
                if key not in meta["options"]:
                    errors.append(f"course.json: options.{key} missing (see tracks/{track}/course.json)")
    return errors, meta


def cmd_check(root, data, course, today):
    cdir = need_course(data, course)
    errors, meta = check_course_json(cdir, course)
    settings, serr = read_json(data / "settings.json")
    if serr:
        errors.append(f"{DATA_DIR_NAME}/{serr}")
    elif not LANG_TAG_RE.match(str(settings.get("language", ""))):
        errors.append("settings.json: 'language' must be a language tag such as en or ru")
    _, prog, header, rows, errs = load_course(data, course)
    if rows is None:
        if errors:
            print(f"{course}: {len(errors)} problem(s)")
            for e in errors:
                print("  - " + e)
            return 1
        print(f"{course}: course.json ok; program.md/progress.md missing (diagnostic pending)")
        return 0
    errors += errs
    topics, _ = prog
    prog_ids = [t[2] for t in topics]
    row_ids = [r["id"] for r in rows]
    if not prog_ids:
        errors.append("program.md: no topic lines found (format: - [ ] `area.topic` — Title: description)")
    for dup in sorted({i for i in prog_ids if prog_ids.count(i) > 1}):
        errors.append(f"program.md: duplicate topic id {dup}")
    for dup in sorted({i for i in row_ids if row_ids.count(i) > 1}):
        errors.append(f"progress.md: duplicate row for {dup}")
    for i in sorted(set(prog_ids) - set(row_ids)):
        errors.append(f"progress.md: missing row for topic {i}")
    for i in sorted(set(row_ids) - set(prog_ids)):
        errors.append(f"progress.md: row {i} has no topic in program.md")
    status = {r["id"]: r["status"] for r in rows}
    mismatched = sum(1 for _, checked, tid in topics if tid in status and (status[tid] != "todo") != checked)
    if mismatched:
        errors.append(f"program.md: {mismatched} checkbox(es) out of sync with progress.md (run: sync)")
    for r in rows:
        where = f"progress.md:{r['line']} ({r['id']})"
        if r["status"] not in STATUSES:
            errors.append(f"{where}: invalid status '{r['status']}'")
        for col in ("since", "reviewed"):
            if r[col] != "-" and not (DATE_RE.match(r[col]) and parse_date(r[col])):
                errors.append(f"{where}: {col} must be YYYY-MM-DD or '-', got '{r[col]}'")
        if not r["reviews"].isdigit():
            errors.append(f"{where}: reviews must be a number")
        if r["status"] == "solid" and r["since"] == "-":
            errors.append(f"{where}: solid topic needs a 'since' date")
        if r["status"] != "solid" and (r["since"] != "-" or r["reviewed"] != "-"):
            errors.append(f"{where}: since/reviewed must be '-' unless status is solid")
        if len(r["note"]) > NOTE_MAX:
            errors.append(f"{where}: note longer than {NOTE_MAX} chars")
    for key in ("course", "level", "sessions", "last_session"):
        if key not in header:
            errors.append(f"progress.md header: missing '{key}'")
    if header.get("course") and header["course"] != course:
        errors.append(f"progress.md header: course is '{header['course']}', expected '{course}'")
    if "sessions" in header and not header["sessions"].isdigit():
        errors.append("progress.md header: sessions must be a number")
    if not (cdir / "timeline.md").exists():
        errors.append("timeline.md: missing")
    cards, cerrs = read_cards(cdir / "cards.md")
    errors += cerrs
    fronts = [c["front"].lower() for c in cards]
    for dup in sorted({f for f in fronts if fronts.count(f) > 1}):
        errors.append(f"cards.md: duplicate card '{dup}'")
    for c in cards:
        where = f"cards.md:{c['line']} ({c['front']})"
        if not (c["box"].isdigit() and 1 <= int(c["box"]) <= 5):
            errors.append(f"{where}: box must be 1-5")
        if not (DATE_RE.match(c["next"]) and parse_date(c["next"])):
            errors.append(f"{where}: next must be YYYY-MM-DD")
    if errors:
        print(f"{course}: {len(errors)} problem(s)")
        for e in errors:
            print("  - " + e)
        return 1
    print(f"{course}: ok ({len(rows)} topics" + (f", {len(cards)} cards" if cards else "") + ")")
    return 0


# ---------------------------------------------------------------- sessions

def read_front_matter(path: Path):
    """Return the simple `key: value` pairs of a Markdown file's front matter."""
    fm = {}
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return fm
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip()
    return fm


HASH_EXT = {"py", "sh", "bash", "zsh", "fish", "yaml", "yml", "toml", "rb", "ps1", "r", "jl", "ex", "exs", "nim",
            "cr", "pl", "tf", "hcl", "coffee", "awk", "mk", "dockerfile", "conf", "ini", "gd", "tcl"}
DASH_EXT = {"sql", "lua", "hs", "elm", "ada", "adb", "ads", "vhd", "vhdl", "purs", "agda", "idr"}
PERCENT_EXT = {"tex", "erl", "hrl", "m", "pro", "mat"}
SEMI_EXT = {"clj", "cljs", "lisp", "lsp", "scm", "ss", "el", "rkt", "asm", "s", "fnl"}


def comment_line(ext: str, text: str, override: str = None) -> str:
    if override:
        return f"{override} {text}"
    e = ext.lower()
    if e in HASH_EXT:
        return f"# {text}"
    if e in DASH_EXT:
        return f"-- {text}"
    if e in PERCENT_EXT:
        return f"% {text}"
    if e in SEMI_EXT:
        return f"; {text}"
    if e in ("f", "f90", "f95", "f03"):
        return f"! {text}"
    if e in ("vb", "bas", "vbs"):
        return f"' {text}"
    if e in ("ml", "mli", "pas", "pp"):
        return f"(* {text} *)"
    if e in ("css", "scss", "less"):
        return f"/* {text} */"
    if e in ("html", "htm", "xml", "md", "svg", "vue", "svelte"):
        return f"<!-- {text} -->"
    if e in ("txt",):
        return text
    return f"// {text}"


def cmd_session(root, data, a, today):
    if len(a.extra) != 2:
        sys.exit("usage: learn_tool.py session <course> <mode> <slug> [--topics a,b] [--title T] [--ext ts]")
    mode, slug = a.extra
    course = a.course
    cdir = need_course(data, course)
    if mode not in SESSION_MODES:
        sys.exit(f"error: mode must be one of {', '.join(SESSION_MODES)}")
    if not SLUG_RE.match(slug):
        sys.exit(f"error: slug must be lowercase letters, digits and dashes, got '{slug}'")
    if a.ext and not EXT_RE.match(a.ext):
        sys.exit(f"error: bad extension '{a.ext}'")
    if mode != "diagnostic" and not (cdir / "program.md").exists():
        sys.exit(f"error: course '{course}' has no program.md yet; run the diagnostic first")
    tpl_path = TEMPLATES_DIR / "lesson.md"
    if not tpl_path.exists():
        sys.exit(f"error: template not found: {tpl_path}")
    meta, _ = read_json(cdir / "course.json")

    sessions = cdir / "sessions"
    name = f"{today.isoformat()}-{slug}"
    folder, n = sessions / name, 2
    while folder.exists():
        folder = sessions / f"{name}-{n}"
        n += 1
    folder.mkdir(parents=True)

    topics = ", ".join(t.strip() for t in (a.topics or "").split(",") if t.strip())
    if a.ext:
        where_work = f"Hands-on work goes into `practice.{a.ext}` (each task names the exact place and how to check it)."
    elif mode in ("test", "diagnostic"):
        where_work = "Everything is answered in this file, right under each question."
    else:
        where_work = "If a task needs another file, the task names it."
    values = {
        "course": course,
        "track": (meta or {}).get("track", "?"),
        "date": today.isoformat(),
        "mode": mode,
        "topics": topics,
        "practice": f"practice.{a.ext}" if a.ext else "none",
        "title": a.title or f"Session: {slug}",
        "where_work": where_work,
    }
    text = tpl_path.read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    (folder / "lesson.md").write_text(text, encoding="utf-8")
    if a.ext:
        header = comment_line(a.ext, f"{values['title']}: tasks are described in lesson.md", a.comment)
        (folder / f"practice.{a.ext}").write_text(header + "\n", encoding="utf-8")

    print(f"session created: {rel(root, folder)}")
    print(f"  lesson:   {rel(root, folder / 'lesson.md')}")
    print("  practice: " + (rel(root, folder / ('practice.' + a.ext)) if a.ext else "none"))
    print("  note: translate the lesson intro block into the learner's language before handing it over")
    return 0


def cmd_open(root, data, course, today):
    dirs = [need_course(data, course)] if course else course_dirs(data)
    found = []
    for cdir in dirs:
        for lesson in (cdir / "sessions").glob("*/lesson.md"):
            fm = read_front_matter(lesson)
            if fm.get("status") == "open":
                found.append((lesson.parent.name, lesson, fm))
    found.sort(key=lambda t: t[0], reverse=True)
    if not found:
        print("no open sessions")
        return 0
    for _, lesson, fm in found:
        print(f"{rel(root, lesson.parent)}  mode={fm.get('mode', '?')}  "
              f"topics={fm.get('topics', '[]')}  practice={fm.get('practice', 'none')}")
    return 0


# ---------------------------------------------------------------- interactive exercises

def results_name(fname: str) -> str:
    stem = fname[:-5] if fname.endswith(".json") else fname
    if stem.startswith("exercises"):
        return "results" + stem[len("exercises"):] + ".json"
    return stem + ".results.json"


def page_name(fname: str) -> str:
    return (fname[:-5] if fname.endswith(".json") else fname) + ".html"


def pick_session(cdir: Path, name):
    sessions = cdir / "sessions"
    if name:
        folder = sessions / name
        if not (folder / "lesson.md").exists():
            sys.exit(f"error: session '{name}' not found in {cdir.name}/sessions")
        return folder
    open_ones = sorted((p.parent for p in sessions.glob("*/lesson.md")
                        if read_front_matter(p).get("status") == "open"), key=lambda p: p.name, reverse=True)
    if not open_ones:
        sys.exit("error: no open session; pass --session <folder name>")
    return open_ones[0]


def _strs(v, n_min=1):
    return isinstance(v, list) and len(v) >= n_min and all(isinstance(x, str) and x.strip() for x in v)


def validate_exercises(data):
    errors = []
    if not isinstance(data, dict):
        return ["exercises: top level must be an object"]
    mode = data.get("mode", "drill")
    if mode not in ("drill", "exam"):
        errors.append("mode must be 'drill' or 'exam'")
    if "lang" in data and not (isinstance(data["lang"], str) and LANG_TAG_RE.match(data["lang"])):
        errors.append("lang must be a language tag such as en-US")
    items = data.get("items")
    if not isinstance(items, list) or not items:
        return errors + ["items must be a non-empty list"]
    seen = set()
    for n, it in enumerate(items, start=1):
        where = f"items[{n}]"
        if not isinstance(it, dict):
            errors.append(f"{where}: must be an object")
            continue
        iid = it.get("id")
        where = f"items[{n}] ({iid})"
        if not isinstance(iid, str) or not iid.strip():
            errors.append(f"{where}: id must be a non-empty string")
        elif iid in seen:
            errors.append(f"{where}: duplicate id")
        seen.add(iid)
        typ = it.get("type")
        if typ not in ITEM_TYPES:
            errors.append(f"{where}: type must be one of {', '.join(ITEM_TYPES)}")
            continue
        for key in ("prompt", "explain", "say", "audio", "topic", "card"):
            if key in it and it[key] is not None and not isinstance(it[key], str):
                errors.append(f"{where}: {key} must be a string")
        has_key = any(k in it for k in ("answer", "accept")) or (
            typ == "gap" and any(isinstance(g, dict) and "accept" in g for g in it.get("gaps") or []))
        if mode == "exam" and has_key:
            errors.append(f"{where}: exam mode must not contain answers (answer/accept): solutions stay off disk")
        if mode == "exam" and "say" in it:
            errors.append(f"{where}: exam mode must not use 'say' (it reads the answer aloud); use 'audio' for a listening prompt")
        if typ == "choice":
            opts = it.get("options")
            if not isinstance(it.get("prompt"), str) or not it["prompt"].strip():
                errors.append(f"{where}: prompt is required")
            if not _strs(opts, 2) or len(opts) > 9:
                errors.append(f"{where}: options must be 2-9 non-empty strings")
            elif len({o.strip().lower() for o in opts}) != len(opts):
                errors.append(f"{where}: options must be distinct")
            ans = it.get("answer")
            if mode == "drill" and not (isinstance(ans, int) and not isinstance(ans, bool)
                                        and isinstance(opts, list) and 0 <= ans < len(opts)):
                errors.append(f"{where}: answer must be the 0-based index of the correct option")
        elif typ == "gap":
            text, gaps = it.get("text"), it.get("gaps")
            if not isinstance(text, str) or not isinstance(gaps, list) or not gaps:
                errors.append(f"{where}: text (with {{{{1}}}}, {{{{2}}}} ...) and a non-empty gaps list are required")
                continue
            nums = [int(x) for x in GAP_RE.findall(text)]
            if sorted(nums) != list(range(1, len(gaps) + 1)):
                errors.append(f"{where}: text must contain {{{{1}}}}..{{{{{len(gaps)}}}}} exactly once each "
                              f"(found {nums or 'none'})")
            for k, g in enumerate(gaps, start=1):
                if not isinstance(g, dict):
                    errors.append(f"{where}: gaps[{k}] must be an object")
                    continue
                if "options" in g and not _strs(g["options"], 2):
                    errors.append(f"{where}: gaps[{k}].options must be 2+ non-empty strings")
                if mode == "drill":
                    if not _strs(g.get("accept")):
                        errors.append(f"{where}: gaps[{k}].accept must list the accepted answers")
                    elif "options" in g and _strs(g["options"], 2) and not set(g["accept"]) & set(g["options"]):
                        errors.append(f"{where}: gaps[{k}]: no accepted answer is among the options")
        elif typ == "order":
            if not _strs(it.get("tokens"), 2):
                errors.append(f"{where}: tokens must be 2+ non-empty strings")
            if mode == "drill" and not _strs(it.get("accept")):
                errors.append(f"{where}: accept must list the correct sentence(s)")
        elif typ == "flashcard":
            if mode == "exam":
                errors.append(f"{where}: flashcards are self-graded and only allowed in drill mode")
            for key in ("front", "back"):
                if not isinstance(it.get(key), str) or not it[key].strip():
                    errors.append(f"{where}: {key} is required")
    return errors


def build_page(data: Path, cdir: Path, folder: Path, fname: str, token: str, served: bool):
    """Return (html, exercises, errors)."""
    ex, err = read_json(folder / fname)
    if err:
        return None, None, [f"{folder.name}/{err}"]
    errors = validate_exercises(ex)
    if errors:
        return None, ex, errors
    tpl = INTERACTIVE_DIR / "player.html"
    ui, uerr = read_json(INTERACTIVE_DIR / "ui.en.json")
    if not tpl.exists() or uerr:
        return None, ex, ["player template missing or broken in .agents/skills/learn/interactive/"]
    custom, cerr = read_json(data / "ui.json")
    if custom and not cerr and isinstance(custom, dict):
        ui.update({k: v for k, v in custom.items() if isinstance(v, str)})
    if isinstance(ex.get("ui"), dict):
        ui.update({k: v for k, v in ex["ui"].items() if isinstance(v, str)})
    settings, _ = read_json(data / "settings.json")
    payload = {"exercises": ex, "ui": ui, "meta": {
        "course": cdir.name, "session": folder.name, "file": fname, "served": served, "token": token,
        "ui_lang": (settings or {}).get("language", "en")}}
    blob = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/").replace("<!--", "<\\!--")
    html = tpl.read_text(encoding="utf-8").replace(DATA_PLACEHOLDER, blob, 1)
    return html, ex, []


def summarize(ex):
    kinds = {}
    for it in ex.get("items", []):
        kinds[it.get("type")] = kinds.get(it.get("type"), 0) + 1
    kinds_text = ", ".join(f"{k} {v}" for k, v in kinds.items())
    return f"{len(ex.get('items', []))} items ({kinds_text}), mode {ex.get('mode', 'drill')}"


def print_problems(root, path, errors):
    print(f"{rel(root, path)}: {len(errors)} problem(s)")
    for e in errors:
        print("  - " + e)


def cmd_exercises(root, data, a, today):
    cdir = need_course(data, a.course)
    folder = pick_session(cdir, a.session)
    fname = a.file or "exercises.json"
    html, ex, errors = build_page(data, cdir, folder, fname, "", served=False)
    if errors:
        print_problems(root, folder / fname, errors)
        return 1
    out = folder / page_name(fname)
    out.write_text(html, encoding="utf-8")
    print(f"ok: {summarize(ex)}")
    print(f"static page: {rel(root, out)} (open it in a browser; results via Download or Copy)")
    extra = f" --file {fname}" if fname != "exercises.json" else ""
    print(f"served mode (answers saved automatically): learn_tool.py serve {cdir.name} --session {folder.name}{extra}")
    return 0


def cmd_serve(root, data, a, today):
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    cdir = need_course(data, a.course)
    folder = pick_session(cdir, a.session)
    fname = a.file or "exercises.json"
    token = secrets.token_urlsafe(16)
    html, ex, errors = build_page(data, cdir, folder, fname, token, served=True)
    if errors:
        print_problems(root, folder / fname, errors)
        return 1
    results_path = folder / results_name(fname)
    last_seen = [time.monotonic()]

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):  # keep the console quiet
            pass

        def _send(self, code, body: bytes, ctype="text/plain; charset=utf-8"):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            last_seen[0] = time.monotonic()
            path = self.path.split("?", 1)[0]
            if path in ("/", "/index.html"):
                # Rebuilt on every request, so an edited exercise file shows up on reload.
                page, _, errs = build_page(data, cdir, folder, fname, token, served=True)
                if errs:
                    self._send(500, ("exercise file problems:\n" + "\n".join(errs)).encode("utf-8"))
                else:
                    self._send(200, page.encode("utf-8"), "text/html; charset=utf-8")
            elif path == "/health":
                self._send(200, b"ok")
            else:
                self._send(404, b"not found")

        def do_POST(self):
            last_seen[0] = time.monotonic()
            if self.path != "/results" or self.headers.get("X-Session-Token") != token:
                return self._send(403, b"forbidden")
            length = int(self.headers.get("Content-Length") or 0)
            if length <= 0 or length > 2_000_000:
                return self._send(413, b"too large")
            try:
                body = json.loads(self.rfile.read(length).decode("utf-8"))
                if not isinstance(body, dict) or not isinstance(body.get("items"), list):
                    raise ValueError("bad shape")
            except (ValueError, UnicodeDecodeError):
                return self._send(400, b"bad json")
            tmp = results_path.with_suffix(".tmp")
            write_json(tmp, body)
            os.replace(tmp, results_path)
            if body.get("finished"):
                print(f"results saved: {rel(root, results_path)} "
                      f"(finished, {body.get('answered')}/{body.get('total')} answered)", flush=True)
            return self._send(200, b"saved")

    server, port = None, a.port
    for candidate in range(a.port, a.port + 20):
        try:
            server = ThreadingHTTPServer(("127.0.0.1", candidate), Handler)
            port = candidate
            break
        except OSError:
            continue
    if server is None:
        sys.exit(f"error: no free port in {a.port}-{a.port + 19}")
    url = f"http://127.0.0.1:{port}/"
    print(f"serving {rel(root, folder / fname)}: {summarize(ex)}")
    print(f"open: {url}")
    print(f"answers are saved to {rel(root, results_path)} after every answer")
    print(f"stops by itself after {a.idle_timeout // 60} min without activity, or press Ctrl+C", flush=True)

    def watchdog():
        while True:
            time.sleep(5)
            if time.monotonic() - last_seen[0] > a.idle_timeout:
                print("idle timeout: stopping", flush=True)
                server.shutdown()
                return

    threading.Thread(target=watchdog, daemon=True).start()
    if not a.no_browser:
        try:
            webbrowser.open(url)
        except Exception:  # noqa: BLE001 - a missing browser must not stop the server
            pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


# ---------------------------------------------------------------- entry point

COMMANDS = ("doctor", "init", "settings", "new-course", "status", "report", "due", "check", "sync", "session", "open",
            "exercises", "serve")
NEEDS_COURSE = ("new-course", "report", "due", "check", "sync", "session", "exercises", "serve")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=COMMANDS)
    ap.add_argument("course", nargs="?")
    ap.add_argument("extra", nargs="*", help="session: <mode> <slug>")
    ap.add_argument("--topics", help="session: comma-separated topic IDs")
    ap.add_argument("--title", help="session: lesson title; new-course: course title")
    ap.add_argument("--ext", help="session: extension of the practice file, e.g. ts, py, md")
    ap.add_argument("--track", help="new-course: track name (folder under .agents/skills/learn/tracks)")
    ap.add_argument("--lang", help="init/settings: conversation language tag, e.g. ru, en-US")
    ap.add_argument("--lang-name", help="init/settings: language name in English, e.g. Russian")
    ap.add_argument("--no-git", action="store_true", help="init: do not create a git repository")
    ap.add_argument("--comment", help="session: comment prefix for the practice file header, e.g. '#'")
    ap.add_argument("--session", help="exercises/serve: session folder name (default: newest open session)")
    ap.add_argument("--file", help="exercises/serve: exercise file in the session folder (default: exercises.json)")
    ap.add_argument("--port", type=int, default=8765, help="serve: first port to try (default 8765)")
    ap.add_argument("--no-browser", action="store_true", help="serve: do not open a browser window")
    ap.add_argument("--idle-timeout", type=int, default=3 * 3600, help="serve: stop after N idle seconds")
    ap.add_argument("--root", type=Path, help="repository root (default: found via AGENTS.md)")
    ap.add_argument("--data", type=Path, help=f"learner workspace (default: <root>/{DATA_DIR_NAME})")
    ap.add_argument("--today", help="override today's date, YYYY-MM-DD (for tests)")
    a = ap.parse_args()
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")  # Windows consoles default to a legacy codepage
        except (AttributeError, ValueError):
            pass
    root = a.root.resolve() if a.root else find_root(Path.cwd().resolve())
    data = a.data.resolve() if a.data else root / DATA_DIR_NAME
    today = parse_date(a.today) if a.today else date.today()
    if today is None:
        ap.error("--today must be YYYY-MM-DD")
    if a.command in NEEDS_COURSE and not a.course:
        ap.error(f"'{a.command}' needs a course slug")
    if a.command in ("init", "settings", "doctor") and a.course:
        ap.error(f"'{a.command}' takes no positional arguments")
    if a.command in ("doctor", "init", "settings", "new-course", "session", "exercises", "serve"):
        fn = {"doctor": cmd_doctor, "init": cmd_init, "settings": cmd_settings, "new-course": cmd_new_course,
              "session": cmd_session, "exercises": cmd_exercises, "serve": cmd_serve}[a.command]
        sys.exit(fn(root, data, a, today))
    fn = {"status": cmd_status, "report": cmd_report, "due": cmd_due, "check": cmd_check,
          "sync": cmd_sync, "open": cmd_open}[a.command]
    sys.exit(fn(root, data, a.course, today))


if __name__ == "__main__":
    main()
