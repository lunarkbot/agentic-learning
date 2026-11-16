---
name: learn
description: Turns the agent into a mentor for one course in this learning repository: programming, a foreign language, or any other subject. Runs the placement test, teaches new topics, sets short tasks the learner answers in files, reviews with spaced repetition, quizzes, reports progress, and keeps program, progress and timeline files up to date, then commits. Use whenever the user types /learn, or says things like "learn go", "let's practice English", "quiz me on physics", "review", "continue my course", "show my progress", even when no mode is given. Also use when the learner writes "done" or "stop" (or the same word in their language) while a session is open.
---

# learn (Claude Code entry point)

This is a thin stub. The single source of truth lives in `.agents/skills/learn/` (shared with every other agent), so there is only one copy to maintain.

1. Read `AGENTS.md` in the repository root if it is not already in your context.
2. Read `.agents/skills/learn/SKILL.md` in full and follow it exactly, using the arguments the user passed to this skill (`<course> [mode] [focus]`).
3. Resolve the referenced files (`references/`, `templates/`, `tracks/`, `scripts/`) relative to `.agents/skills/learn/`, not relative to this stub.
