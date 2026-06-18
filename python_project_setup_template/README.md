# Interactive Python Project Setup Template

This repo contains an educational setup script for creating a Python project with:

- a virtual environment
- either `requirements.txt` or `pyproject.toml`
- optional `src/` layout for package projects
- `.gitignore` rules for `.venv/`, Python caches, and setup logs
- timestamped logs
- interactive pauses and explanations

The script is meant to teach what is happening while it sets up the project.

---

## Files

```text
your-repo/
├── interactive_python_project_setup.py
├── README.md
│
├── .gitignore                 # created or updated by the script
├── .venv/                     # created by the script, ignored by Git
├── setup_logs/                # created by the script, ignored by Git
│   └── python_project_setup_YYYYMMDD_HHMMSS.log
│
├── requirements.txt           # if using requirements mode
├── requirements-dev.txt       # optional, if dev tools are included
│
└── pyproject.toml             # if using pyproject mode
```

If using `pyproject.toml` with `src/` layout, the script can also create:

```text
your-repo/
├── pyproject.toml
└── src/
    └── my_python_project/
        ├── __init__.py
        └── cli.py
```

---

## Step 1: Edit the config section

Open:

```text
interactive_python_project_setup.py
```

Then edit the top `CONFIG` section.

Important values:

```python
TARGET_OS = "windows"       # or "macos_linux"
VENV_DIR_NAME = ".venv"
PROJECT_STYLE = "requirements"  # or "pyproject"
```

For `pyproject.toml` projects, also edit:

```python
PROJECT_NAME = "my-python-project"
PACKAGE_IMPORT_NAME = "my_python_project"
USE_SRC_LAYOUT = True
```

### Project name vs package import name

These are not always the same.

```toml
[project]
name = "my-python-project"
```

This is the install/distribution name.

But Python imports use underscores:

```python
import my_python_project
```

---

## Step 2: Run the script

From the repo folder:

```bash
python interactive_python_project_setup.py
```

The script will pause at major decision points and explain what it is about to do.

---

## Step 3: Activate the virtual environment

### Windows

```bash
.venv\Scripts\activate
```

### macOS/Linux

```bash
source .venv/bin/activate
```

After activation, `python` and `pip` should point inside `.venv`.

You can check:

### Windows

```bash
where python
where pip
```

### macOS/Linux

```bash
which python
which pip
```

---

## Mode A: requirements.txt

Use this mode for simple projects and scripts.

Example layout:

```text
your-repo/
├── script.py
├── helper.py
├── requirements.txt
└── .venv/
```

Typical workflow:

```bash
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
pip install -r requirements.txt
python script.py
```

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python script.py
```

`requirements.txt` lists third-party packages:

```text
requests
beautifulsoup4
```

---

## Mode B: pyproject.toml

Use this mode for reusable packages, command-line tools, or larger projects.

Example layout:

```text
your-repo/
├── pyproject.toml
├── src/
│   └── my_python_project/
│       ├── __init__.py
│       └── cli.py
└── .venv/
```

Typical workflow:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

The `-e` means editable install.

That means your project is linked into the virtual environment. When you edit source files, Python sees the changes immediately.

---

## What the script teaches

### `python -m venv .venv`

Runs Python's built-in `venv` module and creates a virtual environment in `.venv`.

### `pip install -r requirements.txt`

Installs packages listed in `requirements.txt`.

### `pip install -e .`

Installs the project in the current folder in editable mode.

### `.gitignore`

The virtual environment should not be committed to Git. The script ensures rules like these exist:

```gitignore
.venv/
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.ruff_cache/
setup_logs/
```

---

## Logs

Each run creates a timestamped log file:

```text
setup_logs/python_project_setup_YYYYMMDD_HHMMSS.log
```

The logs include:

- selected configuration
- commands run
- command output
- errors, if any

The `setup_logs/` folder is ignored by Git by default.

---

## Suggested usage

For personal scripts, start with:

```python
PROJECT_STYLE = "requirements"
```

For a reusable package or CLI tool, use:

```python
PROJECT_STYLE = "pyproject"
USE_SRC_LAYOUT = True
```

---

## Deleting and recreating the environment

Virtual environments are disposable.

If something breaks:

```bash
rm -rf .venv        # macOS/Linux
```

Windows PowerShell:

```powershell
Remove-Item -Recurse -Force .venv
```

Then rerun the setup script.
