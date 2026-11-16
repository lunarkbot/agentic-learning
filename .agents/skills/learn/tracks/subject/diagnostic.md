# Subject track: entry diagnostic and program creation

Used once per course, when `my-learning/<course>/program.md` does not exist. Goal: place the learner on `options.level_scale` and build a program to `options.target_level`.

The diagnostic runs like any other session: questions live in a `lesson.md` with `mode: diagnostic`. Create it with `learn_tool.py session <course> diagnostic diagnostic`.

## 1. Prerequisites first

Most subjects depend on prerequisites (physics on algebra and basic trigonometry, statistics on algebra, history on reading sources). Include 3–5 prerequisite items in round 1. If they fail, the program starts with a short "foundations" stage; say so plainly and without judgement.

## 2. Adaptive quiz

- Rounds of 6–10 items, one round per step. Start around the middle of the path from the likely current level to the target; go up or down by the answers. "I don't know" is fine; say so once in the intro.
- Cover the breadth of the subject's curriculum before depth. For an exam, use the exam specification's topic list as the map and verify it is current (official site) when possible.
- Mix the kinds of checks: a concept question ("why", "what would happen if"), an application (a problem, a case), and a misconception probe for the subject's well-known misconceptions.
- Every item states its answer format (a number with units, a letter, two sentences). For problems, ask for the key steps, not only the final number, so the reasoning can be judged.
- For `practical` subjects: theory items plus a short self-description ("what can you already do, how often do you practice"); say that a real skill check would need someone to watch or listen.
- Stop when every stage of the draft program can be placed (usually 10–20 items, two rounds). Do not teach during the quiz.

## 3. Draft the program

- 4–7 stages in a learning order that respects prerequisites, 20–50 topics in total (fewer for a hobby course, the exam spec's size for an exam).
- Topic IDs: `area.topic` in English, lowercase (`kinematics.projectile-motion`, `stats.confidence-intervals`, `ww1.causes`, `pmp.risk-register`).
- For an exam with a date, add a pacing line to the program (sessions per week needed, what to cut if time runs out) and plan a mock exam stage at the end.
- Pick 2–4 authoritative sources: a standard textbook, the official curriculum or exam specification, a reputable open resource (e.g. OpenStax for many school and university subjects). Verify they exist and are current; never invent one.
- Present the outline first: placement per area, stages with topic counts, the task mix. Adjust after feedback. Create files only after confirmation.

## 4. At or above the target

Offer, as in the other tracks: **raise the target** (next level on the scale, or a harder exam/score), or **review mode** (all topics up to the current level, confirmed ones `solid`, sessions become spaced review, mixed problem sets and mock tests). Recommend one by the goal.

## 5. Create the files

1. `program.md` from `templates/program.md`, in the learner's language.
2. `progress.md`: every topic ID; `solid` only with two good answers of different kinds (explanation + application); partial → `learning`/`shaky`; untested → `todo`. `level` = the placement on the scale (short, e.g. `high-school`, `practitioner`, `intermediate`).
3. `timeline.md` with the first entry "diagnostic".
4. If `options.cards` is true: `cards.md` from `templates/cards.md`, seeded with up to 10 terms or formulas the learner missed.
5. Close the session, run `learn_tool.py sync` and `learn_tool.py check`, then commit.
