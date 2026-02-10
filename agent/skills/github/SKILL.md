---
name: github
description: "Interact with GitHub using the gh CLI tool"
always: false
requires_bins: gh
requires_env:
---

# GitHub Skill

Use the `gh` CLI to interact with GitHub repositories, pull requests, and issues.

## Prerequisites

- Install `gh` CLI: https://cli.github.com
- Authenticate: `gh auth login`

## Common Commands

### Repository Operations

```bash
# Clone a repository
gh repo clone owner/repo

# View repository information
gh repo view owner/repo

# List repositories
gh repo list
```

### Pull Requests

```bash
# Create a pull request
gh pr create --title "Title" --body "Description"

# List pull requests
gh pr list

# Check PR status
gh pr status

# Merge a PR
gh pr merge <number>
```

### Issues

```bash
# Create an issue
gh issue create --title "Title" --body "Description"

# List issues
gh issue list

# Close an issue
gh issue close <number>
```

### Workflows & CI

```bash
# View workflow runs
gh run list

# View run details
gh run view <run-id>

# Trigger a workflow
gh workflow run <workflow-name>
```

## Tips

- Use `gh <command> --help` for detailed help
- Most commands work with the current repository by default
- Use `--repo owner/repo` to specify a different repository
