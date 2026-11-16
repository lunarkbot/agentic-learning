# Programming track: lessons and practice

How to write a step and design practice for programming courses. The container (session folder, task block, review block, hint ladder) is defined in `../../references/session-files.md`; this file adds what is specific to code.

## Depth

Explain thoroughly and with examples. Depth beats brevity: the learner would rather read one complete explanation than ask three follow-ups. There is no length cap on a step, but every section must earn its place: no padding, no restating the obvious, no motivational filler.

Calibrate to the status in `progress.md`:
- `todo`: assume the learner does not know the specifics of this topic, even if adjacent topics are solid. Start from the ground, define terms at first use.
- `shaky`: do not repeat the whole lesson; address the recorded gap directly, with a fresh angle and new examples.
- `learning` / review: shorter, nuance-focused.

## Structure of a study step

Use these sections in this order, skipping those that would be empty. Headings in the learner's language.

1. **Why it matters**: one concrete situation from real work where not knowing this hurts (a bug, an outage, a review comment). 2–4 sentences.
2. **The idea in plain words**: an analogy only if it genuinely helps; every new term defined at first use.
3. **Examples**: three or four, increasing in difficulty: minimal, realistic, edge case. Include one pair "don't → do". Each example has code, the result as comments (`// → 3`), and a sentence on why.
4. **How it works inside**: only when the mechanism explains the behavior (engine, runtime, compiler, protocol).
5. **Pitfalls**: typical mistakes, each with a mini example and the symptom it produces.
6. **Options and when to choose which**: strengths, costs, failure modes, the situation each fits. A table works well. End with a default recommendation and the conditions for choosing another.
7. **How real projects do it**: practice from companies and open-source codebases, non-obvious tricks, production-only pitfalls. Name the origin; label local conventions as such; a hack always comes with its cost.
8. **What a reviewer will flag**: lint rules by name where they exist.
9. **Cheat sheet**: three to six bullets.
10. **Sources**: links to official docs and the sources used.

Then two or three tasks: a mix of questions and one small code task.

## Task types

- **Find the bug**: a short snippet with one real defect (race, off-by-one, leaked resource, wrong lifetime, stale closure, misused API).
- **Predict the result**: "what does this print / return / render, and why".
- **Fix it**: a failing check or a clear symptom; the fix is a few lines.
- **Review it**: a small piece of code with two or three problems a strong reviewer would flag.
- **Make it idiomatic**: working but clumsy code; rewrite it the way the ecosystem expects.
- **Choose and justify**: two short implementations, which one and why.
- **Tiny implementation**: a function of a few lines that targets the topic. Never a whole component or module.

Give the signature or a stub in the practice file, so the learner does not spend time on boilerplate.

## Practice files and run commands

Check what is installed first (e.g. `node --version`) and write the exact command into the task. Commands must work in PowerShell and in bash: no `&&` chains, one command per line.

| course | practice file | run |
|---|---|---|
| `go` | `practice.go` (`package main`) | `go run practice.go` |
| `js-ts` | `practice.ts` | `node practice.ts` (Node 22.18+ strips types; verify the installed version), plus `npx tsc --noEmit` when type errors are the point; otherwise `npx tsx practice.ts` |
| `python` | `practice.py` | `python practice.py` (`py -3` on Windows if `python` is missing) |
| `rust` | `practice.rs` for std-only tasks; a cargo project when crates are needed | `rustc practice.rs`, then run the binary; or `cargo run` |
| `java`, `kotlin` | `practice.java` / `practice.kt` for single-file tasks; a Gradle project otherwise | `java practice.java` (source-file mode, Java 11+, the file name need not match the class); `kotlinc practice.kt -include-runtime -d practice.jar`, then `java -jar practice.jar` |
| `csharp` | a console project in the session folder | `dotnet run` |
| `react`, `vue` | a Vite project in the session folder, or `practice.tsx` for pure logic | the project's dev or test command |
| `angular` | a project in the session folder; `practice.ts` for pure TS or RxJS tasks | the project's test command |
| `css` | `practice.html` (HTML with a `<style>` block) | open in a browser |
| `sql` | `practice.sql` against SQLite (zero setup) or the learner's database | `sqlite3 practice.db ".read practice.sql"` (works in PowerShell too, unlike `<`) |
| `devops` | the artifact itself: `Dockerfile`, `practice.yaml`, `practice.sh` | the matching tool (`docker build`, a linter, ...) |
| `backend`, `frontend` | by `options.stack` | per task |
| anything else | `options.practice_file` | `options.run_command` |

The table only covers common cases. **Any technology works**: for one that is not listed (Elixir, Zig, Haskell, Swift, Dart, PHP, Solidity, ABAP, COBOL, Bash, ...), setup chose the practice file and the run command and stored them in `options.practice_file` and `options.run_command`; use those. When `options` has them, they win over the table for every course.

When a task needs a framework, a build setup or several files, scaffold the project inside the session folder (a subfolder such as `app/`), set `practice: none`, and name the files to edit in each task. Each session installs what it needs inside its own folder; pin nothing in the repository root.

## Self-check block

Put runnable checks at the bottom of the practice file under a marker such as `// ===== CHECKS (do not edit) =====` (translated). Each check prints `✔ <name>` or `✘ <name>` with expected versus actual on failure. The learner runs the file and sees the result immediately; you run the same command on `done`. Checks must not give away the solution. If the learner changed the checks, tell them and run the original ones. Typical helper for TypeScript:

```ts
function check(name: string, ok: boolean, detail = ""): void {
  console.log(`${ok ? "✔" : "✘"} ${name}${ok ? "" : ` ${detail}`}`);
}
```

Questions, find-the-bug discussions and design choices have no automated check: they are answered in `lesson.md`.

## Always verify before handing out

Run every example and every task yourself first: with the reference solution all checks are green, and with the untouched stub they fail for the intended reason. Make sure the bug is real and the example output is the actual output. If the toolchain is not available on the learner's machine, tell the learner and run what you can; do not hand out tasks you have not executed.

## Demo project

Folder: `my-learning/<course>/practice/demo-project/` (tracked in the learner's progress repository, optional). One project per course, created when you and the learner agree on a small realistic idea (a CLI tool, a small API, a small UI). It grows slowly with the course. Use it when realistic context matters more than an isolated exercise.

Requirements:
- Opens in an IDE, builds and runs with one documented command; its `README.md` states the commands.
- Has tests, so you can verify fixes quickly.
- Is small: a few files per feature. No generated output is committed.

Rules for tasks inside it:
- For a "find and fix" task, introduce one small defect and describe only the symptom. Do not point to the location.
- At the end of the session the project must build and its tests must pass. Revert any defect that remained unsolved and note it in the topic's `note` if useful.

## Interactive quizzes (opt-in: only when `options.interactive` is true)

Closed-format checks go into the browser player (`../../references/interactive.md`): "what does this print" and "which version is idiomatic / correct" as `choice` items with code in fenced blocks or backticks; "fill in the missing keyword or method" as `gap`. Run every snippet before writing the options, so the right option is the real output. Find-the-bug, fix-it, review and implementation tasks stay in practice files: they need real code and a real review.

## Mode specifics

- **practice**: 3–5 tasks from `learning`/`shaky` topics plus one `solid` topic for mix; use the practice file for focused checks, the demo project for realistic context, a scaffolded project when a task needs its own environment.
- **test**: 10–15 questions: multiple choice, "what does this print or why does it fail", short open answers. No `todo` topics.
