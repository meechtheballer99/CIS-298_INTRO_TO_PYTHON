# Interactive Python Project Setup Helper

This repo is an educational Python project generator.

It does two things at once:

1. It helps create a new Python project.
2. It teaches how Python modules, packages, imports, virtual environments, `requirements.txt`, `pyproject.toml`, and CLI entry points work.

The helper itself is packaged using the `src/` layout so the repo demonstrates the same packaging ideas it teaches.

---

## What changed from the single-script version

The original version was one working script. This version is an installable package with modules and subpackages.

Instead of editing a large CONFIG section first, you run the helper and answer prompts:

```text
Step 1: Choose project type

  1) requirements.txt project
  2) pyproject package

Step 2: Choose project name

Step 3: Choose destination

  1) Current directory
  2) generated_projects/
  3) Custom path

Step 4: Generate project
```

This makes the tool feel more like a real project scaffolder while still staying beginner-friendly.

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
│       ├── prompts.py
│       ├── commands.py
│       ├── logging_setup.py
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

## What each part teaches

```text
src/project_setup_helper/
```

This is the main Python package.

```text
installers/
project_files/
```

These are subpackages.

```text
cli.py
config.py
prompts.py
commands.py
```

These are modules.

```python
from project_setup_helper.project_files.pyproject import create_pyproject_package
```

This teaches imports across packages and modules.

---

## Install for development

From this repo folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

On Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

The `-e` means editable install. When you edit files under `src/project_setup_helper/`, the installed command sees those changes immediately.

---

## Run the helper

After installing in editable mode:

```bash
project-setup-helper
```

You can also run it as a module:

```bash
python -m project_setup_helper
```

The package supports module execution because it includes:

```text
src/project_setup_helper/__main__.py
```

---

## The interactive flow

### Step 1: Choose project type

```text
1) requirements.txt project
2) pyproject package
```

Use `requirements.txt` for simple scripts and beginner projects.

Use `pyproject.toml` for installable packages, reusable tools, or command-line programs.

---

### Step 2: Choose project name

Example:

```text
weather-cli
```

The helper teaches the difference between the distribution name and the import package name:

```text
Distribution/folder name: weather-cli
Import package name:      weather_cli
```

This matters because Python imports cannot use hyphens:

```python
import weather_cli
```

---

### Step 3: Choose destination

```text
1) Current directory
2) generated_projects/
3) Custom path
```

The default is `generated_projects/` so beginners can safely create multiple examples without cluttering the helper repo root.

Example result:

```text
generated_projects/
└── weather-cli/
```

---

### Step 4: Generate project

Before writing files, the helper shows a review summary:

```text
Project type: pyproject
Project name: weather-cli
Package name: weather_cli
Destination:  /path/to/generated_projects/weather-cli
Dev tools:    yes
```

Then it creates the selected project.

---

## Generated layout: requirements.txt project

If you choose `requirements.txt project`, the helper creates something like:

```text
weather-scraper/
├── .gitignore
├── .venv/
├── README.md
├── main.py
├── requirements.txt
├── requirements-dev.txt
├── SETUP_NOTES_YYYYMMDD_HHMMSS.md
└── setup_logs/
    └── python_project_setup_YYYYMMDD_HHMMSS.log
```

Run it with:

```bash
source .venv/bin/activate
python main.py
```

On Windows:

```powershell
.venv\Scripts\activate
python main.py
```

---

## Generated layout: pyproject package

If you choose `pyproject package`, the helper creates something like:

```text
weather-cli/
├── .gitignore
├── .venv/
├── README.md
├── pyproject.toml
├── SETUP_NOTES_YYYYMMDD_HHMMSS.md
├── setup_logs/
│   └── python_project_setup_YYYYMMDD_HHMMSS.log
├── src/
│   └── weather_cli/
│       ├── __init__.py
│       ├── __main__.py
│       └── cli.py
└── tests/
    └── test_cli.py
```

Run it with:

```bash
source .venv/bin/activate
pip install -e .
weather-cli Demetrius
```

Or:

```bash
python -m weather_cli Demetrius
```

---

## Why generated projects are not timestamped by default

The generated project folder should look like a real project:

```text
weather-cli/
├── pyproject.toml
├── src/
└── tests/
```

That is more useful than hiding the real layout inside a timestamped folder.

The timestamped files are logs and setup notes:

```text
setup_logs/python_project_setup_YYYYMMDD_HHMMSS.log
SETUP_NOTES_YYYYMMDD_HHMMSS.md
```

This keeps the project layout realistic while still preserving a history of each helper run.

---

## macOS Apple Silicon support

On Apple Silicon Macs, Apple's system-managed Python is usually located at:

```text
/usr/bin/python3
```

For development, you usually want Homebrew Python instead:

```text
/opt/homebrew/bin/python3
```

The helper includes a macOS Apple Silicon module that can check:

- whether Homebrew is installed
- whether Homebrew Python is installed
- whether `/opt/homebrew/bin` appears before `/usr/bin` on `PATH`
- which `python3` will be used to create the virtual environment

The related code lives here:

```text
src/project_setup_helper/installers/macos_apple_silicon.py
```

---

## Windows support

The helper uses Windows-specific virtual environment paths when running on Windows:

```text
.venv\Scripts\python.exe
.venv\Scripts\activate
```

The Windows-specific extension point lives here:

```text
src/project_setup_helper/installers/windows.py
```

---

## Development checks

Compile-check the package:

```bash
python -m compileall src tests
```

Run tests:

```bash
PYTHONPATH=src pytest
```

Or, after installing development tools:

```bash
pytest
```

---

## Teaching progression

This repo supports this learning path:

```text
Level 1: single script
Level 2: functions
Level 3: modules
Level 4: package
Level 5: installable CLI tool
Level 6: project scaffolder
```

The helper is now both the lesson and the tool that creates the next practice project.
