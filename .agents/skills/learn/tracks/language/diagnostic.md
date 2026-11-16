# Language track: placement test and program creation

Used once per course, when `my-learning/<course>/program.md` does not exist. Goal: estimate the CEFR level per skill quickly and build a program from that level to `options.target_level`.

The placement test runs like any other session: it lives in a `lesson.md` with `mode: diagnostic`, and the learner answers in the file. Create it with `learn_tool.py session <course> diagnostic placement --ext md` (the `practice.md` holds the writing sample).

## 1. Context (one short chat message)

If setup did not cover it: how long and how they studied the language before, whether they use it now (work, media, travel), and any certificate they hold. A learner who says "zero" gets a two-minute mini check (5 A1 items) instead of the full test; if it confirms zero, place everything at `todo`, `level: pre-A1`, and start from the alphabet/sounds stage when the script or pronunciation is new.

## 2. Adaptive placement

Write the test in rounds. Each round is one step in `lesson.md`; the learner answers under each item and sends `done`. Instructions are in the conversation language; items are in the target language and its variant. Say once in the intro that "I don't know" is fine and that guessing makes the result worse, not better.

Round 1, about 12–15 items, mixed levels A2–B2 (start lower if the context suggests A1):
- 8–10 **grammar and vocabulary** items: multiple choice or gap fill, 2 per level band, ordered by difficulty.
- 1 short **reading** text (80–150 words, around B1) with 3 questions.
- 1 **error correction** item: a sentence with one or two typical mistakes.

Round 2 adapts: go up a band where round 1 was confident, down where it was not, and probe the borderline level with 8–10 items. Include 2–3 items on the skills the learner's goal needs most (e.g. formal register for work).

Writing sample (always): a short prompt matched to the estimated level (A2: 40–60 words about yourself; B1: 80–120 words, an email; B2+: 150–200 words, an opinion with arguments) written in `practice.md`. If translation is in `options.exercise_types`, add 3 sentences to translate in the chosen direction.

Rules:
- With `options.interactive`, the grammar, vocabulary and reading-question items of each round go into an `exam`-mode `exercises.json` (no answers on disk; see `../../references/interactive.md`); the reading text, the error-correction item and the writing sample stay in the files.
- Every item states its answer format.
- Do not teach during the test. Note gaps; teaching starts in the first study session.
- The learner can say "enough" at any time; then place by what you have and say how certain the estimate is.

## 3. Estimate the level

- Estimate per skill: grammar, vocabulary range, reading, writing (and translation if tested). Use the CEFR descriptors; for writing, judge range, accuracy, coherence and task achievement.
- The overall level is the level the learner can *reliably* operate at, not the highest item they got right. Use sub-levels (`B1+`) when the picture is between levels.
- Tell the learner the result in the conversation language: overall level, per-skill picture, two or three concrete strengths, two or three concrete gaps with examples from their answers. Say that a text test cannot measure listening or speaking and that the estimate is approximate.

## 4. Level vs target

- **Below the target** (normal case): build the program from the current level to the target.
- **At or above the target**: say so with the evidence, then offer:
  1. **Raise the target** (e.g. B2 → C1) and build the program for it; update `options.target_level`.
  2. **Review mode**: a program of all levels up to and including the current one, with topics the test confirmed set to `solid` and the rest `learning`, so the course becomes spaced review, gap filling and production practice (writing, translation) to keep the level. Recommend this for "I want to keep my level" or exam refreshers.
  Record the choice in the program's goal line.

## 5. Draft the program

- One stage per CEFR band from the current level to the target (e.g. `B1 → B1+ → B2`), plus, if needed, a short stage 0 for basics the test showed as missing below the current level. 4–7 stages in total.
- Inside each stage, topics of these areas (ID prefixes, English identifiers):
  - `grammar.*`: structures (`grammar.present-perfect`, `grammar.conditionals-mixed`, `grammar.ser-estar`)
  - `vocab.*`: thematic sets and word-building (`vocab.work-meetings`, `vocab.phrasal-verbs-core`)
  - `func.*`: communicative functions (`func.polite-requests`, `func.disagreeing`)
  - `writing.*`: text types (`writing.formal-email`, `writing.opinion-essay`)
  - `reading.*`, `translation.*`, `pron.*` (rules only), `culture.*` when they serve the goal
- About 8–15 topics per stage, 30–70 in total; more and smaller topics at A1–B1, fewer but deeper at B2–C1. A topic = one sitting.
- Weight the areas by `options.goals` and `options.exercise_types` (an IELTS goal adds exam task types; a work goal adds meetings, email, small talk).
- Pick 2–4 authoritative sources for the variant: a learner's dictionary of the variant (e.g. Merriam-Webster Learner's for `en-US`), a reference grammar, the CEFR Companion Volume, an exam handbook if relevant. Verify links when possible.
- Present the outline first: estimated level, target, stages with topic counts, the exercise mix. Adjust after feedback. Create files only after confirmation.

## 6. Create the files

1. `program.md` from `templates/program.md`, in the conversation language (topic titles may quote target-language forms: `grammar.present-perfect` — Present Perfect vs Past Simple: ...).
2. `progress.md`: every topic ID; confirmed by at least two good answers of different kinds → `solid` with `since` = today; partly right → `learning` or `shaky`; untested above the level → `todo`. `level` = the overall estimate (e.g. `B1+`).
3. `timeline.md` with the first entry "placement test": the level per skill and the target, facts only.
4. If `options.cards` is true: `cards.md` from `templates/cards.md`, seeded with up to 10 words the learner missed in the test.
5. Close the session, run `learn_tool.py sync` and `learn_tool.py check`, then commit.
