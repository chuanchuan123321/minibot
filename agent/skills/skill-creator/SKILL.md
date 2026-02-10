---
name: skill-creator
description: "Guide for creating custom skills"
always: false
requires_bins:
requires_env:
---

# Skill Creator Guide

Learn how to create custom skills for Minibot.

## What is a Skill?

A skill is a reusable knowledge module that teaches the AI about specific domains, tools, or best practices. Skills are stored as Markdown files with YAML metadata.

## Creating a Skill

### Step 1: Create Skill Directory

```bash
mkdir -p ~/Desktop/AI智能体/workspace/skills/my-skill
```

### Step 2: Create SKILL.md File

Create a file named `SKILL.md` in your skill directory with the following structure:

```markdown
---
name: my-skill
description: "Brief description of what this skill does"
always: false
requires_bins: tool1,tool2
requires_env: ENV_VAR1,ENV_VAR2
---

# My Skill

Full description and instructions for this skill.

## Section 1
...

## Section 2
...
```

### Step 3: Fill in Metadata

- **name**: Unique identifier for the skill (lowercase, no spaces)
- **description**: One-line description of the skill
- **always**: Set to `true` to always load this skill, `false` for on-demand
- **requires_bins**: Comma-separated list of CLI tools needed (e.g., `git,docker`)
- **requires_env**: Comma-separated list of environment variables needed

### Step 4: Write Skill Content

After the frontmatter, write comprehensive Markdown content that teaches the AI about:

- How to use specific tools
- Best practices and patterns
- Common commands and examples
- Tips and tricks
- Common mistakes to avoid

## Skill Examples

### Example 1: Tool-Based Skill (GitHub)

```markdown
---
name: github
description: "Interact with GitHub using the gh CLI"
always: false
requires_bins: gh
requires_env:
---

# GitHub Skill

Use the `gh` CLI to interact with GitHub...

## Prerequisites
- Install gh CLI
- Authenticate with `gh auth login`

## Common Commands
...
```

### Example 2: Knowledge-Based Skill (Web Search)

```markdown
---
name: web
description: "Web search and information gathering"
always: false
requires_bins:
requires_env:
---

# Web Skill

Techniques for effective web searching...

## Search Strategies
...
```

### Example 3: Programming Skill (Python)

```markdown
---
name: python
description: "Python programming best practices"
always: false
requires_bins: python3
requires_env:
---

# Python Skill

Best practices for Python development...

## Project Structure
...
```

## Skill Locations

Skills can be stored in two locations:

1. **Builtin Skills** (included with Minibot)
   - Location: `agent/skills/`
   - Managed by Minibot team

2. **Workspace Skills** (your custom skills)
   - Location: `workspace/skills/`
   - Create your own skills here
   - Workspace skills override builtin skills with the same name

## Best Practices

### 1. Be Specific and Practical

✅ Good:
```markdown
## Using Docker

To run a container:
```bash
docker run -d -p 8080:8080 myimage
```
```

❌ Bad:
```markdown
## Docker

Docker is a containerization platform.
```

### 2. Include Examples

Always provide concrete examples that the AI can reference:

```markdown
## Example: Creating a GitHub Issue

```bash
gh issue create --title "Bug: Login fails" --body "When I click login..."
```
```

### 3. Organize with Headers

Use clear hierarchical headers:

```markdown
# Skill Name

## Section 1
### Subsection 1.1
### Subsection 1.2

## Section 2
```

### 4. Include Prerequisites

Always list what's needed:

```markdown
## Prerequisites

- Node.js 16+
- npm or yarn
- Git
```

### 5. Add Tips and Warnings

```markdown
💡 **Tip**: Use `--help` flag for more options

⚠️ **Warning**: This command will delete data
```

## Testing Your Skill

1. Place your skill in `workspace/skills/my-skill/`
2. Run Minibot
3. The skill will be automatically loaded
4. Ask the AI to use your skill

## Sharing Skills

To share your skill with others:

1. Create a GitHub repository
2. Follow the skill structure
3. Add documentation
4. Share the repository link

## Skill Naming Conventions

- Use lowercase names
- Use hyphens for multi-word names: `my-skill`
- Keep names short and descriptive
- Avoid generic names like `tools` or `help`

## Common Skill Types

### Tool Skills
Teach the AI how to use specific CLI tools or APIs.

### Knowledge Skills
Provide best practices, patterns, and techniques.

### Domain Skills
Teach about specific domains (web development, DevOps, etc).

### Integration Skills
Teach how to integrate with external services.

## Troubleshooting

### Skill Not Loading

1. Check the skill directory name matches the `name` field
2. Verify SKILL.md exists in the directory
3. Check for YAML syntax errors in frontmatter
4. Verify required tools are installed

### Skill Not Being Used

1. Check if skill is marked as `always: true`
2. Ask the AI explicitly to use the skill
3. Provide context that requires the skill
4. Check if dependencies are missing

## Advanced: Skill Dependencies

You can create skills that depend on other skills:

```markdown
---
name: advanced-github
description: "Advanced GitHub workflows"
always: false
requires_bins: gh
requires_env:
depends_on: github
---

# Advanced GitHub Skill

This skill builds on the basic GitHub skill...
```

Note: Dependency management is not yet implemented but planned for future versions.
