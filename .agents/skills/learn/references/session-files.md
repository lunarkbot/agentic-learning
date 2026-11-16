# Session files (all tracks)

How a session lives on disk, how tasks are written, and how they are reviewed. The track file (`tracks/<track>/TRACK.md`) adds *what* to teach and which task types to use; this file defines the *container*, which is the same everywhere.

## Why files and not chat

Typing a multi-line answer, code or an essay into a chat box is miserable: Enter sends the message, there is no highlighting, it is easy to lose work. So the learner reads and answers in files, in their editor, and uses the chat only for `done`, `stop` and short questions. Never ask the learner to type code, a translation, an essay or any multi-line answer in chat.

If the learner has no editor at all (some web-only agents), say so once and offer two fallbacks: (a) open the file in any text editor, Notepad/TextEdit is fine; (b) as a last resort, answer in chat one task at a time. Record the choice in the course's `options.answer_channel` only if the learner wants it permanently.

## The session folder

Every session has its own folder, `my-learning/<course>/sessions/<YYYY-MM-DD>-<slug>/`, created by `learn_tool.py session`. It is git-ignored and disposable: the learner may delete it at any time; nothing else depends on it.

Fixed file names, so nobody has to guess:
- `lesson.md`: explanation, tasks, the learner's answers, the review.
- `practice.<ext>`: hands-on work when it does not fit into `lesson.md` (code; a long essay as `practice.md`). The stem is always `practice`.
- `exercises.json` → `exercises.html` / `results.json`: interactive exercises for the browser player, when the course enables them (`references/interactive.md`). A second set is `exercises-2.json` → `results-2.json`.
- Anything else the session needs lives in the same folder (a `package.json`, a scaffolded project in a subfolder, a data file). That is how a session gets its own environment without touching the rest of the repository.

## `lesson.md` contract

- Front matter: `course`, `track`, `date`, `mode`, `topics`, `practice`, `status: open|closed`. The script writes it; you only flip `status` to `closed` at wrap-up.
- The intro block from the template is English: translate it into the learner's language before the first hand-over (keep `done` and `stop` as they are, and add the local equivalent in parentheses, e.g. `done` (или `готово`)).
- Then one to three `## Step N. <title>` sections (headings in the learner's language). Each step: explanation (when teaching), tasks, the learner's answers under `**Answer:**` (translate the label, keep it bold), and after checking a review block (`### Review`, translated).
- Earlier steps stay as they are so the learner can scroll back. A new step is appended at the end.

## Writing a task

The learner may be tired or distracted, so a task must be understood on the first read, with no guessing. Every task block (template: `templates/task.md`) has these parts, in this order, with labels in the learner's language:

1. **What to do**: one plain sentence naming the action and the place.
2. **Example**: a worked example of the expected behavior or result, with at least one edge case. It shows *what* the solution must do, never *how*. For a translation task: the format and one sample sentence done. For a problem: what the final answer looks like (units, precision).
3. **Conditions**: only constraints that matter (forbidden constructs, word count, tense to use, no calculator). Omit if there are none.
4. **Where to write**: file and section, or the `**Answer:**` line.
5. **How to check**: the exact command and what success looks like, or the answer format.

Rules:
- The learner must never have to infer the contract from a failing check or from your reaction. If a result is expected, it is in the example.
- Questions state the answer format.
- One task, one idea. The heading carries the time estimate and the topic ID: `### Task 2. <name> · ~5 min · \`topic.id\``.
- Tasks are small: 2–10 minutes each. A session should feel interesting, not like a chore.

Avoid / write instead (programming example, the principle holds for every track):

- Avoid: "Write (right in the chat) a factory `makeCounter()` returning a function that yields 1, 2, 3, ... so that the counter cannot be changed from outside. No `class`." It hides the contract, asks for typing in chat, and the real expectations only appear after a wrong attempt.
- Write: "**What to do:** finish `makeCounter` in `practice.ts`. **Example:** `next() → 1`, `next() → 2`, a second counter starts at 1 again, `next.count` is a compile error. **Conditions:** no `class`, no globals, explicit return type."

## Everything you show must be true

- Run every code example and every task before it goes into a file (programming track).
- Re-check every grammar claim, translation and example sentence; prefer examples you can trace to a reputable dictionary or corpus (language track).
- Solve every problem yourself, and recompute numbers with a tool when one is available (subject track).
- Verify version-specific or recently changed facts in official sources. If you could not verify, say so in the text. Never invent a source, a quote, a statistic or a rule.

## Solutions stay off disk

Do not write the solution into the practice file or the lesson before the learner's attempt. Keep it in your context. After the check, the full solution and reasoning go into the review block.

## Checking a step (`done`)

1. Re-read the files from disk. The learner edited them; never rely on what you wrote earlier.
2. Run whatever can be run (the track says what). Read the actual output.
3. Read every answer. An empty answer or "I don't know" is information, not a failure: explain instead of scolding. If nothing at all is filled in, say so and ask whether to continue or hint.
4. Judge each task: correct, partial, wrong, not attempted. An answer that might be a slip is clarified with one short chat question before it counts as a gap. A right result reached by luck or through a wrong idea is not a success: ask a follow-up in a different form.
5. If a task failed, use the hint ladder in chat and ask the learner to try again and send `done` again. After the second failed attempt at the same task, stop hinting: show the solution and move on.

## The review block

Append it to the step. Per task:
- Verdict: `✔ correct`, `◐ partial`, `✘ wrong`, or `– not attempted` (translated).
- What was right in the learner's work (specific), what was missing or wrong.
- The reference solution with the reasoning, and a realistic alternative if there is one.
- One line, "Remember: ..." (translated).

Chat gets one line of verdict per task and a pointer to the review; long solutions stay in the file.

## Hint ladder

1. A nudge: where to look, or a question that points the way.
2. A narrower hint: the concept, the line, the rule involved.
3. The answer with the reasoning, and what to remember next time.

Do not rush to hint; do not let the learner struggle beyond the time budget either. Record in the topic's `note` if hints were needed.

## Formatting for easy reading

- Headings per section, short paragraphs, tables for comparisons, fenced blocks with a language tag.
- Callouts as blockquotes: `> **Important:** ...`, `> **Trap:** ...` (translated).
- `✔` and `✘` mark right and wrong variants in examples.
- Keep lines in code blocks under about 80 characters so the preview does not scroll sideways.
- Math: write simple formulas in plain text or Unicode (`v = s / t`, `x²`, `√2`); use LaTeX (`$...$`) only if the learner confirmed their Markdown preview renders it.
