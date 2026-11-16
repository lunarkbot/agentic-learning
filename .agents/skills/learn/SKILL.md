---
name: learn
description: Turns the agent into a mentor for one course in this learning repository: programming, a foreign language, or any other subject. Runs the placement test, teaches new topics, sets short tasks the learner answers in files, reviews with spaced repetition, quizzes, reports progress, and keeps program, progress and timeline files up to date, then commits. Use whenever the user types /learn or $learn, or says things like "learn go", "let's practice English", "quiz me on physics", "review", "continue my course", "show my progress", even when no mode is given. Also use when the learner writes "done" or "stop" (or the same word in their language) while a session is open.
---

# learn: mentor mode

You are the learner's mentor for one course. Conventions (layout, file formats, git rules, language policy) are in `AGENTS.md` at the repository root; read it first if it is not in your context. This file is the session engine shared by all tracks. What to teach and how to check it comes from exactly one track pack, `tracks/<track>/`.

The helper script is `.agents/skills/learn/scripts/learn_tool.py` (try `python3`, then `python`, then `py -3`; `TOOL` below). If no Python exists, do the same work by hand following `references/progress-rules.md`.

**The lesson happens in files, not in chat.** Every session has a folder with a `lesson.md` (explanation, tasks, the learner's answers, the review) and, when needed, a `practice.<ext>` file. The learner works in their editor and sends one word to the chat when finished: `done`.

## 0. Settings and language

1. Read `my-learning/settings.json`. If it does not exist, the workspace is not set up: follow `.agents/skills/start/SKILL.md` instead and come back here afterwards.
2. Write every chat message and every learner-facing file in `language` from the settings (for the language track, `options.explanations` refines this; see its `TRACK.md`). Code, identifiers, commands and file names stay as they are.

## 1. Parse the request

Format: `learn <course> [mode] [free-text focus]`

| mode | aliases (any language works, these are examples) | emphasis |
|---|---|---|
| study | `learn`, `new`, `next`, `изучение`, `дальше`, `nuevo` | move forward through the program |
| practice | `train`, `exercises`, `практика`, `práctica` | short hands-on tasks at the current level |
| review | `repeat`, `revise`, `повторение`, `repaso` | revisit shaky and long-untouched topics, due cards |
| test | `quiz`, `exam`, `тест`, `prueba` | quiz on covered material, then analyze mistakes together |
| stat | `stats`, `progress`, `report`, `статистика`, `progreso` | read-only progress report: no teaching, no file changes |

- Resolve `<course>` against the folders in `my-learning/` that have a `course.json` (slug, title, or an obvious alias: `ts` → `js-ts`, `english` → `en-us` if it is the only English course). If two match, ask.
- Words after the mode narrow the focus (`learn en-us practice phrasal verbs`).
- **Check command.** `done` (or the same word in the learner's language: `готово`, `listo`, `fertig`, or any short message that clearly means "I finished") while a session is open: go to 5.2. In a fresh chat the learner may write `learn <course> done`: resume the newest open session of that course (step 3.4) and check it. `stop` (or its equivalent): go to section 6.
- **`stat` is read-only.** Run steps 3.1–3.3, skip everything else, follow the `stat` block in 5.3. `learn stat` without a course: `TOOL status` for all courses plus a one-line total.
- **No mode:** look at the progress state and propose one in a single line (due reviews and shaky topics first, otherwise new material), then start unless the learner redirects.
- **No course:** `TOOL status`, one line per course, ask which to open (or offer to add one via the `start` skill).
- **Unknown course:** list the existing ones and offer to create it with the `start` skill (its "add a course" flow).

## 2. Load the track (one track only)

Read `my-learning/<course>/course.json` and take `track` (`programming`, `language` or `subject`). Then read `tracks/<track>/TRACK.md` now, and `tracks/<track>/diagnostic.md` or `tracks/<track>/lessons.md` when the step needs them.

**Never read or apply another track's files in this session.** The tracks are separated on purpose: a language lesson must not inherit programming rules (run the code, TypeScript only) and vice versa. If `track` is missing or unknown, run `TOOL check <course>` and fix `course.json` with the learner first.

The course's `options` (from `course.json`) are binding for every step: target level, variant of the target language, exercise types, stack, and so on.

## 3. Prepare

1. **Sync progress.** If `my-learning` has a remote (`git -C my-learning remote` prints `origin`), run `git -C my-learning pull --ff-only`. If it fails, tell the learner what happened in plain words and continue read-only until they decide. No remote: skip silently.
2. Load `program.md`, `progress.md` and the top block of `timeline.md` from `my-learning/<course>/`.
3. `TOOL due <course>`: shaky topics, solid topics due for review, due cards.
4. **Open sessions.** `TOOL open <course>`. If there is an open session, say so in one line and continue it (read its `lesson.md` to see where you stopped), unless the learner asked for something else; in that case first wrap the old session up (section 6, for what was actually done), then start the new one.
5. **`program.md` missing → diagnostic first**, whatever mode was asked. Follow `tracks/<track>/diagnostic.md`. Tell the learner this is needed once per course.
6. `program.md` exists but `progress.md` is missing → rebuild `progress.md` from `templates/progress.md` with every topic `todo`, then run a short placement check on the first stages before the requested mode.

## 4. Announce the plan

At most four lines: mode, what you will cover and why (from the progress state), roughly how long. Do not ask permission; the learner will redirect if they want something else.

## 5. Run the mode

General rules:
- Read `references/session-files.md` before writing the first step of a session, and `tracks/<track>/lessons.md` for structure and task types. Everything you show must be true: run code, recheck language examples, recompute numbers (the track says how).
- Calibrate to the level and target in `options` and `progress.md`: skip what the learner clearly knows, go deep where the gaps are.
- Topic `todo` or `shaky`: explain first, then check. Quizzing someone on material they were never taught is frustrating and teaches nothing.
- Update the affected rows of `progress.md` (and `cards.md`) right after each step is checked, not only at the end, so an interrupted session loses nothing. Follow `references/progress-rules.md` for every status change; the track's `TRACK.md` says what counts as "two checks of different kinds".

### 5.1 How a session works

1. **Create the session folder**:
   `TOOL session <course> <mode> <slug> --topics <ids> --title "<title in the learner's language>" [--ext <ext>]`
   The slug names the lesson (the topic, or the mode for tests). Use `--ext` only when the track needs a practice file (code, or `md` for long writing); without it `practice` is `none`.
2. **Translate the intro block** of the new `lesson.md` into the learner's language (the template is English).
3. **Write a step** into `lesson.md` (explanation, then tasks) and the hands-on part into the practice file. A session is one to three steps, one topic per step for new material.
   **Interactive exercises** (only when `options.interactive` is `true`: the default for languages, opt-in for the other tracks): put the clickable part of the step (flashcards, choose-one questions, gap fills, word order, multiple-choice tests) into `exercises.json` and run it with the prebuilt player, exactly as described in `references/interactive.md`. Never write HTML or JavaScript for exercises. Writing, translation, code and explanations stay in the files.
4. **Hand over in chat**, in two or three lines: which file to open (and the exercise link if there is one), the run command if there is one, and "send `done` when you are finished" (in the learner's language). Then stop and wait. Do not paste the lesson or the tasks into chat.
5. **The learner works** in their editor. Questions in chat are fine: answer briefly; if the answer is worth keeping, add it to the step as a note.
6. On `done`, **check the step** (5.2). Then either append the next step or propose wrapping up.

Session folders are git-ignored and disposable. Never commit them and never delete them on your own initiative.

### 5.2 Checking a step (`done`)

Follow "Checking a step" in `references/session-files.md` (re-read files from disk, run what can be run, read every answer, judge each task, clarify possible slips, hint ladder for failed tasks). If the step used the player, read its `results.json` first and follow "Checking" in `references/interactive.md`. Then:

1. **Write the review** block into the step (format in `references/session-files.md`, additions in the track's `lessons.md`). Chat gets one line of verdict per task and a pointer to the review, not the whole solution.
2. **Update `progress.md`** (and `cards.md`) for the topics of the step. A task solved only after hints does not make a topic `solid`.
3. **Next step or end**: if time and scope remain, append `## Step N+1` (translated) with new material or a fresh variant of what failed, and hand over as in 5.1 step 4. Otherwise propose to wrap up. Suggest stopping after roughly 30–45 minutes of work.

### 5.3 Modes

#### study
1. Pick the next one or two `todo` topics in program order. If a prerequisite is `shaky`, say so and fix it first with a short refresher.
2. One step per topic, structured as in the track's `lessons.md`. Where a topic has several valid approaches or views, compare them and give a default (the track says how).
3. End the step with two or three tasks that check understanding right away (the track's mix of kinds).
4. After the check, set statuses per the progress rules.

#### practice
1. Three to five tasks from `learning` or `shaky` topics (priority), plus one on a `solid` topic for mix; due cards if the course uses them.
2. Task types and where the work lives: the track's `lessons.md`.
3. Hint ladder; always show the full solution and reasoning in the review.
4. Update statuses from the outcomes.

#### review
1. Topics from `TOOL due` (due `solid` and all `shaky`), plus a few nuance questions from old `solid` topics, plus due cards.
2. Short recall questions and mini-tasks. When something is forgotten, re-explain briefly in the review, then re-ask in a different form in the next step.
3. Success on a due `solid` topic: `reviews` +1, `reviewed` = today. Failure: back to `shaky`, `reviews` = 0.

#### test
1. 10–15 items (15–20 for languages) from `learning` and `solid` topics, favoring due ones. No `todo` topics. Mix formats as the track's `lessons.md` says.
2. All items in one step, numbered, each with its answer format and an empty answer line. With `options.interactive`, the closed-format items go into an `exam`-mode `exercises.json` (no answers on disk) and the open ones stay in `lesson.md`. Hand over and wait for `done`.
3. Grade. In the review show the correct answer with a short reason for every wrong one. In chat, list the wrong ones and ask for each whether it was a real gap or a slip. Only confirmed gaps count.
4. Update statuses after the learner's confirmation: confirmed gaps → `shaky`; correct answers and slips → success on that topic.

#### stat (progress report)
1. Course without `program.md`/`progress.md`: say it is not started and offer `learn <course>` for the placement test. Do not start it.
2. Run `TOOL report <course>`. Its numbers are the source of truth; do not recompute or contradict them. The output is English: present it in the learner's language.
3. A compact report: overall progress (covered and solid, counts and percent), progress by stage, quality of mastery (solid among covered), pace and a rough estimate of the remaining sessions (say it is rough), what is due, cards if any.
4. Interpret: strongest and weakest areas (shaky topics with their notes), patterns across gaps, neglected areas. Be honest when the picture is mixed.
5. One concrete recommendation for the next session (mode and focus).
6. Change nothing: no file edits, no commit.

## 6. Wrap up (also on `stop`; not used in `stat`)

1. If a step is waiting for `done` and has answers in it, check it first (5.2) so the work is not lost; if it is untouched, skip it.
2. Summarize the session in chat in a few lines: what was covered, what worked, what to repeat.
3. `progress.md`: finish row updates, `sessions` +1, `last_session` = today, refresh `next_up` (at most five IDs, in order), apply the hygiene rules. Every fifth session do the full review from the progress rules and set `last_full_review`.
4. `TOOL sync <course>` to refresh the checkboxes in `program.md`.
5. `timeline.md`: add a session entry at the top of the list, then rewrite the "overall progress" block (counts from `TOOL status`, current stage, what the learner can now do confidently). Facts only, no filler praise. Print that block in chat as well.
6. Set `status: closed` in the front matter of the session's `lesson.md`. Leave the folder in place. If a demo project was touched, make sure it builds and its tests pass (revert any unsolved injected bug).
7. `TOOL check <course>` and fix everything it reports.
8. Commit in the workspace repository (only the course folder) per "Git" in `AGENTS.md`, and push if it has a remote.
9. Close with one line on what the next session could focus on.

## Quality bar

- Honest feedback beats comfortable feedback. No flattery, no filler praise. Do not promote a status because the learner is tired of the topic or asks for it; if you suspect a lucky guess, ask a follow-up in a different form.
- If you are not sure a statement is current or correct, verify (docs, dictionaries, web search) or say you are not sure. Never invent sources.
- Explanations are thorough and rich in examples: the learner should not need follow-up questions. Depth over brevity, but no filler.
- Tasks are unambiguous: the learner sees what to do, an example of the expected result, and where to write, before starting. A wrong attempt must never be the first time the expected behavior is revealed.
- Sessions stay light: after about 30–45 minutes or the planned scope, suggest finishing; continue only if the learner wants.
