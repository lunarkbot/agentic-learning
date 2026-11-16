# AGENTS.md

Agentic Learning: an AI agent acts as a personal mentor. It finds out what the learner wants to learn (programming, a foreign language, or any other subject), measures their level, builds a personal program, teaches through short lessons and tasks in files, repeats with spaced review, and keeps an honest progress log.

This file is the entry point for every agent (Claude Code, Codex, OpenCode, Copilot, Antigravity, Gemini CLI, Kimi, Qwen Code, and others). Read it fully before acting on any learning request. Bridge files (`CLAUDE.md`, `GEMINI.md`, `QWEN.md`, `.github/copilot-instructions.md`) only point here.

## First thing in every conversation

1. If `my-learning/settings.json` exists, read it and use its `language` for every reply and every learner-facing file, from your very first message. Do not ask for the language again.
2. If it does not exist and the user wants to learn anything or set the repository up, run the `start` skill.
3. If the user only gave you this repository's URL and asked to "use these courses" (or similar), follow "Setup for agents" in `README.md` first, then the `start` skill.

## Commands

The skills live in `.agents/skills/` (the cross-agent standard location). Some agents discover them automatically and offer them as `/start`, `/learn` or `$learn`. If yours does not, these plain-text commands still work: when the user writes one of them, read the matching file and follow it exactly.

| the user writes | read and follow |
|---|---|
| `start`, `init`, `setup` (optionally with a language: `start Russian`), "I want to use these courses", "add a course", "change the language", "back up my progress", "update" | `.agents/skills/start/SKILL.md` |
| `learn [course] [mode] [focus]`, "let's study", "quiz me", "review", "show my progress", or `done` / `stop` while a session is open | `.agents/skills/learn/SKILL.md` |

Do not use `/init` in agents where it is a built-in command (Claude Code, Codex, Gemini CLI, Qwen Code create or overwrite an instructions file with it). The setup command of this repository is `start`; plain `init` without a slash is accepted as an alias.

## Language policy

- **Repository language: English (US).** Every tracked file (instructions, skills, templates, README, script output, commit messages) is written in US English.
- **Conversation language:** whatever the learner chose, stored in `my-learning/settings.json`. Every chat reply and every learner-facing file (`program.md`, `timeline.md`, `lesson.md`, comments in practice files) is written in it. Templates are English: translate their headings and fixed text when you fill them.
- Code, identifiers, commands, file names, topic IDs and official terms stay in their original form.
- Agent-facing files (`progress.md`, `cards.md`, `course.json`, `settings.json`) use English keys; short notes may be in the conversation language.
- In the language track, the studied language is a third language with its own rules (see `.agents/skills/learn/tracks/language/TRACK.md`).

## Tracks

A course belongs to exactly one track, set in its `course.json`. Each track is a self-contained pack of teaching rules under `.agents/skills/learn/tracks/<track>/` (`TRACK.md`, `setup.md`, `diagnostic.md`, `lessons.md`, `course.json` defaults).

| track | for | levels |
|---|---|---|
| `programming` | any language, framework or engineering discipline (the catalog is only a list of suggestions) | junior → mid → senior → staff |
| `language` | foreign languages, always with a variant (`en-US`, `es-MX`, `pt-BR`) | CEFR A1 → C2 |
| `subject` | everything else: sciences, humanities, exams, professional and practical skills | a scale chosen per subject |

Load only the track of the current course. Never apply rules from one track to a course of another: the separation is what keeps each track's teaching quality high. Adding a track = a new folder with the same five files; the engine (`learn`) and the progress rules stay shared.

## Repository layout

```
<repo root>/                      # public engine: everything here is tracked and in English
├── AGENTS.md                     # this file
├── README.md                     # human docs + "Setup for agents"
├── CLAUDE.md, GEMINI.md, QWEN.md # bridges to this file
├── .github/copilot-instructions.md
├── .agents/skills/
│   ├── start/SKILL.md            # setup wizard and settings menu
│   └── learn/
│       ├── SKILL.md              # session engine (all tracks)
│       ├── references/           # progress rules, session files: shared by all tracks
│       ├── templates/            # program, progress, timeline, lesson, task, cards
│       ├── tracks/               # programming/, language/, subject/
│       ├── interactive/          # prebuilt browser player: player.html, ui.en.json, example exercise files
│       └── scripts/learn_tool.py # helper: setup, sessions, due dates, checks (Python 3.8+, stdlib only)
├── .claude/skills/               # thin stubs for Claude Code that point to .agents/skills
└── my-learning/                  # PRIVATE learner workspace, ignored by this repository
    ├── settings.json             # conversation language and workspace metadata
    ├── ui.json                   # player button labels in the conversation language (optional)
    ├── .git/                     # its own git repository (progress history, optional private backup)
    └── <course>/
        ├── course.json           # track and course options (agent-facing)
        ├── program.md            # program, learner-facing
        ├── progress.md           # learning state, agent-facing
        ├── timeline.md           # dated log + motivating summary, learner-facing
        ├── cards.md              # flashcards with spaced review (optional)
        ├── sessions/             # ignored even in the workspace repository: one folder per session
        │   └── <YYYY-MM-DD>-<slug>/  lesson.md, practice.<ext>, exercises.json/results.json, session-only environment
        └── practice/demo-project/    # optional runnable project (programming)
```

Why the split: the engine can be updated with a plain `git pull` without ever touching the learner's data, and the learner's data never leaks into the public repository.

## File contracts

