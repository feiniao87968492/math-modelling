# CLAUDE.md — math-modeling-v4 skill instructions

- Treat `SKILL.md` as dispatcher and `references/` files as the source of execution detail.
- v4 is Markdown-first.
- Do not use `modeling_state.yaml` as the workflow driver.
- Subagents are expert reviewers, not stage owners.
- Reviewer profiles are not sufficient by themselves to satisfy fixed review gates.
- Fixed review gates require actual subagent-produced review artifacts in `reviews/`.
- The main agent must not self-review past a fixed review gate.
- Use actual subagent-produced review artifacts when satisfying fixed review gates.
- Keep the old `math-modeling` package untouched.
