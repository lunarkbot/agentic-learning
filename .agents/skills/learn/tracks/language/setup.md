# Language track: course setup

Used by the `start` skill (or by `learn` for an unknown course) after the learner chose to study a foreign language. Ask in the conversation language, in two or three short chat messages, never one long form. Offer choices as numbered lists so the learner can answer with digits ("1, 3, 5").

## Questions

1. **Which language, and which variant?** Accept free text ("English", "американский английский", "Spanish for Mexico"). Always pin the variant:
   - If the learner named it (`English US`, `Brazilian Portuguese`), use it: `en-US`, `pt-BR`.
   - If not, offer the common variants with one line each and a recommendation based on their goal (moving to Canada → `en-CA` or `fr-CA`; working with US companies → `en-US`; most textbooks and exams in Europe → `en-GB`).
   - For languages with several scripts, also pin the script (`zh-Hans` vs `zh-Hant`, `sr-Latn` vs `sr-Cyrl`, Japanese: kana from the start or romaji first).
2. **Why?** Pick any: work and meetings, an exam (IELTS, TOEFL, Cambridge, DELE, Goethe, DELF, JLPT, HSK...), moving abroad, travel, reading books and media, family, fun. The goal shapes vocabulary and register.
3. **Target level.** A1–C2 with one plain line each (A2: everyday situations in simple sentences; B1: independent in familiar topics; B2: fluent work conversations and texts; C1: complex professional and academic use; C2: near-native precision). For an exam goal, use the level the exam requires. If unsure, recommend B2 for work, B1 for travel and living.
4. **Exercise mix.** Show the catalog from `lessons.md` as a numbered list with one line each, preselect a mix that fits the goal, and let the learner add or remove. Always keep at least one controlled and one production type, and say why in one line. The list ends with one more item, preselected: **interactive drills in the browser** (flashcards with 4 options or flip-and-grade, choose the preposition or article, type the ending or verb form, put the words in order, clickable tests, a 🔊 button to hear the correct sentence after answering). If the learner unticks it, set `options.interactive` to `false`; otherwise it stays `true`.
5. **Translation direction**, if translation is in the mix: from their language into the target language (`to-target`, builds production), from the target language into theirs (`from-target`, builds comprehension), or `both` (default).
6. **Explanations**: `auto` (default; switches to the target language as the level grows), `native`, `target`. One line on each.
7. **Flashcards**: on by default (words and phrases from lessons go into `cards.md` with spaced review). Off if they already use Anki or another app; offer to keep `cards.md` exportable as a simple table.

Mention the limits of text-only listening and speaking practice in one or two lines (see `TRACK.md`) and the workarounds; ask whether they want those workarounds in the mix.

Do not ask about the current level: the placement test measures it.

## Options written to `course.json`

| key | value |
|---|---|
| `target_language` | BCP 47 tag with region or script: `en-US`, `es-MX`, `pt-BR`, `zh-Hans` |
| `target_language_name` | English name, e.g. "English (United States)" |
| `source_language` | tag, usually the conversation language from `settings.json` |
| `target_level` | `A1` … `C2` |
| `goals` | short strings, e.g. `["work meetings", "IELTS 7.0"]` |
| `exercise_types` | IDs from the catalog in `lessons.md` |
| `translation_direction` | `to-target`, `from-target`, `both` |
| `explanations` | `auto`, `native`, `target` |
| `script` | only when relevant, e.g. `kana`, `Latn`; empty otherwise |
| `cards` | `true` / `false` |
| `interactive` | `true` (default) / `false`: browser drills, the last item of the exercise mix (`../../references/interactive.md`) |
| `answer_channel` | `files` (default) or `chat` |

Suggested slug: the tag in lowercase, e.g. `en-us`, `es-mx`, `de-de`; title in the learner's language ("Английский (США)"). Then hand over to the placement test (`diagnostic.md`).
