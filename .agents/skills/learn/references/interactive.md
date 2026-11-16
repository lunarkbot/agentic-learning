# Interactive exercises (all tracks, optional)

A prebuilt browser player for exercises with clickable or short typed answers: flashcards, choose-one questions (4 options), fill-in-the-gap (type, or choose from a dropdown), and put-the-words-in-order. It is one of the standard exercise formats, switched by `options.interactive`: **on by default for the language track** (drills are its natural format), **off by default for programming and other subjects** (there the work belongs in files: code, problems, explanations). The learner can switch it either way in setup or later in the course settings.

## Why it is cheap

The player is written once and lives in the engine: `.agents/skills/learn/interactive/player.html` (logic and styles) and `ui.en.json` (interface strings). **Never write HTML, CSS or JavaScript for exercises.** Per session you write only a compact `exercises.json` (the data), and the helper builds the page, so the cost is close to writing the same tasks as Markdown. Do not warn the learner about cost; the README mentions it once. Copy a ready skeleton from `interactive/example.drill.json` or `interactive/example.exam.json`.

## What goes in the player and what does not

| use the player | keep in `lesson.md` / practice files |
|---|---|
| vocabulary and flashcards (word → 4 options, or flip-and-self-grade) | explanations (always in `lesson.md`) |
| grammar drills: prepositions, articles, verb forms, endings, word order | writing, translation of whole sentences, essays |
| quick checks after an explanation (3–8 items) | code tasks, problems with steps, "explain why" |
| multiple-choice tests (`exam` mode) | anything with several valid long answers |
| "what does this print" with fixed options (programming) | |

Mixing is normal: a step explains in `lesson.md`, then says "do the warm-up in the browser", then has a writing task in the file.

## The file: `exercises.json`

Put it in the session folder. A second set in the same session is `exercises-2.json` (results go to `results-2.json`).

Top level:

| key | meaning |
|---|---|
| `schema` | `1` |
| `title` | shown on top, in the learner's language |
| `mode` | `drill`: instant feedback, explanations, then a retry round of missed items. `exam`: no feedback, Back/Next, answers recorded for you to grade. |
| `lang` | target language tag (`en-US`, `es-MX`) for the language track: sets the speech voice and the input language. Omit for other tracks. |
| `shuffle` | shuffle options of `choice` items (default `true`) |
| `shuffle_items` | shuffle the item order (default `false`; `true` for flashcard decks) |
| `retry_wrong` | drill only: repeat missed items at the end (default `true`) |
| `items` | the list below |

