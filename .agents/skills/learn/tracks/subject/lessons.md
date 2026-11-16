# Subject track: lessons and tasks

How to write a step and design tasks for subject courses. The container (session folder, task block, review block, hint ladder) is defined in `../../references/session-files.md`; this file adds what is specific to subjects.

## Task catalog

IDs are stored in `options.exercise_types`. Use only the chosen ones (plus cards review when `options.cards` is true).

| id | what the learner does | kind of check |
|---|---|---|
| `worked-problem` | finish a partly solved problem (faded example) | application |
| `problem` | solve a problem from scratch, showing key steps and units | application |
| `estimation` | an order-of-magnitude estimate with stated assumptions (Fermi problem) | application |
| `explain` | explain a concept in their own words to a 12-year-old or a colleague | explanation |
| `why-what-if` | predict what changes when a condition changes, and why | explanation |
| `spot-the-error` | find the mistake in a solution, an argument or a claim | explanation |
| `compare` | compare two concepts, events, methods or positions | explanation |
| `source-analysis` | read a short source or data excerpt and answer: who, why, how reliable | explanation |
| `argued-answer` | a short answer with a claim, evidence and a counterargument (100–250 words) | explanation |
| `case` | decide in a realistic situation and justify the decision | application |
| `apply-framework` | apply a named method or framework to given data | application |
| `concept-map` | list how 5–8 concepts relate (as a nested list or table) | explanation |
| `exam-format` | an item in the exact format of the learner's exam, optionally timed | mixed |
| `practice-plan` | follow a short plan between sessions and report what happened | self-report |
| `flashcards` | due cards from `cards.md` | recall |

## Structure of a study step

Headings in the learner's language. Skip sections that would be empty.

1. **Where you meet this**: a concrete situation or question that this topic answers (why the sky is blue, why a project slipped, why a war started).
2. **Intuition**: the idea without formalism, an analogy if it helps.
3. **Precise version**: definitions, the formula with the meaning of each symbol and its units, or the established account with its key evidence.
4. **Worked examples**: two or three, increasing in difficulty, every step explained; one shows a common wrong approach and why it fails.
5. **Misconceptions**: the well-known ones for this topic, each with a quick test that exposes it.
6. **Different views** (conceptual subjects): the main positions and who holds them, when experts disagree.
7. **Cheat sheet**: 3–6 bullets (key formulas, definitions, dates).
8. **Sources**: the textbook sections or references used.

Then 2–4 tasks: at least one explanation-type and one application-type task.

## Writing problems and answers

- State all given data, units and the required precision ("give the answer in m/s, two significant figures").
- For multi-step problems, ask for the key steps in `lesson.md` (or `practice.md` for long derivations), not only the final number.
- Formulas in plain text or Unicode by default (`F = m·a`, `v₀`, `x²`); LaTeX only if the learner's preview renders it (see `session-files.md`).
- Solve every problem yourself before handing it out and recompute numbers with a tool when one is available (`python -c "print(9.81*2.5**2/2)"`). Check units and orders of magnitude.

## Checking answers

- Judge the reasoning, not only the result: a correct number from a wrong method is `◐ partial` and the method error is a gap; a right method with an arithmetic slip is a slip (confirm with the learner).
- For explanations, check three things: correct, complete enough for the level, in their own words (not a recited definition).
- For argued answers and source analysis, use a short rubric: claim, evidence, reasoning, counterargument, each 0–2.
- For practice-plan reports, ask one or two specific follow-up questions and adjust the plan; record what the learner reports, never claim to have verified a physical skill.

## Interactive exercises (opt-in: only when `options.interactive` is true)

Closed-format items go into the browser player (`../../references/interactive.md`): `flashcards` and term recall as `flashcard` / 4-option `choice` items, misconception probes and `exam-format` multiple choice as `choice`, fill-in-the-term as `gap`, process steps or timelines as `order`. A numeric answer fits a `gap` only when the format is fixed (state units and rounding in the prompt and list every accepted spelling, e.g. `9.8`, `9.80`). Problems with steps, explanations, argued answers and cases stay in `lesson.md` / `practice.md`.

## Mode specifics

- **study**: one new topic per step: explanation, worked examples, 2–4 tasks.
- **practice**: 3–5 mixed tasks on `learning`/`shaky` topics, interleaved (different topics in one set), plus due cards.
- **review**: recall questions first (no notes), then one application task per due topic.
- **test**: 10–15 items in the exam's style when there is an exam, otherwise mixed; for timed exams, state the time and ask the learner to keep to it.
