# Agentic Learning

Turn your AI coding agent into a personal tutor. It finds out what you want to learn, measures your level, builds a program for you, teaches with short lessons and tasks, repeats what you are about to forget, and keeps an honest log of your progress.

Works for three kinds of courses:

| track | examples | levels |
|---|---|---|
| **Programming** | any language or framework: Go, TypeScript, Python, Rust, React, SQL, DevOps ... or Elixir, Zig, Swift, PHP, COBOL | junior → mid → senior → staff |
| **Foreign languages** | English (US), British English, Spanish (Spain or Mexico), German, French, Portuguese (Brazil), Japanese | CEFR A1 → C2 |
| **Any other subject** | physics, math, history, economics, an exam (SAT, AP, IELTS-style prep), project management, music theory | a scale that fits the subject |

You talk to the tutor in your own language. The repository itself is in English, so anyone can use it.

## Quick start (no technical knowledge needed)

1. Open an AI agent that can work with files and run commands on your computer: Claude Code, Codex, OpenCode, GitHub Copilot (agent mode in VS Code), Google Antigravity, Gemini CLI, Kimi Code, Qwen Code, or similar.
2. Send it one message, in any language:

   > Set up https://github.com/lunarkbot/agentic-learning for me. I want to use these courses.

3. The agent downloads the repository and checks your computer. If something useful is missing (Python, git, a comfortable editor), it explains what it is for and offers to install it; nothing is installed without your OK. Then it asks you a few short questions: which language to talk in, what you want to learn, and how. Then it gives you a short placement test, in a file you open in your editor.

That's it. Next time, open the same folder in your agent and write `learn` (or `/learn`).

> Chat-only websites (a plain chat window with no access to your files) cannot run this: the tutor needs to create and read files on your computer. Models such as DeepSeek, Qwen or Kimi work fine through an agent app (for example OpenCode, Qwen Code, Kimi Code).

## How a session works

1. You write `learn` (or `learn english`, `learn go practice`). The agent checks your progress and says in two or three lines what you will do today.
2. It creates a session folder with `lesson.md`: an explanation with examples and a few tasks. For code or long writing there is also a `practice` file.
3. You open the file in your editor, read, and write your answers right in the file, under **Answer:**.
4. You send one word to the chat: **`done`**. The agent reads your answers, checks them (it runs your code, corrects your text, recomputes your numbers), writes a review into the file, and prepares the next step.
5. A session takes 30–45 minutes, one to three steps. Send **`stop`** at any time to wrap up.
6. At the end you get a short summary, and your progress is saved.

In language courses some tasks open in your **browser** instead (interactive exercises; optional for the other tracks): flashcards, pick one of four options, choose or type the missing word or ending, put the words in order, clickable tests. You get instant feedback, a 🔊 button lets you hear the correct sentence after you answer, and your answers are saved to the session folder automatically, so `done` works the same way.

Why files and not chat? In a chat box Enter sends the message and there is no formatting. In a file you can write code, an essay or a translation comfortably, and the whole lesson stays readable later. Any editor works: VS Code, an IDE, even Notepad or TextEdit. Turn on Markdown preview if your editor has it.

## Commands

Plain words work in every agent. Where skills appear as slash commands, you can also type `/start` and `/learn` (Claude Code, and others); in Codex, `$learn`.

