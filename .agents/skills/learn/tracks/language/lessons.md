# Language track: lessons and exercises

How to write a step and design exercises for language courses. The container (session folder, task block, review block, hint ladder) is defined in `../../references/session-files.md`; this file adds what is specific to languages.

All target-language material follows `options.target_language` and its variant (see "Variant fidelity" in `TRACK.md`). Instructions follow `options.explanations`.

## Exercise catalog

IDs are stored in `options.exercise_types`. Offer them in setup; use only the chosen ones, plus cards review when `options.cards` is true.

| id | what the learner does | kind |
|---|---|---|
| `grammar` | gap fill, choose the form, transform a sentence (active → passive, direct → reported) | controlled |
| `error-correction` | find and fix the mistakes in sentences or a short text | controlled |
| `vocabulary` | match, collocations ("make or do?"), word formation, synonyms by register | controlled |
| `reading` | a short authentic-style text with comprehension and "what does X mean here" questions | input |
| `listening-tts` | a dialogue the learner plays with a text-to-speech tool before reading it, then answers questions | input |
| `writing` | a short text with a clear prompt: an email, a message, a review, an opinion, a story | production |
| `translation-to-target` | translate sentences or a short passage from the source language into the target language | production |
| `translation-from-target` | translate from the target language into the source language, keeping tone and idiom | input/production |
| `rewrite-register` | rewrite a text more formally or more casually, or for another audience | production |
| `dialogue` | write your lines in a scripted situation (a meeting, a complaint, a job interview) | production |
| `speaking-transcript` | answer a prompt aloud, transcribe with a speech-to-text tool, submit the transcript | production |
| `exam-tasks` | task formats of the learner's exam (IELTS Writing Task 2, DELE, Goethe, ...) | mixed |

## Interactive exercises (on by default; skipped when `options.interactive` is false)

The prebuilt browser player (`../../references/interactive.md`) takes over the closed-format work; you write only `exercises.json`, with `"lang"` set to `options.target_language` so the 🔊 voice and the input language match the variant. Put the full correct sentence in `say` (heard after answering); use `audio` only for real listening items whose answer is not simply the recording read back (see the `say` and `audio` rules in `interactive.md`).

| catalog type | player item |
|---|---|
| `vocabulary`, cards review | `choice` with `card` set (word → 4 options; mix directions), or `flashcard` (flip and self-grade) for due cards |
| `grammar` (prepositions, articles, auxiliaries) | `choice`, or `gap` with `options` (dropdown) |
| `grammar` (verb forms, endings, cases, agreement) | `gap` with typed answers and every valid form in `accept` |
| word order, question formation | `order` |
| `error-correction` (spot the wrong word) | `choice` ("Which part is wrong?") |
| `reading`, `listening-tts` comprehension questions | `choice`; the text itself stays in `lesson.md` (or in `say` for listening) |
| `test` mode, closed items | `exam` mode set |

`writing`, translation, `rewrite-register`, `dialogue` and `speaking-transcript` stay in `lesson.md` / `practice.md`: they need open answers and a real review. A typical study step: explanation in `lesson.md` → a drill of 6–10 items in the player → one production task in the file.

Distractors for language items come from real errors of speakers of `options.source_language` (calques, false friends, wrong preposition) and must be wrong in the chosen variant: for `en-US`, *gotten* is not a distractor.

## Structure of a study step

Headings in the explanation language. Skip sections that would be empty.

1. **Where you need it**: one realistic situation (a message to a colleague, an order in a café) where this topic matters, 2–3 sentences.
2. **The rule in plain words**: form and meaning, with a mini table of forms when there are any. Define every grammatical term at first use, or avoid it at low levels.
3. **Examples in context**: 4–6 sentences or a short dialogue in the target language, each with the translation (A1–B1) or a gloss for hard words (B2+). Mark the key form in **bold**.
4. **Contrast**: with the learner's first language or with a confusable structure ("Present Perfect vs Past Simple"), as a ✘/✔ pair table.
5. **How people really say it**: register (formal, neutral, casual), frequency, regional notes for the chosen variant, what sounds "textbook". Name the source when you claim it.
6. **Typical mistakes**: the 2–4 most likely errors for this learner, with the correction.
7. **Cheat sheet**: 3–6 bullets.
8. **New words**: the words from this step that go into `cards.md` (word, meaning, one example).
9. **Sources**: dictionary or grammar references used.

Then 2–4 tasks moving from controlled to production, e.g. a gap fill, an error correction, then 3–5 sentences of their own or a short translation using the structure.

## Writing tasks

- **Prompt**: situation, audience, purpose, and what must be included (3 bullet points), plus the word range for the level (A2: 40–60, B1: 80–120, B2: 150–200, C1: 220–280). Long texts go into `practice.md`; short ones under `**Answer:**`.
- **Example**: show the expected *format* (greeting, paragraphs) or a model answer of a *different* prompt, never of the same one.
- **Review**:
  1. A score per criterion on a 0–5 scale: task achievement, coherence and organization, vocabulary range, grammatical accuracy (plus the official band descriptors when `exam-tasks` is in the mix and you can verify them; otherwise say the score is an estimate).
  2. The learner's text with corrections marked inline: `~~wrong~~ **right**` and a short tag in brackets for the error type: `[grammar]`, `[word choice]`, `[spelling]`, `[word order]`, `[register]`, `[variant]`, `[punctuation]`.
  3. A short list of the error *patterns* (not every typo) with the rule behind each.
  4. An improved version of the whole text at the learner's level + one step up, so they see the next level, not a native-speaker rewrite they cannot reach.
  5. 3–5 words or phrases worth stealing, added to `cards.md`.

## Translation tasks

- Direction from `options.translation_direction`. Use realistic material: messages, short news-style passages, dialogue lines; avoid sentences that only test one word.
- State what to preserve: meaning first, then tone and register; literal translation is not the goal unless the task says so.
- Review: accept every correct variant (there is rarely one right translation); mark meaning errors separately from naturalness issues ("correct, but a native speaker would say ..."). Show one or two natural reference translations.

## Checking answers

- Nothing is "run" in this track, so read every answer carefully twice. Distinguish an error from an acceptable alternative: if a form is correct in another context or variant, say so.
- For each wrong answer, give the correct form and the reason in one line; for patterns, point to the rule in the step.
- A spelling slip in an otherwise right answer is a slip, not a grammar gap; ask only when unsure.
- When you are not sure whether a phrase is natural in the chosen variant, say so and suggest checking it in the dictionary from the sources; never fake certainty.

## Cards review

When `options.cards` is true, every `review` and `practice` session includes a short block of due cards from `learn_tool.py due` (10–20 cards): in the player as a flashcard deck when `options.interactive` is true (`shuffle_items: true`, a mix of `flashcard` and 4-option `choice` items, both directions), otherwise in `lesson.md` (front → back, and some back → front). Update `cards.md` per the flashcard rules in `../../references/progress-rules.md`. Add new cards from each study step (5–15 at most per session).

## Mode specifics

- **study**: one new topic per step, explanation + 2–4 tasks from controlled to production.
- **practice**: 3–5 tasks across `learning`/`shaky` topics using the chosen exercise types, at least one production task, plus the cards block.
- **review**: due topics in new contexts (a different text, a different situation), plus the cards block.
- **test**: 15–20 items on covered topics: mostly controlled items for breadth, one short production task for depth. In the review, confirm slips with the learner before counting them.
