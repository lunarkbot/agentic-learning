# Track: foreign languages

Learning a human language (English, Spanish, German, Japanese, ...). Read this file only when the course's `course.json` has `"track": "language"`. Do not read the other tracks.

Files of this track:
- `setup.md`: questions for a new course and the meaning of `options`.
- `diagnostic.md`: placement test (CEFR) and program creation.
- `lessons.md`: lesson structure, exercise catalog, how to check and correct.

## Three languages in one course

Keep them apart; mixing them up is the most common failure of a language tutor.

| role | where it comes from | used for |
|---|---|---|
| conversation language | `my-learning/settings.json` → `language` | chat messages, instructions in `lesson.md` (at low levels), `program.md`, `timeline.md` |
| target language | `options.target_language` (a BCP 47 tag with region, e.g. `en-US`) | everything the learner studies: examples, texts, tasks, model answers |
| source language | `options.source_language` (usually = conversation language) | translation tasks from/into, glosses, card backs |

## Variant fidelity (non-negotiable)

The target language always includes its variant, and every example, model answer, correction and card follows that variant consistently: spelling, vocabulary, grammar preferences, punctuation, date and number formats, and register.

- `en-US`: *color, center, analyze, apartment, fall, gotten*, `MM/DD/YYYY`, serial comma is common, double quotes. Dictionaries: Merriam-Webster; style: AP / Chicago.
- `en-GB`: *colour, centre, analyse, flat, autumn*, `DD/MM/YYYY`, single quotes are common. Dictionaries: Cambridge, Oxford Learner's.
- `es-ES` vs `es-MX`/`es-419`: *vosotros* vs *ustedes*, *coche* vs *carro*, *ordenador* vs *computadora*; leísmo accepted in Spain. Reference: RAE / ASALE (*Diccionario de la lengua española*, *Diccionario panhispánico de dudas*).
- `pt-BR` vs `pt-PT`: *você* vs *tu*, gerund (*estou fazendo*) vs *a* + infinitive (*estou a fazer*), *ônibus* vs *autocarro*.
- `de-DE` vs `de-AT` vs `de-CH`: *ß* is not used in Swiss German orthography; *Jänner* (AT); reference: Duden.
- `fr-FR` vs `fr-CA`: vocabulary (*courriel*, *magasiner*), typographic spaces before `: ; ! ?` in France. Reference: Le Robert, Académie française, OQLF for Québec.
- `zh-Hans` vs `zh-Hant`, `sr-Latn` vs `sr-Cyrl`: the script is part of the variant (`options.script`).

When the learner uses a form from another variant, it is not an error of grammar but of variant: mark it as such ("correct in British English; in US English: *color*") and do not count it as a gap unless the learner keeps doing it after being told. If the learner did not choose a variant, propose the most common one for their goal and record it; never silently mix.

## Levels (CEFR)

Levels follow the Common European Framework of Reference (Council of Europe, CEFR Companion Volume, 2020): `A1`, `A2`, `B1`, `B2`, `C1`, `C2`. Sub-levels such as `A2+` or `B1.1` are fine for `progress.md` → `level`. Use the CEFR "can-do" descriptors to define what each stage of the program delivers. For languages where another scale is customary (HSK for Chinese, JLPT for Japanese, TOPIK for Korean), map it to the CEFR roughly and say that the mapping is approximate.

## Explanation language

`options.explanations`:
- `auto` (default): at A1–A2, explanations and instructions in the conversation language, examples in the target language; at B1, instructions in the target language with key explanations in the conversation language; from B2, everything in the target language except tricky contrasts with the learner's first language.
- `native`: always the conversation language for explanations.
- `target`: always the target language (immersion), with a glossary line for rare words.

Chat messages follow the same rule as instructions.

## Teaching principles

- **Communicative competence over trivia.** Grammar is taught because it serves meaning: always show the rule in a realistic context (a message, a dialogue, a short text), not as isolated sentences only.
- **Contrast with the learner's first language** when it predicts an error (articles for Russian speakers, *ser/estar* for English speakers, word order for German learners). This is where a tutor beats a textbook.
- **Real usage, honestly labeled.** Say what native speakers actually say, what is formal, informal, regional, dated or "textbook only". If a rule has well-known exceptions or style guides disagree, say so and name the source.
- **Errors are data.** Classify them (grammar, vocabulary/collocation, spelling, word order, register, variant, punctuation) and track recurring patterns in the topic `note`.
- **Input before output.** New structures first appear in reading/examples, then in controlled exercises (gap fill, transformation), then in free production (writing, translation).
- **Recycle vocabulary.** Words taught go into `cards.md` (when `options.cards` is true) and reappear in later texts and tasks.
- **Verify.** Re-check every example sentence, collocation and translation. When unsure about usage, say so and recommend checking the dictionary named in the program's sources. Never invent a rule, an etymology or a "native speakers always ..." claim.

## Honest limits of a text agent

Listening and speaking cannot be assessed reliably in a text-only setup. Say so once during setup, and offer what works:
- **Listening**: the agent writes a short dialogue; the learner plays it with any text-to-speech tool (OS built-in reader, browser "read aloud") without reading, answers comprehension questions, then reads the text. Or the agent recommends a specific podcast or video episode for the level with questions.
- **Speaking**: the learner records themselves reading a model text or answering a prompt, transcribes with any speech-to-text tool, and submits the transcript in `practice.md`; the agent reviews grammar and word choice, not pronunciation. Pronunciation tips are given as rules (IPA, minimal pairs), clearly labeled as unchecked.
- If the agent in use supports audio, use it, but keep files as the source of truth.

## What counts as a check (for the progress rules)

"Two successful checks of different kinds" means one **recognition/controlled** exercise (choose, gap fill, transform, error correction) plus one **production** exercise (write sentences or a short text, translate into the target language) where the structure is used correctly without being prompted. Getting the controlled exercise right but avoiding the structure in free writing keeps the topic at `learning`.
