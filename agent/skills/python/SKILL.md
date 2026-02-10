---
name: python
description: "Python programming best practices and patterns"
always: false
requires_bins: python3
requires_env:
---

# Python Skill

Best practices, patterns, and techniques for Python programming.

## Project Structure

```
project/
├── src/
│   └── myproject/
│       ├── __init__.py
│       ├── main.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── test_utils.py
├── docs/
├── requirements.txt
├── setup.py
└── README.md
```

## Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Freeze dependencies
pip freeze > requirements.txt
```

## Common Patterns

### Error Handling

```python
try:
    # Code that might fail
    result = risky_operation()
except SpecificError as e:
    # Handle specific error
    logger.error(f"Error: {e}")
except Exception as e:
    # Handle unexpected errors
    logger.error(f"Unexpected error: {e}")
finally:
    # Cleanup code
    cleanup()
```

### Context Managers

```python
with open('file.txt') as f:
    content = f.read()

with requests.Session() as session:
    response = session.get(url)
```

### List Comprehensions

```python
# Instead of:
result = []
for item in items:
    if item > 5:
        result.append(item * 2)

# Use:
result = [item * 2 for item in items if item > 5]
```

## Testing

```bash
# Run tests with pytest
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_main.py::test_function
```

## Code Quality

```bash
# Format code
black src/

# Lint code
flake8 src/

# Type checking
mypy src/

# Security check
bandit -r src/
```

## Debugging

```python
# Print debugging
print(f"Debug: {variable}")

# Using pdb
import pdb; pdb.set_trace()

# Logging
import logging
logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

## Performance Tips

- Use list comprehensions instead of loops
- Use generators for large datasets
- Profile code with `cProfile`
- Use `timeit` for timing code
- Avoid global variables
- Cache expensive operations

## Common Mistakes to Avoid

- Mutable default arguments: `def func(items=[]):`
- Not closing files or connections
- Catching too broad exceptions
- Modifying lists while iterating
- Not using f-strings for formatting