| command | what happens |
|---|---|
| `start` | first setup, or the settings menu later (add a course, change a course's settings, change the language, back up, update) |
| `start Spanish` | first setup, and the agent talks to you in Spanish from now on |
| `learn` | overview of your courses, then pick one |
| `learn <course>` | the agent picks the best mode for today |
| `learn <course> study` | new material |
| `learn <course> practice` | short tasks on what you need to strengthen |
| `learn <course> review` | refresh what you are about to forget (spaced repetition) |
| `learn <course> test` | a quiz on what you covered, then you go through the mistakes together |
| `learn <course> stat` | a progress report only: what is done, strengths, weak spots, what is due |
| `learn <course> practice <focus>` | any mode plus a focus, e.g. `learn en-us practice phrasal verbs` |
| `done` | "I finished this step, check it" |
| `stop` | end the session and save |

Words in your language work too (`готово`, `listo`, `fertig`).

Do not type `/init`: in several agents it is a built-in command that rewrites the agent's instruction file. Use `start`.

## What the tutor does differently per track

- **Programming**: any technology, not only the suggested list: for something less common (Elixir, Zig, Haskell, Swift, PHP, Solidity, COBOL, ...) the agent pins the version, the official sources, the practice file and the run command during setup and checks them with a hello-world before the first lesson. Senior-level depth (idioms, trade-offs, what code reviewers flag, how real projects do it), every example and task is executed before you see it, practice files with self-checks you can run, an optional small demo project that grows with the course. JavaScript is taught as TypeScript.
- **Foreign languages**: always one exact variant (US English stays US English in every example and correction), a CEFR placement test, a program up to your target level, the exercise mix you choose (grammar, vocabulary, reading, writing, translation in either direction, register, dialogues, exam tasks), detailed writing corrections, and flashcards with spaced review. If you are already above your target, you can raise it or switch to a review mode across all levels.
- **Any other subject**: the agent first asks what exactly you need (an exam, school support, a job skill, a hobby) and proposes a format that fits: worked problems, explanations in your own words, cases, source analysis, practice plans. Health, law and finance content is educational only.

## Interactive exercises

One of the exercise types: on by default for foreign languages, off by default for programming and other subjects, where code, problems and explanations are better done in files. You can switch it either way during setup, or later with `start` → "change a course's settings". They add a little to the agent's usage per session (the agent prepares answer options and reads your results), but much less than you might expect: the player itself is prebuilt.

How it works:
- The player is a single prebuilt page in this repository (`.agents/skills/learn/interactive/player.html`). Agents never generate web pages; they only write a short list of questions (`exercises.json`), which keeps the cost low and the experience the same with every agent.
- `python .agents/skills/learn/scripts/learn_tool.py serve <course>` opens the exercises in your browser and saves every answer into the session folder. It runs only on your computer (`127.0.0.1`) and stops by itself when idle.
- Without Python, the page still works offline; at the end you download or copy your results.

| type | example |
|---|---|
| flashcard | *перенести (встречу)* → show answer → "I knew it" / "I didn't know" |
| choose one | *I was born ___ 1994.* in / on / at / by |
| fill the gap | *Yesterday we ___ (stop) at a diner.* → type *stopped*, or pick from a dropdown |
| word order | tap *I · have · never · been · to · Chicago · .* in the right order |
| test | the same formats without instant feedback; the agent grades them on `done` |

## Your data and privacy

- Everything about you lives in one folder, `my-learning/`, inside the repository folder on your computer. It is **ignored by this public repository**, so it is never uploaded here and updating the tutor never touches it.
- `my-learning/` is its own small git repository: every session is saved as a commit, so nothing gets lost.
- To keep a backup or continue on another computer, write `start` and choose "back up". Use a **private** repository: your files describe what you study and how it goes.
- Nothing beyond learning progress is stored: no names, emails or other personal data.

## Updating

Write `start` and choose "update". The agent pulls the new version of the instructions and checks that your courses still fit. Your data is not affected.

## Setup for agents

> This section is written for AI agents. If you are a person, you can skip it: just ask your agent to set the repository up.

Follow these steps in order. Talk to the user in the language of their request. Keep messages short and non-technical. Ask before installing anything.

1. **Detect the environment.** OS (Windows, macOS, Linux) and shell. On Windows prefer PowerShell syntax unless you run in bash. Do not chain commands with `&&` when the shell may be Windows PowerShell 5.

2. **Check git.** Run `git --version`.
   - Missing: tell the user git is needed to download and update the tutor, and offer to install it: Windows `winget install --id Git.Git -e`, macOS `xcode-select --install` (or `brew install git`), Debian/Ubuntu `sudo apt install git`. Install only after a clear yes. If the user declines, download https://github.com/lunarkbot/agentic-learning/archive/refs/heads/main.zip and extract it instead (updates will then be manual).

3. **Choose the folder.** If the user named a location, use it. Otherwise use a folder named `agentic-learning` in the user's home directory (`$HOME/agentic-learning`, on Windows `%USERPROFILE%\agentic-learning`) and tell the user where it is. If the folder already exists and is a clone of this repository, reuse it and run `git pull --ff-only` instead of cloning. Never overwrite an existing non-empty folder.

4. **Clone.** `git clone https://github.com/lunarkbot/agentic-learning.git <folder>`

5. **Prepare the computer.** Follow section 2 of `<folder>/.agents/skills/start/SKILL.md` ("Prepare the computer"): check Python 3.8+ (and an editor), explain in plain words what is missing and why, and install only after a clear yes. Without Python everything still works; the agent follows the rules by hand.

6. **Verify.** From the folder: `python .agents/skills/learn/scripts/learn_tool.py doctor` (use the interpreter found in step 5). It must list the tracks `language, programming, subject` and say the workspace is not created yet.

7. **Make the folder your working directory.** Skills and instructions are discovered from the folder the agent was started in.
   - CLI agents (Claude Code, Codex, OpenCode, Gemini CLI, Qwen Code, Kimi Code): if you cannot switch the working directory yourself, tell the user the two steps: open a terminal in the folder (`cd <folder>`) and start the agent again there.
   - IDE agents (VS Code with Copilot, Antigravity, Cursor, JetBrains): tell the user to open the folder via File → Open Folder.
   - If you can keep working in this session, continue now: read `<folder>/AGENTS.md` and `<folder>/.agents/skills/start/SKILL.md`, and run every command with `<folder>` as the working directory. Still tell the user to open that folder next time.

8. **Run the setup wizard.** Follow `.agents/skills/start/SKILL.md`. If the user's request was written in some language, propose it as the conversation language instead of asking an open question.

9. **Done when** `doctor` shows the workspace with the chosen language and at least one course, and the user knows the two words `learn` and `done`.

## Troubleshooting

- **The agent does not know `learn` or `start`.** It must be started in the repository folder (step 7 above). Plain words work in any agent because `AGENTS.md` routes them; if your agent does not read `AGENTS.md` by default, tell it once: "read AGENTS.md and follow it".
- **I closed the chat in the middle of a session.** Write `learn <course> done` (or just `learn <course>`): the agent finds the unfinished session and continues.
- **No Python.** The helper script is a convenience; the agent works without it.
- **Sync conflict.** The agent tells you and never resolves it silently. The usual cause: a session on another computer was not saved before you started here.
- **I want to delete a lesson.** Delete its folder under `my-learning/<course>/sessions/`. Progress is stored separately and is not affected.

## Repository structure

```
agentic-learning/
├── AGENTS.md                       # rules for every agent (formats, tracks, git, language policy)
├── README.md                       # this file
├── CLAUDE.md, GEMINI.md, QWEN.md   # bridges to AGENTS.md for agents that read their own file
├── .github/copilot-instructions.md # bridge for GitHub Copilot
├── .agents/skills/
│   ├── start/SKILL.md              # setup wizard and settings menu
│   └── learn/
│       ├── SKILL.md                # session engine shared by all tracks
│       ├── references/             # progress rules, session files
│       ├── templates/              # course file templates
│       ├── tracks/                 # programming/, language/, subject/: teaching rules per track
│       ├── interactive/            # prebuilt browser player for interactive exercises
│       └── scripts/learn_tool.py   # helper (Python 3.8+, standard library only)
├── .claude/skills/                 # thin stubs for Claude Code pointing to .agents/skills
└── my-learning/                    # created by `start`; your private data, not part of this repository
```

## Contributing

- **A new track** (for example music performance or sports) is a folder under `.agents/skills/learn/tracks/` with the same five files: `TRACK.md`, `setup.md`, `diagnostic.md`, `lessons.md`, `course.json`. The engine and the progress rules stay shared, and other tracks are not affected.
- **Improving a track**: keep each track self-contained; never reference another track's rules.
- Everything in the repository is written in US English.
- Test the helper with a throwaway workspace: `python .agents/skills/learn/scripts/learn_tool.py --data /tmp/test-ws init --lang en --lang-name English --no-git`.

## License

[MIT](LICENSE)
