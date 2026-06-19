# Project Setup Helper

An educational, interactive Python project setup helper.

This repo is intentionally structured as a real Python package so it teaches two things at once:

1. how to create a beginner Python project with a virtual environment, dependency files, `.gitignore`, and setup notes
2. how Python packages, modules, imports, `src/` layout, and CLI entry points work

The original version was one working script. This version refactors that script into an installable package.

---

## What this helper creates

Depending on the settings in `src/project_setup_helper/config.py`, the helper can create:

- `.venv/`
- `.gitignore`
- `requirements.txt`
- `requirements-dev.txt`
- `pyproject.toml`
- a package folder such as `src/my_python_project/`
- timestamped setup logs
- local setup notes

It can also walk macOS Apple Silicon users through Homebrew Python and `PATH` checks.

---

## Repo layout

```text
python_project_setup_template/
├── README.md
├── pyproject.toml
├── src/
│   └── project_setup_helper/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── config.py
│       ├── paths.py
│       ├── logging_setup.py
│       ├── prompts.py
│       ├── commands.py
│       ├── os_detect.py
│       ├── venv_tools.py
│       ├── dependencies.py
│       ├── notes.py
│       │
│       ├── installers/
│       │   ├── __init__.py
│       │   ├── macos_apple_silicon.py
│       │   ├── macos_linux.py
│       │   └── windows.py
│       │
│       └── project_files/
│           ├── __init__.py
│           ├── gitignore.py
│           ├── requirements.py
│           └── pyproject.py
│
├── tests/
│   ├── test_config.py
│   └── test_os_detect.py
└── examples/
    └── generated_project_example/
```

---

## What the layout teaches

```text
src/project_setup_helper/
```

is the main Python package.

```text
installers/
project_files/
```

are subpackages.

```text
cli.py
config.py
commands.py
```

are modules.

This import:

```python
from project_setup_helper.project_files.gitignore import ensure_gitignore
```

means:

```text
from package.subpackage.module import function
```

---

## Install for development

From the repo root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e .
```

The `-e` means editable install. When you edit files under `src/project_setup_helper/`, Python sees the changes immediately.

---

## Run it

After editable install:

```bash
project-setup-helper
```

You can also run the package directly:

```bash
python -m project_setup_helper
```

Both call:

```python
project_setup_helper.cli:main
```

That entry point is defined in `pyproject.toml`:

```toml
[project.scripts]
project-setup-helper = "project_setup_helper.cli:main"
```

---

## Edit the configuration

Open:

```text
src/project_setup_helper/config.py
```

Important values:

```python
TARGET_OS = "macos_linux"       # or "windows"
VENV_DIR_NAME = ".venv"
PROJECT_STYLE = "requirements"  # or "pyproject"
```

For package projects:

```python
PROJECT_NAME = "my-python-project"
PACKAGE_IMPORT_NAME = "my_python_project"
USE_SRC_LAYOUT = True
```

For macOS Apple Silicon users:

```python
ENABLE_MACOS_HOMEBREW_PYTHON_HELPER = True
```

---

## Module map from the original single script

```text
Original responsibility              New module
--------------------------------------------------------------
TARGET_OS, PROJECT_STYLE, deps       config.py
PROJECT_ROOT, VENV_DIR, LOG_FILE     paths.py
SafeStreamHandler, logging config    logging_setup.py
ask_yes_no, ask_choice, pause        prompts.py
run_command, run_interactive_command commands.py
is_macos, is_apple_silicon           os_detect.py
Homebrew helper functions            installers/macos_apple_silicon.py
Windows-specific preflight           installers/windows.py
macOS/Linux shared preflight         installers/macos_linux.py
get_base_python_path, venv paths     venv_tools.py
ensure_gitignore                     project_files/gitignore.py
create_requirements_txt              project_files/requirements.py
create_pyproject_toml                project_files/pyproject.py
install_dependencies                 dependencies.py
write_local_notes                    notes.py
main flow                            cli.py
```

---

## macOS Apple Silicon Python setup

On Apple Silicon Macs, Apple’s system-managed Python is usually located at:

```text
/usr/bin/python3
```

For development, you usually want Python installed through Homebrew instead:

```text
/opt/homebrew/bin/python3
```

The Apple Silicon module checks:

- whether you are on macOS Apple Silicon
- whether Homebrew is installed
- whether Python is installed through Homebrew
- whether `/opt/homebrew/bin` appears before `/usr/bin` on `PATH`
- whether your virtual environment will use Homebrew Python

Verify Python resolution with:

```bash
which -a python3
python3 --version
```

Ideally, `python3` should resolve to:

```text
/opt/homebrew/bin/python3
```

before:

```text
/usr/bin/python3
```

---

## Beginner teaching path

This repo demonstrates this progression:

```text
Level 1: one script
Level 2: functions
Level 3: modules
Level 4: package
Level 5: installable CLI tool
```

The helper itself now lives at Level 4/5 while still creating beginner-friendly project templates.

---

## Run tests

Install dev tools:

```bash
python -m pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

---

## Notes

This project is intentionally educational. Some design choices, such as keeping beginner-editable settings in `config.py`, are meant to make the code easier to inspect before introducing command-line flags, config files, or advanced packaging patterns.