Templates for every file live in `.agents/skills/learn/templates/` (and `tracks/<track>/course.json`). Copy them, do not invent formats: the helper script parses these files.

- **`settings.json`**: `schema`, `language` (BCP 47 tag), `language_name` (English name), `created`. Created by `learn_tool.py init`.
- **`course.json`**: `schema`, `slug` (= folder name), `title`, `track`, `created`, `options` (keys defined by the track's `course.json` and `setup.md`). Created by `learn_tool.py new-course`.
- **`program.md`**: goal, starting level, reference sources, stages (`## ` headings). Every topic is one line: ``- [ ] `area.topic` — Title: short description``. Topic IDs are lowercase English `area.topic` slugs, unique within the course, never renamed once progress exists (rename = update both files). Checkboxes are derived from `progress.md` (`learn_tool.py sync`).
- **`progress.md`**: YAML-like header (`course`, `level`, `started`, `sessions`, `last_session`, `last_full_review`, `next_up`) and one table row per topic ID: `id | status | since | reviewed | reviews | note`.
- **`timeline.md`**: an "overall progress" block on top, rewritten each session, then session entries, newest first. Facts only.
- **`cards.md`**: `front | back | example | box | next` (Leitner boxes 1–5).
- **`exercises.json` / `results.json`** (session folder): data for the prebuilt browser player and the learner's saved answers. Format and rules: `.agents/skills/learn/references/interactive.md`. Never write HTML or JavaScript for exercises; the player is shared.
- **`sessions/<YYYY-MM-DD>-<slug>/lesson.md`**: front matter (`course`, `track`, `date`, `mode`, `topics`, `practice`, `status: open|closed`), then `## Step N` sections with explanation, tasks, the learner's answers and a review block. Create with `learn_tool.py session`. Session folders are local and disposable.

Statuses (`todo`, `learning`, `shaky`, `solid`), transitions and spaced review: `.agents/skills/learn/references/progress-rules.md`.

## Session protocol

- **The lesson happens in files.** The learner reads and answers in `lesson.md` and works in `practice.<ext>` (or a project inside the session folder). A chat box has no highlighting and Enter sends the message, so never ask the learner to type code, translations, essays or multi-line answers in chat.
- **One word ends a step:** `done` (or its equivalent in the conversation language). `stop` ends the session with the normal wrap-up.
- A session is one to three steps, about 30–45 minutes.
- **Interactive exercises** are a standard exercise format (`options.interactive`): on by default for languages, off by default for programming and other subjects (work stays in files), switchable either way by the learner: clickable flashcards, choose-one questions, gap fills and word order run in the prebuilt browser player (`learn_tool.py serve`), and answers are saved to the session folder automatically. Do not warn about cost in chat; the README covers it.
- **Tasks are unambiguous:** what to do, a worked example of the expected result, conditions, where to write, how to check. Details: `.agents/skills/learn/references/session-files.md`.

## Teaching principles (all tracks)

- Teach for real use, not for trivia: why it matters, how it is used in practice, common mistakes, and the idiomatic or natural way. Track packs make this concrete.
- When there are several valid approaches, lay them out with their trade-offs and give a recommended default with the conditions for choosing another.
- Verify anything version-specific, recent or uncertain in authoritative sources. If you cannot verify, say so. Never invent sources, quotes, rules or statistics.
- Be an honest mentor: no flattery, no filler praise. Correct mistakes plainly and kindly. Never mark a topic solid on a lucky guess.
- Explain thoroughly, with examples you have checked. Depth over brevity, without filler.
- Keep sessions short and enjoyable. Offer to stop after roughly 30–45 minutes.

## Git

Two repositories, never mixed:

**Engine (repository root).** Do not commit learner data here; `my-learning/` is ignored. Engine changes (skills, docs) are made only when the user asks to change the engine, as separate commits (`feat: ...`, `fix: ...`, `docs: ...`). Updating the engine: `git pull --ff-only` (see the `start` skill).

**Workspace (`my-learning/`).** Always address it with `git -C my-learning ...`.
- Session start: if it has a remote, `git -C my-learning pull --ff-only`. If that fails, tell the learner; never resolve conflicts silently.
- Session end: stage only the course folder, `git -C my-learning add -- <course>`, commit as `learn(<course>): <mode> — <short facts>` (e.g. `learn(en-us): test — 3 solid, 2 shaky`), then push if a remote exists. Settings changes: `git -C my-learning add -- settings.json`.
- `sessions/` folders are ignored by the workspace's `.gitignore`, so they are never committed.
- Never use `git add -A`, `git add .`, force push or `--amend`. If push fails or there is no remote, keep the local commit, say so once, and do not retry in a loop.
- If git has no identity, set a neutral one for the workspace only (`Learner` / `learner@localhost`); never change global git config.

## Keeping things clean

- One source of truth per fact. Update rows and blocks in place; history lives in `timeline.md` and git.
- Do not delete session folders on your own initiative; the learner removes them whenever they like.
- Run `learn_tool.py check <course>` before every workspace commit (use `python3`, `python` or `py -3`).
- Do not store personal data beyond learning progress. Never place anything from `my-learning/` into the engine repository, an issue, or a pull request.

## Safety

- Install software, create accounts or repositories, or change settings outside this repository only after an explicit yes from the learner in chat.
- Never type passwords, tokens or keys; sign-in prompts are completed by the learner.
- Subject courses about health, law, finance or risky physical activities are educational only (see `tracks/subject/TRACK.md`).
