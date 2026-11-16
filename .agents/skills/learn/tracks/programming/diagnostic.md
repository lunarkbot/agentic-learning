# Programming track: entry diagnostic and program creation

Used once per course, when `my-learning/<course>/program.md` does not exist. Goal: measure the real level quickly and build a personal program from that level to `options.target_level` in this technology.

The diagnostic runs like any other session: its questions live in a `lesson.md` with `mode: diagnostic`, and the learner answers in the file. Create it with `learn_tool.py session <course> diagnostic diagnostic`.

## 1. Context (one short chat message)

If setup did not already cover it, ask briefly:
- Hands-on experience with this technology: where and how much (commercial work, pet projects, only read about it, none).
- Anything from `options.goals` that needs a clarification.

If the learner says they have never written code at all, do not run a quiz: say so, place everything at `todo`, set `level: beginner`, and build the program from the ground up (stage 1 = setting up the environment and first programs).

## 2. Adaptive quiz

- Ask in rounds of 5–8 questions. Each round is one step in `lesson.md`; the learner answers under each question and sends `done`. Start one level below the target, then go up when answers are confident and down when they are not. "I don't know" is allowed and useful data; say so once in the file's intro.
- Cover the breadth of the course scope (see the catalog in `TRACK.md` or the learner's description) before going deep on one area: language or platform basics, idioms and style, tooling, testing, concurrency/async or state (as applicable), performance, architecture, operational concerns.
- Mix formats: a conceptual "why", a short code reading ("what happens here"), a "what is wrong here", a trade-off question. Every question states its answer format (a letter, a number, one or two sentences). Code follows the rules in `TRACK.md` (TypeScript for JS).
- Mark each probed area internally as clearly known, partially known, or unknown. Stop when you can place every stage of the draft program (usually 10–20 questions, two or three rounds). The learner can say "enough" at any time; then work with what you have and mark the rest `todo`.
- Do not teach during the quiz. Note gaps; teaching starts in the first study session. A brief correction only if the learner explicitly asks.

## 3. Draft the program

- The end point is `options.target_level` (see `TRACK.md`). For `senior`: idiomatic code, knows the standard tooling, understands the trade-offs and internals that matter in production, can review others' code and design components.
- 4–7 stages in a sensible learning order, about 25–60 topics in total (fewer for `junior`). Topics the diagnostic showed as solid stay in the program (it describes the whole path) but start as `solid`.
- Topic = something one can learn and check in one sitting. IDs: `area.topic`, lowercase, `[a-z0-9.-]`, in English (they are identifiers, not text).
- Pick 2–4 authoritative sources (official docs, style guide, well-known engineering guides) and verify they are current with web search or docs when available.
- Present the outline first: stage titles, topic counts, which areas start as known, what the program emphasizes. Adjust after feedback. Create files only after confirmation.

## 4. Create the files

1. `program.md` from `templates/program.md`, in the learner's language.
2. `progress.md` from `templates/progress.md`: every topic ID, status from the diagnostic: clearly known with at least two good answers (one of them a "why" or trade-off answer) → `solid` with `since` = today; partially known → `shaky` or `learning`; unknown → `todo`. Set `level` (`beginner`, `junior`, `junior+`, `mid`, `mid+`, `senior`), `started`, `next_up`.
3. `timeline.md` from `templates/timeline.md` with a first entry "diagnostic" (what was assessed, the starting picture in a few facts).
4. The demo project is created later, when first needed and agreed with the learner.
5. Close the diagnostic session, run `learn_tool.py sync` and `learn_tool.py check`, then commit (see the `learn` skill, wrap-up).

## 5. Already at or above the target

If the diagnostic places the learner at or above `options.target_level`, say so honestly with the evidence, and offer:
1. **Raise the target** (e.g. `senior` → `staff`) and build the program for the new target; update `options.target_level`.
2. **Maintenance mode**: build the program for the current target with most topics `solid`, so the course becomes spaced review plus deep-dive "nuance" sessions on the weakest areas.

Recommend one based on their goals (interviews → maintenance with tests; growth → raise the target).

After the files exist, continue with the originally requested mode, or propose the first study session.