Common item keys: `id` (unique), `type`, `topic` (topic ID from `program.md`), `card` (the `front` of a card in `cards.md`, to update its box), `prompt`, `explain` (shown after answering in drill), and two audio keys (language track; read aloud with the browser's speech synthesis in the `lang` voice):

- `say`: the correct full text, e.g. `"I was born in 1994."`. The 🔊 button appears **only after the learner has answered** (in the feedback, and on a flashcard after "Show answer"), because it gives the answer away. Not allowed in `exam` mode.
- `audio`: a listening prompt, playable **before** answering. Write it so that hearing it is the task, never the answer to a different question on the screen: for "I was born ___ 1994." do **not** set `audio` to the full sentence; for a listening item ("When does Dana land?") the recording is the material to understand.

Before using `audio`, ask yourself: "Could the learner answer by just listening, without the skill this item checks?" If yes, move the text to `say`.

Item types:

```json
{ "id": "p1", "type": "choice", "topic": "grammar.prepositions-time",
  "prompt": "I was born ___ 1994.", "options": ["in", "on", "at", "by"], "answer": 0,
  "explain": "Years take **in**." }

{ "id": "p2", "type": "gap", "text": "The meeting is {{1}} Monday {{2}} 9 a.m.",
  "gaps": [ { "options": ["in", "on", "at"], "accept": ["on"] },
            { "accept": ["at"], "hint": "preposition" } ] }

{ "id": "p3", "type": "order", "tokens": ["I", "have", "never", "been", "to", "Chicago", "."],
  "accept": ["I have never been to Chicago."] }

{ "id": "c1", "type": "flashcard", "card": "перенести (встречу)", "front": "перенести (встречу)",
  "back": "reschedule", "example": "Can we reschedule to Friday?", "say": "reschedule" }
```

- `choice`: 2–9 distinct options, `answer` is the 0-based index (drill only).
- `gap`: `{{1}}`, `{{2}}` ... in `text`, one entry per gap. A gap with `options` is a dropdown; without, a text field. `accept` lists **every** correct variant (drill only). Typed answers are compared ignoring case, extra spaces, curly vs straight apostrophes and final punctuation; set `"case_sensitive": true` on the item when case matters (German nouns).
- `order`: tokens in any order (the player shuffles them); punctuation as separate tokens; `accept` lists every acceptable sentence (drill only).
- `flashcard`: self-graded ("I knew it" / "I didn't know"), drill only. A choice item with `card` set is a recognition flashcard (word → 4 options).
- Text formatting in prompts, options and explanations: `**bold**`, `_italic_`, `` `code` ``, fenced code blocks with ```` ``` ````, and `\n` for a line break. Code is never formatted, so `2**3` is safe inside backticks.

`exam` mode must contain no `answer` and no `accept` (solutions stay off disk until the learner has answered); the helper refuses such a file. `drill` mode intentionally contains the answers, because instant feedback is its point.

## Writing good items

- **One unambiguous right answer** for `choice`. Distractors are plausible and come from real typical errors (for a Russian speaker: missing article, wrong preposition calque), never jokes or obviously absurd options. Double-check that no distractor is also correct in some reading or in the chosen language variant.
- **`accept` is generous**: contractions and full forms (`I've` / `I have`), variant spellings allowed by the course's variant only, both word orders if both are correct.
- 5–15 items per set; drills over 20 items get tiring. Flashcard decks: the due cards from `learn_tool.py due`, up to 20.
- Order items: 4–10 tokens; do not include tokens that make two different correct sentences unless both are in `accept`.
- Every item has a `topic` or a `card`, so results map to progress.

## Running it

0. **No Python on this machine**: offer once to install it (see the `start` skill, "Prepare the computer") and continue with step 4 if the learner declines.
1. Write `exercises.json` into the session folder and validate + build the offline page:
   `TOOL exercises <course>` (or `--file exercises-2.json`, `--session <folder>`).
   Fix every reported problem and run it again.
2. Start the helper server so answers are saved automatically, **in the background** (your shell tool's background mode, or `start`/`nohup` equivalents):
   `TOOL serve <course>`
   It opens the browser at `http://127.0.0.1:8765/` (next free port if busy; `--no-browser` to skip), saves `results.json` after every answer, accepts writes only from its own page (a per-run token), and stops by itself after 3 hours idle.
   If you cannot keep a process running, give the learner the same command to run in their terminal; it stops with Ctrl+C.
3. Hand over in chat: the link, and "send `done` when you finish". The learner can reload or close the tab: progress is kept in the browser and in `results.json`.
4. **No Python**: copy `player.html` into the session folder as `exercises.html`, replace the placeholder `__EXERCISE_DATA__` with `{"exercises": <the JSON>, "ui": <ui.en.json or my-learning/ui.json>, "meta": {"course": "<slug>", "session": "<folder>", "file": "exercises.json", "served": false}}` (escape `</` as `<\/`), and ask the learner to open the file. At the end the page offers **Download results** (save `results.json` into the session folder) and **Copy results** (paste under the `**Answer:**` line of the step in `lesson.md`).

## Interface language

The player's buttons come from `interactive/ui.en.json`. The first time a course uses the player, create `my-learning/ui.json` with the same keys translated into the conversation language (keep `{n}`, `{total}`, `{correct}` placeholders) and commit it with the workspace settings. The helper merges it automatically. When the conversation language changes, translate it again.

## Checking (`done`)

1. Read `results.json` from the session folder (or the pasted JSON in `lesson.md`). If `finished` is false, say how many items are answered and ask whether to grade now or wait.
2. **Drill**: `correct` is the first attempt, `retry_correct` the retry round. Re-judge every typed answer marked wrong: if it is actually acceptable (a valid variant you did not list), count it as correct and say so. Use the first-attempt result for progress; a success only in the retry round counts as "with hints".
3. **Exam**: `correct` is `null`; grade every response yourself, then follow the `test` mode rules (ask about slips before counting gaps).
4. Write the review into the step in `lesson.md` as usual: a short table (item, answer, verdict) and explanations only for the misses and the patterns behind them.
5. Update `progress.md` by `topic` and `cards.md` by `card` (correct → box +1, wrong → box 1, per the flashcard rules).
6. Results and generated pages are session files: never commit them.
