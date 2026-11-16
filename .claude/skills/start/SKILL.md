---
name: start
description: First-run setup wizard and settings menu for this learning repository. Asks which language to talk in (or takes it from the argument, e.g. "start Russian"), saves it to my-learning/settings.json, asks whether the learner wants to study programming, a foreign language, or another subject, sets up the course, and hands over to the placement test. When setup is already done, shows a menu to add a course, change a course's settings (such as interactive browser exercises), change the conversation language, back up progress, or update the engine. Use when the user types /start, start, init, setup, or says things like "I want to use these courses", "set this up", "add a new course", "change the language", "back up my progress".
---

# start (Claude Code entry point)

This is a thin stub. The single source of truth lives in `.agents/skills/start/` (shared with every other agent), so there is only one copy to maintain.

1. Read `AGENTS.md` in the repository root if it is not already in your context.
2. Read `.agents/skills/start/SKILL.md` in full and follow it exactly, using the arguments the user passed to this skill (an optional language, e.g. `Russian`).
3. Resolve every path it mentions relative to the repository root.
