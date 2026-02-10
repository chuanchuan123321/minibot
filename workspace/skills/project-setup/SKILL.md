---
name: project-setup
description: "Guide for setting up new projects"
always: false
requires_bins:
requires_env:
---

# Project Setup Skill

Quick guide for setting up new projects with best practices.

## New Python Project

```bash
# Create project directory
mkdir my-project
cd my-project

# Initialize git
git init

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Create project structure
mkdir src tests docs
touch README.md requirements.txt setup.py

# Create initial files
echo "# My Project" > README.md
echo "pytest" > requirements.txt
```

## New Node.js Project

```bash
# Create project directory
mkdir my-project
cd my-project

# Initialize npm
npm init -y

# Install common dependencies
npm install --save-dev prettier eslint

# Create project structure
mkdir src tests
touch .gitignore .prettierrc .eslintrc.json
```

## New Git Repository

```bash
# Initialize
git init

# Create .gitignore
echo "node_modules/" > .gitignore
echo "venv/" >> .gitignore
echo ".env" >> .gitignore
echo "__pycache__/" >> .gitignore

# Initial commit
git add .
git commit -m "Initial commit"

# Add remote
git remote add origin https://github.com/user/repo.git
git branch -M main
git push -u origin main
```

## Project Checklist

- [ ] README.md with description and setup instructions
- [ ] .gitignore file
- [ ] License file
- [ ] Contributing guidelines
- [ ] Code of conduct
- [ ] Issue templates
- [ ] Pull request template
- [ ] CI/CD configuration
- [ ] Tests
- [ ] Documentation

## Common Project Types

### Web Application
- Frontend framework (React, Vue, etc)
- Backend framework (Django, Express, etc)
- Database setup
- API documentation

### CLI Tool
- Argument parsing
- Help documentation
- Configuration file support
- Error handling

### Library
- Clear API design
- Comprehensive documentation
- Examples and tutorials
- Version management

### Data Science
- Jupyter notebooks
- Data directory structure
- Requirements file
- Results directory
