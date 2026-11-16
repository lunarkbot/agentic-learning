# Progress rules (all tracks)

`progress.md` is the agent's working memory of the learner's knowledge. It must stay small, current, and honest. Row format: `id | status | since | reviewed | reviews | note`. These rules are the same for every track; a track may only add *what counts as a check* (see its `TRACK.md`).

## Fields

- `status`: `todo | learning | shaky | solid`.
- `since`: date the topic became `solid` (`YYYY-MM-DD`), otherwise `-`.
- `reviewed`: date of the last successful review or check that confirmed `solid`, otherwise `-`.
- `reviews`: number of successful spaced reviews since the topic became `solid`.
- `note`: at most one short line (80 characters), only what changes how you teach: the specific gap, a confusion pattern, a useful analogy. No dates, no history, no pipes.

## Statuses

| status | meaning | next action |
|---|---|---|
| `todo` | unknown or never covered | explain first, do not quiz |
| `learning` | explained, not yet confirmed | check understanding, then promote or demote |
| `shaky` | checked, with gaps | re-explain the gap, then fresh practice |
| `solid` | confirmed; `since` holds the date it became solid | spaced review only |

## Transitions

| from | event | to |
|---|---|---|
| `todo` | explained in a session | `learning` |
| `learning` | two successful checks of different kinds, hints not needed | `solid`: `since` = today, `reviewed` = today, `reviews` = 0 |
| `learning` | a check failed or needed heavy hints | `shaky` with a note on the gap |
| `shaky` | re-explained, then one clean success on a fresh task (not the same one that failed) | `solid` as above |
| `solid` | review passed | stays, `reviews` +1, `reviewed` = today |
| `solid` | review failed (confirmed gap) | `shaky`, `reviews` = 0, `since` = `-`, `reviewed` = `-` |
| any | placed by the entry diagnostic | `solid` only with at least two good answers, one of them a "why" or production-type answer |

"Different kinds" of checks depend on the track: a conceptual question and a code task (programming); a recognition exercise and a production exercise such as writing or translation (language); a conceptual explanation and a solved problem (subject).

Rules of judgement:
- A slip the learner confirms as typo, mis-click or misreading is not a failure.
- A single lucky answer is not a success. If in doubt, ask a follow-up in another form before promoting.
- Success with hints counts as a half step: keep the status, note what needed help.
- Never promote because the learner is tired of a topic or asks for it.

## Spaced review

A `solid` topic is due when `reviewed` (or `since` if `reviewed` is `-`) plus the interval is today or earlier:

| successful reviews so far | interval |
|---|---|
| 0 | 14 days |
| 1 | 30 days |
| 2 | 90 days |
| 3 or more | 180 days |

`shaky` topics are always due. `learn_tool.py due <course>` prints both lists (and due flashcards); use it instead of computing dates by hand. For `solid` topics that are due, prefer questions on nuances and edge cases over the basics: the aim is to refresh, not to re-teach.

## Flashcards (`cards.md`, optional)

Topics are too coarse for individual words, phrases, formulas or dates, so those live in `<course>/cards.md` (template: `templates/cards.md`), a Leitner system. The language track uses it by default; other tracks only when the learner wants it.

- Add a card when an item was taught or when the learner got it wrong and it is worth keeping. Typical session: 5–15 new cards at most. Do not dump whole word lists.
- `front` is what the learner sees (in the language they recall *from*), `back` is the answer, `example` is one short realistic usage.
- New card: `box` = 1, `next` = tomorrow.
- Recalled correctly in a review: `box` +1 (max 5), `next` = today + interval of the new box.
- Not recalled: `box` = 1, `next` = tomorrow.

| box | interval |
|---|---|
| 1 | 1 day |
| 2 | 3 days |
| 3 | 7 days |
| 4 | 21 days |
| 5 | 60 days |

Review due cards in `review` and `practice` sessions as a short block (10–20 cards), in both directions where it makes sense. Cards in box 5 that pass again stay in box 5.

## Hygiene

Every session:
- Update rows in place; one row per topic ID in `program.md`, no extra rows, no duplicates.
- Shorten or delete notes that are no longer true. Clear the note on promotion to `solid` unless it is a durable insight.
- Keep `next_up` at five IDs or fewer, in teaching order.
- Do not log session history here; `timeline.md` and git hold it.

Every fifth session (when `sessions` is divisible by five) do a full review:
- Run `learn_tool.py check`, fix every report.
- Re-read all notes and the whole table once: remove stale statements, fix statuses that contradict the timeline, check that the program still matches reality (topics added or merged during the course, renamed IDs updated in both files).
- Set `last_full_review` to today.
