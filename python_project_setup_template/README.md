# Interactive Python Project Setup Template

This repo contains an educational setup script for creating a Python project with:

- a virtual environment
- either `requirements.txt` or `pyproject.toml`
- optional `src/` layout for package projects
- `.gitignore` rules for `.venv/`, Python caches, and setup logs
- timestamped logs
- interactive pauses and explanations
- macOS Apple Silicon checks for Homebrew, Homebrew-managed Python, and PATH setup

The script is meant to teach what is happening while it sets up the project.

It is interactive by design. At major decision points, the script explains what it is about to do and gives you options, including the option to exit.

---

## Files

```text
your-repo/
├── interactive_python_project_setup.py
├── README.md
│
├── .gitignore
├── .venv/
├── setup_logs/
│   └── python_project_setup_YYYYMMDD_HHMMSS.log
│
├── SETUP_NOTES.md
│
├── requirements.txt
├── requirements-dev.txt
│
└── pyproject.toml
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
TARGET_OS = "macos_linux"       # or "windows"
VENV_DIR_NAME = ".venv"
PROJECT_STYLE = "requirements"  # or "pyproject"
```

For `pyproject.toml` projects, also edit:

```python
PROJECT_NAME = "my-python-project"
PACKAGE_IMPORT_NAME = "my_python_project"
USE_SRC_LAYOUT = True
```

For macOS Apple Silicon users, this helper is enabled by default:

```python
ENABLE_MACOS_HOMEBREW_PYTHON_HELPER = True
```

---

## Step 2: Run the script

From the repo folder:

```bash
python3 interactive_python_project_setup.py
```

On Windows:

```bash
python interactive_python_project_setup.py
```

The script will pause at major decision points and explain what it is about to do.

You can type this at most prompts to stop safely:

```text
exit
```

You can also use:

```text
q
quit
cancel
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

The script can help you check:

- whether you are on macOS Apple Silicon
- whether Homebrew is installed
- whether Python is installed through Homebrew
- whether `/opt/homebrew/bin` appears before `/usr/bin` on `PATH`
- whether your virtual environment will use Homebrew Python

If Homebrew is missing, the script asks whether you want to install it.

If Homebrew Python is missing, the script asks whether you want to run:

```bash
brew install python
```

If Homebrew’s bin directory is not early enough on `PATH`, the script asks whether you want to add this to `~/.zprofile`:

```bash
export PATH="/opt/homebrew/bin:$PATH"
```

After updating `~/.zprofile`, you can apply it in your current terminal with:

```bash
source ~/.zprofile
```

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

Check with:

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
python3 -m venv .venv
source .venv/bin/activate
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

If you choose to include development tools, the script can also create:

```text
requirements-dev.txt
```

Example:

```text
-r requirements.txt

pytest
ruff
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
python3 -m venv .venv
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

## Project name vs package import name

These are not always the same.

In `pyproject.toml`:

```toml
[project]
name = "my-python-project"
```

This is the install/distribution name.

But Python imports use underscores:

```python
import my_python_project
```

So the script separates these two values:

```python
PROJECT_NAME = "my-python-project"
PACKAGE_IMPORT_NAME = "my_python_project"
```

---

## What the script teaches

### `python3 -m venv .venv`

Runs Python’s built-in `venv` module and creates a virtual environment in `.venv`.

On macOS/Linux, the script uses the `python3` found on `PATH`.

That matters because if Homebrew Python is first on `PATH`, the virtual environment will be created from Homebrew Python instead of Apple’s system Python.

### `pip install -r requirements.txt`

Installs packages listed in `requirements.txt`.

### `pip install -e .`

Installs the project in the current folder in editable mode.

### `.gitignore`

The virtual environment should not be committed to Git.

The script ensures rules like these exist:

```gitignore
.venv/
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.ruff_cache/
setup_logs/
```

### `~/.zprofile`

On macOS using the default `zsh` shell, `~/.zprofile` can be used to configure your shell environment.

For Apple Silicon Homebrew, this line puts Homebrew commands before system commands:

```bash
export PATH="/opt/homebrew/bin:$PATH"
```

That means when you run:

```bash
python3
```

your shell checks:

```text
/opt/homebrew/bin
```

before:

```text
/usr/bin
```

---

## Logs

Each run creates a timestamped log file:

```text
setup_logs/python_project_setup_YYYYMMDD_HHMMSS.log
```

The logs include:

- selected configuration
- detected operating system and architecture
- commands run
- command output
- errors, if any

The `setup_logs/` folder is ignored by Git by default.

---

## SETUP_NOTES.md

The script can write a local notes file:

```text
SETUP_NOTES.md
```

This file summarizes:

- how to activate the virtual environment
- which project style was selected
- where the virtual environment Python should live
- macOS Apple Silicon Homebrew Python notes, when relevant

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

For macOS Apple Silicon users, keep this enabled:

```python
ENABLE_MACOS_HOMEBREW_PYTHON_HELPER = True
```

---

## Deleting and recreating the environment

Virtual environments are disposable.

If something breaks:

```bash
rm -rf .venv
```

Windows PowerShell:

```powershell
Remove-Item -Recurse -Force .venv
```

Then rerun the setup script.

---

## Troubleshooting

### `python3` still points to `/usr/bin/python3`

Check all matching Python executables:

```bash
which -a python3
```

If `/usr/bin/python3` appears before `/opt/homebrew/bin/python3`, update your PATH:

```bash
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zprofile
source ~/.zprofile
```

Then check again:

```bash
which -a python3
python3 --version
```

### `brew` is installed but not found

On Apple Silicon, try:

```bash
/opt/homebrew/bin/brew --version
```

If that works, add Homebrew to PATH:

```bash
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zprofile
source ~/.zprofile
```

### The virtual environment used the wrong Python

Check the venv Python:

```bash
.venv/bin/python --version
```

On Windows:

```bash
.venv\Scripts\python.exe --version
```

If it used the wrong Python, delete `.venv`, fix your PATH, and rerun the script.

```bash
rm -rf .venv
python3 interactive_python_project_setup.py
```

### Permission issues during Homebrew install

The Homebrew installer may ask for your macOS password.

That is expected because it may need permission to create or update directories under:

```text
/opt/homebrew
```

If the installer fails, follow the official Homebrew instructions manually, then rerun this script.