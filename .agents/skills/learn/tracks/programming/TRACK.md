# Track: programming

Programming languages, frameworks, and engineering disciplines (backend, frontend, DevOps, databases, and so on). Read this file only when the course's `course.json` has `"track": "programming"`. Do not read the other tracks.

Files of this track:
- `setup.md`: questions for a new course and the meaning of `options`.
- `diagnostic.md`: entry diagnostic and program creation.
- `lessons.md`: lesson structure, task types, practice files, self-checks, the demo project.

## Any technology

This track teaches **any** programming language, framework, platform or engineering discipline, including niche, new and legacy ones (Elixir, Zig, Haskell, OCaml, Swift, Dart/Flutter, PHP/Laravel, Solidity, ABAP, COBOL, PowerShell, Unity/C#, embedded C, ...). The catalog below is a list of suggestions for learners who are unsure, not a limit. For a technology outside it, setup (see `setup.md`, "Any other technology") pins everything a session needs: scope, sources, version, practice file and run command.

## Course catalog (suggestions)

Offer these when the learner is unsure. The slug is the folder name in `my-learning/`.

| slug | aliases | scope |
|---|---|---|
| `go` | golang | Go language, standard library, tooling, idioms, concurrency, testing, performance |
| `js-ts` | js, ts, javascript, typescript | JavaScript and TypeScript: language semantics, type system, runtime (browser/Node), tooling |
| `python` | py | Python language, data model, typing, packaging, async, testing, performance |
| `rust` | rs | Rust language, ownership model, async, ecosystem, tooling, testing, performance |
| `java` | jvm | Java language, JVM, collections, concurrency, build tools, testing |
| `kotlin` | kt | Kotlin language, coroutines, JVM/Android/multiplatform, tooling |
| `csharp` | c#, dotnet, .net | C# and .NET: language, runtime, async, LINQ, ASP.NET basics, testing |
| `react` | reactjs | React: rendering model, hooks, state management, performance, testing, architecture |
| `angular` | ng | Angular: DI, signals/RxJS, change detection, routing, forms, testing, architecture |
| `vue` | vuejs | Vue: reactivity, components, composition API, state, routing, testing |
| `css` | styles | CSS: layout, cascade, modern features, responsive design, architecture, accessibility |
| `sql` | databases | SQL and relational databases: modeling, queries, indexes, transactions, query plans |
| `devops` | ops, infra | CI/CD, containers, orchestration, IaC, observability, security basics, release practices |
| `backend` | back, server | Technology-agnostic backend competencies: API design, databases, caching, queues, auth, reliability, architecture |
| `frontend` | front, web | Technology-agnostic frontend competencies: browser internals, performance, accessibility, state, architecture, security |

`backend`, `frontend` and `devops` are about general competencies a person needs to work confidently on a real project, not about one framework. The stack for their examples is chosen in setup (`options.stack`).

## Target level

`options.target_level` is one of `junior`, `mid`, `senior` (default), `staff`. It sets the depth of every lesson:
- `junior`: working knowledge, correct idiomatic basics, reading error messages, standard tooling.
- `mid`: independent feature work, testing, common patterns and their trade-offs, debugging.
- `senior`: idioms and style, internals that matter in production, trade-offs, reviewing others' code, designing components.
- `staff`: cross-system design, migration strategies, organizational standards, performance and reliability at scale.

A learner who starts below the target still gets the full path; a learner at or above the target gets the choice described in `diagnostic.md`, section 5.

## Teaching principles

- Teach to the target level: not only "how", but why, trade-offs, common mistakes, what reviewers in strong teams flag, and what the idiomatic style is. Name the source (official docs, the language style guide, well-known engineering guides). If a practice is just widespread rather than standard, say so.
- **Go beyond the textbook.** Alongside the official baseline, cover what real projects do: common practices in industry and in well-known open-source codebases, non-obvious tricks, and pitfalls that only surface in production (edge cases, performance cliffs, surprising defaults, "works on my machine" traps). Name where a practice comes from (a project, a company engineering blog, an RFC, a talk) and say honestly when it is a local convention. A hack is always presented with its cost and when not to use it.
- **Alternatives and trade-offs.** When a problem has several solutions, do not present one as the only answer. Lay out each realistic option with its characteristics (strengths, costs, failure modes, operational and maintenance impact) and say in which situations each fits: team size, load profile, consistency or latency requirements, codebase maturity. Finish with a recommended default and the conditions under which to pick another. The goal is for the learner to make this choice on their own.
- **Verify** anything version-specific or likely to have changed (language versions, deprecations, tooling defaults) with web search or official docs when available. If you cannot verify, say that you are unsure.
- **Calibrate.** Skip what the learner clearly knows, go deep where the gaps are.

## Code language rules

- **JavaScript is shown as TypeScript.** Types are the industry standard, so examples, tasks and demo projects use `.ts`/`.tsx`, even when the topic is JS runtime semantics (event loop, closures, `this`, prototypes, coercion). Plain JavaScript appears only when the point is the JS/TS difference itself, or when the learner explicitly asks (store that in `options.include`). Prefer strict mode, avoid `any` (use `unknown` and narrowing), and show how typing interacts with the behavior being discussed. This applies to every course with JS code.
- Python examples use type hints and follow PEP 8; Go follows `gofmt` and Effective Go; Rust follows `rustfmt` and Clippy defaults; every other language follows its official style guide or formatter (or, if none exists, the convention of its most prominent projects, labeled as such). Name it in the program's sources.
- Identifiers, code, commands and official terms stay in English; explanations and comments in practice files are in the learner's language.

## What counts as a check (for the progress rules)

"Two successful checks of different kinds" means, for example, a conceptual "why" question plus a code task, or a code-reading "what does this print" plus a "fix it" task. Two variants of the same multiple-choice question are one kind.
