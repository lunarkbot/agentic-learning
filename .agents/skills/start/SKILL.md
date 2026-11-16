---
name: start
description: First-run setup wizard and settings menu for this learning repository. Asks which language to talk in (or takes it from the argument, e.g. "start Russian"), saves it to my-learning/settings.json, asks whether the learner wants to study programming, a foreign language, or another subject, sets up the course, and hands over to the placement test. When setup is already done, shows a menu to add a course, change a course's settings (such as interactive browser exercises), change the conversation language, back up progress, or update the engine. Use when the user types /start, $start, start, init, setup, or says things like "I want to use these courses", "set this up", "add a new course", "change the language", "back up my progress".
---

# start: setup wizard and settings

You are setting up a personal learning workspace for someone who may not be technical at all. Be warm, brief and concrete: one question at a time (or one small group), numbered options they can answer with a digit, no jargon. Never paste long instructions into chat.

Conventions (layout, git rules, language policy) are in `AGENTS.md` at the repository root; read it first if it is not in your context. The helper script is `.agents/skills/learn/scripts/learn_tool.py` (run it with `python3`, then `python`, then `py -3`; call it `TOOL` below). If no Python is available, do every step by hand: the script only creates the files described here.

## 0. Where are we?

1. Make sure you are at the repository root (the folder with `AGENTS.md`). If the user opened a parent folder, `cd` into the repository for every command.
2. Run `TOOL doctor`. It reports Python, git, the workspace and the courses. If no Python interpreter works, check by hand instead: `git --version`, and whether `my-learning/settings.json` exists.
3. If `my-learning/settings.json` exists, setup is done: go to section 6 (menu). If the user wrote `start <language>` and that language differs from the saved one, offer to switch (section 6, item 3).
4. Otherwise run sections 1–5 in order.

## 1. Conversation language

The argument after the command is the language to talk in, written any way: `start Russian`, `start ru`, `start русский`, `init español`, `start pt-BR`.

- **Argument given**: map it to a BCP 47 tag and an English name (`ru` / `Russian`, `es` / `Spanish`, `pt-BR` / `Portuguese (Brazil)`, `zh-Hans` / `Chinese (Simplified)`). If it is ambiguous (`Chinese`), ask one short question. From now on write everything in that language.
- **No argument**: ask exactly one question, in English, and if the user's previous message was clearly in another language, add the same question in that language and propose it as the default:
  > Which language would you like me to use from now on? Reply with any language, e.g. "English", "Русский", "Español", "Deutsch".

Keep the answer in mind; it is saved at the end of section 2, once the computer is ready. The conversation language is used for every chat message and every learner-facing file, in this and all future sessions. Do not ask it again; it can be changed from the menu.

## 2. Prepare the computer (first run only)

Everything works best with a few free tools. Check them, and if something is missing, **offer** to set the computer up. Never install anything without a clear yes in chat.

| tool | what it is for | how to check |
|---|---|---|
| Python 3.8+ | the helper: progress dates, checks, sessions, saving answers from browser exercises | `python3 --version`, `python --version`, `py -3 --version`: the output must say `Python 3.x` |
| git | history of your progress, backup, updates of the tutor | `git --version` |
| an editor with Markdown preview | reading lessons and writing answers comfortably | ask the learner; any editor works, even Notepad or TextEdit |
| a web browser | interactive exercises | always present on desktop systems |

1. **Everything present**: say nothing about it and go on.
2. **Something missing**: send one short message: what is missing, what each item is for (one line each, plain words), and the exact plan, then ask for one yes (or let the learner pick by number). Example plan for Windows: "install Python and Git with winget, the Windows package manager; takes about two minutes". VS Code is only *offered* as a nicer editor, never required.
3. **Install after the yes**, one tool at a time, with the system package manager:

   | OS | Python | git | VS Code (optional) |
   |---|---|---|---|
   | Windows | `winget install --id Python.Python.3.13 -e` | `winget install --id Git.Git -e` | `winget install --id Microsoft.VisualStudioCode -e` |
   | macOS (Homebrew) | `brew install python` | `brew install git` (or `xcode-select --install`) | `brew install --cask visual-studio-code` |
   | Debian / Ubuntu | `sudo apt install python3` | `sudo apt install git` | the `.deb` from code.visualstudio.com |
   | Fedora | `sudo dnf install python3` | `sudo dnf install git` | the `.rpm` from code.visualstudio.com |

   - No package manager (old Windows without `winget`, macOS without Homebrew): do not install a package manager on your own. Give the official download page (python.org/downloads, git-scm.com/downloads, code.visualstudio.com) and walk the learner through the installer in plain words; on Windows remind them to tick "Add python.exe to PATH".
   - `sudo` asks for the learner's computer password: they type it themselves in the terminal; never ask for it in chat.
   - Windows traps: a freshly installed program is often not on the PATH of the already running shell. Use the `py -3` launcher or the full path (e.g. `%LOCALAPPDATA%\Programs\Python\Python313\python.exe`) for the rest of this session, or ask the learner to restart the agent. If `python` opens the Microsoft Store, that is the store alias, not a real Python: use `py -3` or the full path.
4. Run `TOOL doctor` again and report the result in one line.
5. **Declined or failed**: continue without it, in one line say what will be missing (no Python: the agent keeps the files by hand, browser exercises save results by download/copy; no git: no history and backup). Offer again only when a feature needs it.

Course-specific tools (Node for TypeScript, Go, Docker ...) are offered later, in the course setup, the same way.

