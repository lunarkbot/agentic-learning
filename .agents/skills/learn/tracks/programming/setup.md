# Programming track: course setup

Used by the `start` skill (or by `learn` for an unknown course) after the learner chose to study a programming topic. Ask in the conversation language, in one or two short chat messages, never as a long form. Offer choices as a numbered list so the learner can answer with digits.

## Questions

1. **What exactly?** Any language, framework or discipline. If the learner is unsure, offer the catalog in `TRACK.md` grouped (languages / frontend / backend and data / infrastructure); anything outside it is equally welcome (see "Any other technology" below). Resolve aliases (`ts` → `js-ts`).
2. **Target level.** `junior`, `mid`, `senior` (default), `staff`, with the one-line meaning from `TRACK.md`. If the learner says "I just want to get started", that is `junior`.
3. **Goal.** Pick any: interviews, a specific project or job, closing gaps, system-level depth, switching stacks, curiosity. Free text is fine.
4. **Include / skip.** Anything they definitely want or do not want (e.g. "no frontend frameworks", "include plain JS", "focus on testing"). Optional.
5. **Stack**, only for `backend`, `frontend`, `devops`: which language and frameworks the examples use (e.g. TypeScript + Node + PostgreSQL). Offer two or three sensible defaults.
6. **Clickable quizzes** (off by default): mention in one line that quick checks and tests can also run in the browser with instant feedback, and that by default everything stays in files, because code is best written and read in the editor. Turn it on only if the learner wants it.

Do not ask about the experience level here: the diagnostic measures it.

## Any other technology

For a technology that is not in the catalog (or a catalog entry the table in `lessons.md` does not cover), pin these before the diagnostic, so every later session behaves the same:

1. **Scope**: one line of what the course covers (like the catalog's "scope" column), confirmed with the learner. Store it in `options.scope`.
2. **Version**: the current stable version from the official site (verify with web search when available), and the version the learner uses at work if it differs (legacy systems often run old versions: teach that version and mention what changed later). Store it in `options.version`.
3. **Sources**: the official documentation and style guide; for very niche technologies, say honestly that material is scarce and that you may be less certain, and verify more.
4. **Practice file and run command**: the file (`practice.ex`, `practice.zig`, `practice.hs`, `practice.php`, a project folder) and the exact command (`elixir practice.ex`, `zig run practice.zig`, `runghc practice.hs`, `php practice.php`). Store them in `options.practice_file` and `options.run_command`. If the comment syntax is unusual, pass `--comment` to `learn_tool.py session`.
5. **Smoke test**: write a three-line hello-world practice file in a scratch folder, run it with the stored command, and confirm the output before the diagnostic. If the toolchain cannot run on this machine (mainframe, licensed IDE, hardware), agree on a fallback: code reading, "what does this print", review tasks, plus running on the learner's own environment and pasting the output into the practice file.

## Toolchain check

Before the diagnostic, check what is installed for this course (`node --version`, `go version`, `python --version`, `rustc --version`, `docker --version`, ...). If the toolchain is missing:
- Say what is missing and that hands-on tasks need it.
- Offer to install it with the official installer or the OS package manager (`winget`, `brew`, `apt`), and do it only after the learner says yes.
- Without it, the course still works (questions, code reading), but tell the learner which tasks are not possible.

Detect the package manager from the learner's habits only when relevant (Node: ask once, `npm`, `pnpm` or `yarn`; default `npm` because it ships with Node). Store it in `options.package_manager`.

## Options written to `course.json`

| key | value |
|---|---|
| `technology` | human name, e.g. "Go", "TypeScript", "Backend (Node + PostgreSQL)" |
| `target_level` | `junior` / `mid` / `senior` / `staff` |
| `goals` | short strings |
| `include`, `exclude` | short strings |
| `stack` | for `backend`, `frontend`, `devops`; empty otherwise |
| `package_manager` | when the ecosystem has several; empty otherwise |
| `scope` | one line; required for technologies outside the catalog |
| `version` | the version taught, e.g. "Elixir 1.18"; empty = current stable |
| `practice_file` | e.g. `practice.ex`, or `project` for a scaffolded project; empty = the table in `lessons.md` |
| `run_command` | e.g. `elixir practice.ex`; empty = the table in `lessons.md` |
| `interactive` | `false` (default): everything in files; `true` if the learner wants quick checks and tests as clickable quizzes in the browser |
| `answer_channel` | `files` (default) or `chat` (only if the learner has no editor and asked for it) |

The course title (`--title`) is the human name in the learner's language. Then hand over to the diagnostic (`diagnostic.md`).
