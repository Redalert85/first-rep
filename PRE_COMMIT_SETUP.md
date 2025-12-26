# Pre-commit Hook Setup Guide

This repository includes pre-commit hooks to automatically check Python code quality before commits.

## Installation

1. Install pre-commit:
   ```bash
   pip install pre-commit
   ```

2. Install the git hooks:
   ```bash
   pre-commit install
   ```

## Usage

### Automatic Checks
Once installed, pre-commit will automatically run on every `git commit`. If any checks fail, the commit will be blocked until you fix the issues.

### Manual Checks
You can run the hooks manually at any time:

```bash
# Run on all files
pre-commit run --all-files

# Run on specific files
pre-commit run --files file1.py file2.py
```

## Configured Hooks

1. **flake8 (syntax errors)**: Checks for critical syntax errors (E9) and undefined names (F63, F7, F82)
2. **flake8 (style check)**: Checks code style with max complexity of 10 and max line length of 127

## Updating Hooks

To update to the latest versions of the hooks:

```bash
pre-commit autoupdate
```

## Bypassing Hooks (Not Recommended)

In rare cases where you need to commit despite hook failures:

```bash
git commit --no-verify -m "Your commit message"
```

**Note**: This should only be used in exceptional circumstances, as it bypasses important code quality checks.