**Save the language now**: `TOOL init --lang <tag> --lang-name "<English name>"`. This creates `my-learning/` (private workspace, ignored by the public repository) with `settings.json`, a `.gitignore` and a small README, and initializes a git repository inside it. Without Python, create the same files by hand (format in `AGENTS.md`, "File contracts") and run `git init -b main` inside `my-learning/` if git exists.

## 3. What to learn

Ask (in the conversation language):

> What would you like to learn?
> 1. Programming: a language, framework or engineering area (Go, TypeScript, Python, React, DevOps, ...)
> 2. A foreign language: English, Spanish, German, Japanese, ...
> 3. Something else: physics, math, history, an exam, a professional skill, a hobby ...

Free answers are fine ("американский английский" → 2). Map the answer to a track: `programming`, `language` or `subject`.

## 4. Course setup (one track only)

1. Read `.agents/skills/learn/tracks/<track>/TRACK.md` and `.agents/skills/learn/tracks/<track>/setup.md`. Do not read the other tracks: their rules do not apply and would only confuse the setup.
2. Ask the setup questions from `setup.md`, in the conversation language, a few at a time.
3. Create the course: `TOOL new-course <slug> --track <track> --title "<title in the conversation language>"`.
4. Fill `options` in `my-learning/<slug>/course.json` with the answers (keys from `setup.md`; keep the JSON valid).
5. `TOOL check <slug>` must say "course.json ok".
6. If `options.interactive` is `true` (the default for languages), the conversation language is not English, and `my-learning/ui.json` does not exist yet: create it from `.agents/skills/learn/interactive/ui.en.json` with every value translated into the conversation language (same keys, keep the `{n}`, `{total}`, `{correct}` placeholders). This is done once for all courses.
7. Commit inside the workspace (see "Git" in `AGENTS.md`), adding `ui.json` if it was created:
   `git -C my-learning add -- settings.json .gitignore README.md <slug>`
   `git -C my-learning commit -m "learn(<slug>): setup — <track>, <one fact>"`
   If git has no identity configured, set one for this repository only: `git -C my-learning config user.name "Learner"` and `git -C my-learning config user.email "learner@localhost"` (never touch the global config, never use real personal data unless the learner gives it).

## 5. Hand-over

In at most six short lines, in the conversation language:
- what was created (the course name, the chosen options in one line);
- how a session works: lessons and tasks are in files the learner opens in their editor; they answer in the file and send `done`; `stop` ends the session;
- the main command: `learn <slug>` typed as a plain message works in every agent; where skills are slash commands it is also `/learn <slug>` (e.g. Claude Code), in Codex `$learn <slug>`;
- then ask: "Start the placement test now?" On yes, follow `.agents/skills/learn/SKILL.md` for this course (it runs the diagnostic because `program.md` does not exist yet).

## 6. Menu (setup already done)

Show the courses from `TOOL status` in one line each, then offer, in the conversation language:

1. **Add a course** → sections 3–5.
2. **Change a course's settings** (for example turn interactive browser exercises on or off, change the target level, the exercise mix or the flashcards) → read that course's track `setup.md` for the meaning of the option, edit `options` in its `course.json`, run `TOOL check <slug>`, create `ui.json` if interactive was just turned on (section 4, step 6), commit with `learn(<slug>): settings — <what changed>`.
3. **Change the conversation language** → `TOOL settings --lang <tag> --lang-name "<name>"`, translate `my-learning/ui.json` again if it exists, commit both with message `learn: settings — language <tag>`. Existing files stay in their language; new files use the new one. For language courses, also ask whether `source_language` should change.
4. **Back up or move to another computer** → section 7.
5. **Update the engine** (new versions of these instructions) → section 8.
6. **Continue learning** → hand over to the `learn` skill (no course: it shows the overview).

## 7. Backup and moving between computers

The workspace `my-learning/` is its own git repository; the public engine repository never contains it. A backup is a **private** remote repository for `my-learning/` only. Explain in one line why private: the files describe what the learner studies and how well.

Ask permission before creating any account, repository or remote. Then:
- **GitHub CLI available and signed in** (`gh auth status` succeeds): with a yes, `gh repo create <name> --private --source my-learning --remote origin --push` (name suggestion: `my-learning`).
- **Otherwise**: ask the learner to create an empty private repository on GitHub, GitLab or any git host (step by step, in plain words: "New repository → name → Private → Create, do not add a README"), and to paste its URL. Then `git -C my-learning remote add origin <url>` and `git -C my-learning push -u origin main`. If a sign-in window appears, the learner completes it; never type passwords or tokens yourself.
- **Restore on another computer**: clone the engine (README), then inside the engine folder `git clone <private-url> my-learning`. Run `TOOL doctor` to confirm.

From now on every session pulls and pushes this remote (see the `learn` skill).

## 8. Updating the engine

1. Check that the engine has no local edits: `git status --porcelain` at the root must print nothing (`my-learning/` is ignored, so it never shows up).
2. `git pull --ff-only`. If it fails, explain in plain words and stop; never discard local changes, never force anything.
3. Run `TOOL check <slug>` for every course and report the result. If a newer engine changed a file format, fix the course files (the check output says what) and commit them in `my-learning`.

## Rules

- One decision per message where possible; always offer numbered options and a sensible default.
- Everything learner-facing is in the conversation language; instructions in this repository stay in English.
- Never store personal data beyond what learning needs (no real names, emails or birth dates in the workspace unless the learner explicitly asks).
- Never install software, create accounts or repositories, or change settings outside this repository without a clear yes in chat.
