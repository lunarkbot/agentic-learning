# Track: any other subject

Everything that is neither programming nor a foreign language: school and university subjects (physics, math, chemistry, history, economics), professional knowledge (accounting, project management, UX research, law basics), exam preparation, and practical skills taught through knowledge (music theory, photography, chess, cooking, first aid theory). Read this file only when the course's `course.json` has `"track": "subject"`. Do not read the other tracks.

This track is deliberately generic. It must never change how the programming or language tracks work; if a subject turns out to be programming or a language, move it to that track instead (see `setup.md`).

Files of this track:
- `setup.md`: clarifying the subject and choosing options.
- `diagnostic.md`: entry diagnostic and program creation.
- `lessons.md`: lesson structure, the task-type catalog, checking.

## Subject kinds

`options.kind` shapes the whole course. Pick one in setup:

| kind | examples | the core of practice |
|---|---|---|
| `quantitative` | physics, math, statistics, chemistry, economics models, finance math | solving problems with numbers and derivations |
| `conceptual` | biology, history, philosophy, law basics, psychology | explaining, comparing, arguing with evidence |
| `professional` | project management, product, accounting, UX, marketing | cases, decisions, applying frameworks to situations |
| `exam` | SAT, AP, A-levels, IB, university entrance exams, certifications (PMP, CFA L1) | the exam's own task formats and timing |
| `practical` | music theory, photography, chess, drawing, cooking, fitness theory | theory checks plus a practice plan with self-reports |

A course may combine two kinds (physics for an exam = `exam` with quantitative tasks); pick the dominant one and note the other in `goals`.

## Levels

There is no universal scale, so choose one in setup that fits the subject and store it in `options.level_scale`:
- school or exam subjects: grade or exam level (e.g. "high school", "AP Physics 1", "A-level", "first-year university");
- professional subjects: `foundation`, `practitioner`, `expert` (or the certification's own levels);
- everything else: `beginner`, `intermediate`, `advanced`.

`options.target_level` uses the same scale. The diagnostic places the learner on it.

## Teaching principles

- **Understanding first.** Every new idea is built from what the learner already knows, with an intuitive explanation, then the precise definition, then worked examples. A formula is never introduced without its meaning and units.
- **Worked examples, then faded examples.** Show a fully solved problem, then one with steps missing, then an independent problem (the "fading" technique from cognitive load research).
- **Retrieval and spacing.** Recall beats rereading: short recall questions at the start of each session, spaced review per the progress rules, cards for terms and formulas when `options.cards` is true.
- **Misconceptions are named.** Each subject has well-known misconceptions (heavier objects fall faster, correlation means causation, historical events have one cause). Address them explicitly with a test that would reveal them.
- **Sources and accuracy.** Use established references (textbooks, official curricula and exam specifications, encyclopedias with editorial review, peer-reviewed overviews). For contested topics (history, economics, social sciences), present the main positions fairly and say where experts disagree. Never invent a citation, a date, a statistic or a quote; if unsure, say so.
- **Verify computations.** Recompute every numeric answer, ideally with a tool (a Python one-liner, a calculator) when one is available. Check units and orders of magnitude.

## Safety and limits

- **Physical risk** (chemistry experiments, electricity, fitness, cooking with heat, first aid): teach theory and safe practice; never give instructions for hazardous procedures, and point to qualified supervision where a real skill needs it. Record concerns in `options.safety_notes`.
- **Medicine, law, finance, psychology**: educational content only. Say clearly that this is not personal medical, legal, financial or psychological advice, and recommend a professional for a personal situation.
- **Practical skills** (an instrument, drawing, sport): a text agent cannot see or hear the learner. Teach the theory, design a practice plan, and check through self-reports (what you practiced, what felt hard), photos or recordings only if the agent supports them. Say this honestly in setup.

## What counts as a check (for the progress rules)

"Two successful checks of different kinds" means one **explanation** check (explain in your own words, or why, or compare) plus one **application** check (a solved problem, a case decision, a correctly applied method). A correct numeric answer with wrong reasoning is not a success.
