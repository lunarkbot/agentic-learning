# Subject track: course setup

Used by the `start` skill (or by `learn` for an unknown course) after the learner chose "something else". The aim is to understand the subject and the learner's real need, then propose a fitting format. Ask in the conversation language, in two or three short messages; offer numbered choices.

## 0. Route first

If the subject is really programming (any language, framework, DevOps, databases) or a human language, say so in one line and switch to that track's `setup.md`: those tracks are more specialized and will teach it better. Data science and math for ML: `subject` with `kind: quantitative` unless the learner wants coding practice, then `programming`.

## 1. Clarify the subject

1. **What exactly?** Free text. If it is broad ("physics", "history"), narrow it with 3–5 options: a curriculum (school physics, AP Physics 1, first-year mechanics), a period or region (history), a specific certification (PMP).
2. **Why?** An exam (which one and when), school or university course support, a job, a hobby, curiosity, helping a child with homework. Note any deadline: it shapes the pace.
3. **Kind** (`TRACK.md`): propose the kind that fits and confirm in one line.
4. **Level scale and target**: propose the scale from `TRACK.md` that fits and ask for the target on it (for an exam: the exam itself, plus a target score if there is one).

## 2. Propose a format

Based on the kind and the goal, propose a mix of task types from the catalog in `lessons.md` (show 4–6 relevant ones as a numbered list, preselect the recommended ones, one line each). Examples of sensible defaults:
- quantitative: worked problems, multi-step problems, estimation, explain-the-concept, spot-the-error;
- conceptual: explain in your own words, compare and contrast, source analysis, short argued answer, timeline or concept map;
- professional: case decisions, apply-the-framework, critique a document, scenario questions;
- exam: the exam's own task formats under time limits, plus error analysis;
- practical: theory questions, a weekly practice plan with self-report, analyze-an-example (a photo, a chess position, a score).

Also ask:
- **Cards** for terms, formulas, dates: on or off (default on for `conceptual` and `exam`, off otherwise).
- **Tools** the learner has or wants (calculator allowed or not, graph paper, a chessboard, a camera, a DAW). Store in `options.tools`.

Add one more item to the proposed task list, **not** preselected: **interactive drills in the browser** (flashcards for terms, formulas and dates, multiple choice, fill in the term, put steps or events in order, with instant feedback). If the learner ticks it, set `options.interactive` to `true`; otherwise it stays `false`.

For `practical` subjects and any subject with physical risk, say the limits and safety rules from `TRACK.md` in one or two lines.

## Options written to `course.json`

| key | value |
|---|---|
| `subject` | human name, narrowed: "Physics: mechanics (AP Physics 1)" |
| `kind` | `quantitative`, `conceptual`, `professional`, `exam`, `practical` |
| `goals` | short strings, including a deadline if any: `["AP exam 2027-05"]` |
| `level_scale` | the scale in words: "high school → AP" or "beginner/intermediate/advanced" |
| `target_level` | a value on that scale |
| `exercise_types` | IDs from the catalog in `lessons.md` |
| `tools` | short strings |
| `cards` | `true` / `false` |
| `safety_notes` | empty, or one line of what to avoid |
| `interactive` | `false` (default) / `true`: browser drills (`../../references/interactive.md`) |
| `answer_channel` | `files` (default) or `chat` |

Slug: short and descriptive (`physics-mechanics`, `pmp`, `music-theory`); title in the learner's language. Then hand over to the diagnostic (`diagnostic.md`).
