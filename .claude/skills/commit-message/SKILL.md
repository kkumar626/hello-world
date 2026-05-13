---
name: commit-message
description: Generates a conventional commit message based on staged changes. Use when the user wants to write a commit message, generate a commit message, or asks what to write for a commit.
---

When generating a commit message:

1. Run `git diff --staged` to see what is staged for commit.
2. If nothing is staged, run `git status` and let the user know nothing is staged yet.
3. Write a commit message following the Conventional Commits format:

```
<type>(<scope>): <short summary>

- Bullet point detail about a specific change
- Another bullet point if needed
```

**Types to use:**
- `feat` — a new feature or capability
- `fix` — a bug fix
- `refactor` — code change that neither fixes a bug nor adds a feature
- `docs` — documentation changes only
- `chore` — maintenance tasks (dependencies, config, scripts)
- `test` — adding or updating tests
- `data` — changes to data files (e.g. countries.csv, countries.json)

**Rules:**
- Keep the first line under 72 characters
- Use lowercase for type and scope
- Scope is optional — use it when the change is clearly scoped to one file or module (e.g. `feat(generate_countries_csv): ...`)
- Bullet points are optional for very small, obvious changes
- Do NOT include "Co-authored-by" or any attribution lines
- Do NOT run `git commit` — only output the message for the user to review
- After the message, output the full `git commit -m "..."` command the user can copy and paste into their terminal to execute it themselves. Use the exact message generated, preserving all newlines using `$'...'` shell quoting syntax if the message is multi-line.
