# Notes for Developers

## 1. Setting up the project

### Running locally

Install dev depenendencies:

```bash
uv sync --group dev
```

Run project:

```bash
uv run python main.py
```

## 2. Pre-commit hooks

```bash
uv run pre-commit install
```

After that, linters will run on each commit. You can also run them manually:

```bash
uv run pre-commit run --all-files
```

## 3. Pull requests

#### Please refrain from pushing onto `main`!

Every change should be submitted as a **Pull Request**. This approach enables two things:

1. Other developers can review the code
2. Automatic workflows will be ran to test and check the code

**NOTE:** Consider using understandable commit titles, for example:

```
add: saving output to file
fix: out-of-bounds bug
```

## 4. Miscellaneous

1. All application source files should be inside `/src/cukiernia/`
2. Avoid pushing images/audio files/other auxiliary files into the repository
3. Keep correct naming conventions (PEP8)
