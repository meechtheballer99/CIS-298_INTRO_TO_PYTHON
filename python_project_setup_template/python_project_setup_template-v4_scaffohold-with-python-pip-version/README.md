# Interactive Python Project Setup Helper

An educational Python project generator that teaches modern Python project structure while creating real projects.

---

# Purpose

This repository has two goals:

1. Generate Python projects.
2. Teach Python packaging concepts while doing it.

Most tutorials explain:

* virtual environments
* packages
* subpackages
* submodules
* imports
* `requirements.txt`
* `pyproject.toml`
* CLI tools

separately.

This project demonstrates all of those concepts inside a working tool.

The helper itself is built using the same package structure that it teaches.

Think of this repository as both:

* a project generator
* a Python packaging tutorial


---
## Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd python_project_setup_template
```

### 2. Create a Virtual Environment

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install the Helper

```bash
pip install -e .
```

The `-e` flag performs an **editable install**, meaning changes to the source code are immediately available without reinstalling the package.

### 4. Run the Helper

```bash
project-setup-helper
```

or:

```bash
python -m project_setup_helper
```

### 5. Follow the Interactive Prompts

The helper will guide you through:

```text
Step 1: Choose project type

  1) requirements.txt project
  2) pyproject package

Step 2: Project details

  Project name
  Minimum Python version
  Python interpreter
  Optional pip version

Step 3: Choose destination

  1) Current directory
  2) generated_projects/
  3) Custom path

Step 4: Review summary

Step 5: Generate project
```

The generated project will include a virtual environment, dependency management files, project structure, setup notes, and optional development tooling.

> Note: The generated `.venv/` directory is intentionally local to the project and should not be committed to Git.

---

## Learning Path

This project intentionally demonstrates a progression:

```text
Level 1: Single Script
Level 2: Functions
Level 3: Modules
Level 4: Packages
Level 5: Installable Package
Level 6: CLI Tool
Level 7: Project Scaffolder
```

The helper itself is a Level 6/7 project.

The projects it generates become practice environments for learning the earlier levels.

---

# Interactive Flow

Run the helper:

```bash
project-setup-helper
```

You will be guided through:

```text
Step 1: Choose project type

  1) requirements.txt project
  2) pyproject package

Step 2: Project details

  Project name
  Minimum Python version
  Python interpreter
  Optional pip version

Step 3: Choose destination

  1) Current directory
  2) generated_projects/
  3) Custom path

Step 4: Review summary

Step 5: Generate project
```

The review summary includes the selected Python requirement, Python interpreter, optional pip version, destination, and development-tool choice.

Example:

```text
Project type: pyproject
Project name: weather-cli
Package name: weather_cli
Destination:  /path/to/generated_projects/weather-cli
Python req:   >= 3.12
Interpreter:  /opt/homebrew/bin/python3.12
Pip version:  24.3.1
Dev tools:    yes
```

---

# Repository Layout

```text
python_project_setup_template/
├── README.md
├── pyproject.toml
│
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
│       ├── python_versions.py
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
│
└── generated_projects/
    └── README.md
    ├── README.md # placeholder - see info in readme regarding this directory
    ├── generated-project1    # will exist after running the helper
    ├── generated-project2    # will exist after running the helper
    └── generated-projectN... # will exist after running the helper
```

`generated_projects/` is a workspace for projects created by the helper. See `generated_projects/README.md` for details.

---

# Package Hierarchy at a Glance

This repository demonstrates how larger Python applications are organized.

```text
project_setup_helper                  ← package
│
├── prompts.py                        ← module/submodule
├── commands.py                       ← module/submodule
├── os_detect.py                      ← module/submodule
├── python_versions.py                ← module/submodule
│
├── installers                        ← subpackage
│   ├── windows.py                    ← submodule
│   ├── macos_linux.py                ← submodule
│   └── macos_apple_silicon.py        ← submodule
│
└── project_files                     ← subpackage
    ├── gitignore.py                  ← submodule
    ├── requirements.py               ← submodule
    └── pyproject.py                  ← submodule
```

As projects grow, Python code is usually organized into:

```text
Functions
    ↓
Modules
    ↓
Packages
    ↓
Subpackages
    ↓
Submodules
```

Understanding this hierarchy is essential for understanding imports.

---

# Python Terminology

Before going deeper, here is the short version:

```text
File                         → Module
Directory package            → Package
Package inside a package     → Subpackage
Module inside a package      → Submodule
Module inside a subpackage   → Submodule
```

---

## What Is a Module?

A module is a single Python file.

Examples:

```text
cli.py
prompts.py
commands.py
venv_tools.py
```

Example:

```python
# prompts.py

def ask_yes_no(prompt: str) -> bool:
    ...
```

---

## What Is a Package?

A package is a directory containing Python modules.

Example:

```text
project_setup_helper/
├── __init__.py
├── cli.py
├── prompts.py
└── commands.py
```

The package groups related modules together.

---

## What Is a Subpackage?

Packages can contain other packages.

Example:

```text
project_setup_helper/
└── installers/
    ├── __init__.py
    ├── windows.py
    └── macos_apple_silicon.py
```

Here:

```text
project_setup_helper
```

is the package.

```text
installers
```

is a subpackage.

---

# What Is a Submodule?

A submodule is simply a module that lives inside a package or subpackage.

Example:

```text
project_setup_helper/
├── prompts.py
├── commands.py
│
└── installers/
    ├── windows.py
    └── macos_apple_silicon.py
```

These are all submodules:

```text
project_setup_helper.prompts
project_setup_helper.commands
project_setup_helper.installers.windows
project_setup_helper.installers.macos_apple_silicon
```

Python identifies modules by their full dotted path.

---

## Visualizing the Hierarchy

```text
project_setup_helper
│
├── prompts
├── commands
├── os_detect
│
└── installers
    │
    ├── windows
    └── macos_apple_silicon
```

Think of each dot as moving one level deeper:

```python
project_setup_helper.installers.windows
```

means:

```text
package
    ↓
subpackage
    ↓
module
```

---

## Importing a Submodule

Import a specific function:

```python
from project_setup_helper.installers.windows import (
    run_windows_check,
)
```

Python resolves:

```text
project_setup_helper
    ↓
installers
    ↓
windows.py
    ↓
run_windows_check()
```

---

## Importing the Entire Submodule

You can import the whole submodule:

```python
import project_setup_helper.installers.windows
```

Usage:

```python
project_setup_helper.installers.windows.run_windows_check()
```

---

## Importing a Submodule With an Alias

Long paths are often shortened:

```python
import project_setup_helper.installers.windows as win
```

Usage:

```python
win.run_windows_check()
```

This is common when the full package path is long.

---

## Why Submodules Exist

Imagine placing every function in one file:

```text
project_setup_helper/
└── everything.py
```

After a few months:

```text
everything.py
```

might be:

```text
3,000+ lines
```

and difficult to navigate.

Instead we separate responsibilities:

```text
project_setup_helper/
├── prompts.py
├── commands.py
├── os_detect.py
├── venv_tools.py
│
├── installers/
│   ├── windows.py
│   └── macos_apple_silicon.py
│
└── project_files/
    ├── gitignore.py
    ├── requirements.py
    └── pyproject.py
```

Each submodule has one primary responsibility.

This is called:

```text
Separation of Concerns
```

and is one of the main reasons packages exist.

---

## Real Example From This Repository

When the CLI starts, it may import several submodules:

```python
from project_setup_helper.prompts import ask_choice
from project_setup_helper.venv_tools import create_virtual_environment
from project_setup_helper.project_files.pyproject import (
    create_pyproject_package,
)
```

Notice that:

```text
project_setup_helper.prompts
```

is a submodule.

And:

```text
project_setup_helper.project_files.pyproject
```

is a submodule inside a subpackage.

This demonstrates how larger Python applications are organized.

---

## Package → Subpackage → Submodule

Using this repository:

```text
project_setup_helper
│
├── prompts.py
│
└── project_files
    │
    └── pyproject.py
```

The hierarchy becomes:

```text
Package:
    project_setup_helper

Subpackage:
    project_files

Submodule:
    pyproject
```

Which Python references as:

```python
project_setup_helper.project_files.pyproject
```

Understanding this dotted path notation is one of the most important skills when learning larger Python projects.

---

# Understanding Imports

Python imports code from modules and packages.

---

## Import a Function

```python
from project_setup_helper.prompts import ask_yes_no
```

Usage:

```python
answer = ask_yes_no("Continue?")
```

---

## Import Multiple Functions

```python
from project_setup_helper.prompts import (
    ask_yes_no,
    ask_choice,
    pause,
)
```

---

## Import a Module

```python
import project_setup_helper.prompts
```

Usage:

```python
project_setup_helper.prompts.ask_yes_no(
    "Continue?"
)
```

---

## Import With an Alias

```python
import project_setup_helper.prompts as prompts
```

Usage:

```python
prompts.ask_yes_no("Continue?")
```

Another common example:

```python
import pathlib as pl

root = pl.Path.cwd()
```

---

## Relative Imports

Inside packages:

```python
from .prompts import ask_yes_no
```

The dot means:

```text
Current package
```

Example:

```python
from .commands import run_command
```

---

## Relative Imports With Two Dots

```python
from ..installers.windows import run_windows_check
```

Means:

```text
Move up one package level
Then import windows
```

---

## Avoid Wildcard Imports

Avoid:

```python
from prompts import *
```

Prefer:

```python
from project_setup_helper.prompts import ask_yes_no
```

or:

```python
import project_setup_helper.prompts as prompts
```

---

# Understanding `__init__.py`

One of the most important files in Python packaging is:

```text
__init__.py
```

Example:

```text
project_setup_helper/
├── __init__.py
├── cli.py
└── prompts.py
```

---

## Minimal `__init__.py`

```python
# __init__.py
```

An empty file is valid.

---

## Package Metadata

```python
# __init__.py

__version__ = "0.1.0"
__author__ = "Demetrius Johnson"
```

Usage:

```python
import project_setup_helper

print(project_setup_helper.__version__)
```

---

## Re-exporting Functions

```python
# prompts.py

def ask_yes_no():
    ...
```

```python
# __init__.py

from .prompts import ask_yes_no
```

Now:

```python
from project_setup_helper import ask_yes_no
```

works.

---

## Package API Design

Many libraries use `__init__.py` to create a cleaner public API.

Instead of:

```python
from package.module.submodule import thing
```

users can write:

```python
from package import thing
```

because `__init__.py` re-exports it.

---

# Understanding `__main__.py`

The second special file is:

```text
__main__.py
```

Example:

```text
project_setup_helper/
├── __init__.py
├── __main__.py
└── cli.py
```

---

## Typical `__main__.py`

```python
from project_setup_helper.cli import main

if __name__ == "__main__":
    main()
```

Its job is simple:

```text
Run the application's main entry point.
```

---

## Why `__main__.py` Exists

Because Python supports:

```bash
python -m package_name
```

Example:

```bash
python -m project_setup_helper
```

Python automatically looks for:

```text
project_setup_helper.__main__
```

and executes it.

---

## Execution Flow

```text
python -m project_setup_helper

        │
        ▼

Find package

        │
        ▼

Find __main__.py

        │
        ▼

Run __main__.py

        │
        ▼

Call cli.main()
```

---

# Running Files vs Running Packages

These are different.

---

## Running a File

```bash
python script.py
```

Python executes:

```text
script.py
```

directly.

---

## Running a Package

```bash
python -m project_setup_helper
```

Python executes:

```text
project_setup_helper/__main__.py
```

instead.

---

# Why This Repo Uses a `src` Layout

The package lives here:

```text
src/project_setup_helper/
```

instead of:

```text
project_setup_helper/
```

directly in the repository root.

This is called the:

```text
src layout
```

---

## Benefits

The `src` layout:

* prevents accidental imports
* matches installed behavior
* encourages proper packaging
* is common in professional projects

Example:

```text
repo/
├── pyproject.toml
├── README.md
└── src/
    └── project_setup_helper/
```

---

# Installation

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install:

```bash
pip install -e .
```

---

# What Does `-e` Mean?

```bash
# optional: upgrade pip first
pip install --upgrade pip
# now install the package from local repo in editable mode
pip install -e .
```

means:

```text
Editable install
```

Python creates a link to the source code rather than copying it.

That means changes to:

```text
src/project_setup_helper/
```

are immediately available.

No reinstall is required.

---

# How the CLI Command Appears

Inside:

```text
pyproject.toml
```

there is:

```toml
[project.scripts]
project-setup-helper = "project_setup_helper.cli:main"
```

This tells Python:

```text
Create a terminal command named:

project-setup-helper

When executed:

Import project_setup_helper.cli

Call main()
```

Conceptually:

```python
from project_setup_helper.cli import main

main()
```

---

# Python and Pip Versions

The helper separates three related ideas:

```text
Python requirement
    The version your project says it supports.

Python interpreter
    The actual Python executable used to create `.venv/`.

Pip version
    The version of pip installed inside `.venv/`.
```

For package projects, the Python requirement is written to `pyproject.toml`:

```toml
requires-python = ">=3.12"
```

This tells users and tools that the project expects Python 3.12 or newer.

---

## Installing Multiple Python Versions with Homebrew

On macOS Apple Silicon, Homebrew allows multiple Python versions to coexist.

Examples:

```bash
brew install python@3.11
brew install python@3.12
brew install python@3.13
```

Verify installed versions:

```bash
brew list | grep python
```

You can also inspect a specific version:

```bash
brew info python@3.12
```

Typical Homebrew Python executables:

```text
/opt/homebrew/bin/python3.11
/opt/homebrew/bin/python3.12
/opt/homebrew/bin/python3.13
```

Verify each version:

```bash
/opt/homebrew/bin/python3.11 --version
/opt/homebrew/bin/python3.12 --version
/opt/homebrew/bin/python3.13 --version
```

Homebrew does not automatically switch your active Python version when multiple versions are installed.

Instead, each version remains available as its own executable:

```text
/opt/homebrew/bin/python3.11
/opt/homebrew/bin/python3.12
/opt/homebrew/bin/python3.13
```

The helper uses the specific interpreter you select rather than attempting to modify your system-wide Python configuration.

If a Python version is not installed through Homebrew (or otherwise available on your machine), the helper cannot create a virtual environment using that version until it is installed.

---

## Homebrew Python Versions and the Helper

The helper can only select Python interpreters that already exist on your system.

For macOS Apple Silicon users, the recommended approach is:

```text
Install Python version with Homebrew
    ↓
Verify installation
    ↓
Select interpreter in helper
    ↓
Create virtual environment
```

For example:

```bash
brew install python@3.12
```

Verify:

```bash
/opt/homebrew/bin/python3.12 --version
```

Then select:

```text
Python interpreter:
    /opt/homebrew/bin/python3.12
```

The helper will create the virtual environment using:

```bash
/opt/homebrew/bin/python3.12 -m venv .venv
```

and record that information in the generated setup notes.

---

## Creating a Virtual Environment Manually

If you want to create a virtual environment using a specific Python version:

```bash
/opt/homebrew/bin/python3.12 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Verify the version inside the virtual environment:

```bash
python --version
```

Expected output:

```text
Python 3.12.x
```

This guarantees the project is using Python 3.12 regardless of whatever other Python versions are installed on the machine.

---

## Creating a Virtual Environment with the Helper

The helper can perform this step for you.

During project creation, you may choose:

```text
Python interpreter:
  1) Current Python interpreter
  2) python3 from PATH
  3) Specific executable path
  4) Homebrew Python
```

For example:

```text
/opt/homebrew/bin/python3.12
```

The helper will then create the virtual environment using:

```bash
/opt/homebrew/bin/python3.12 -m venv .venv
```

and record that information in the generated setup notes.

---

## What Happens If Versions Do Not Match?

Consider this configuration:

```toml
[project]
requires-python = ">=3.12"
```

but the virtual environment is created using:

```bash
/opt/homebrew/bin/python3.11 -m venv .venv
```

The virtual environment itself will still be created successfully.

However, problems may appear later:

```text
Create venv
    ✓ succeeds

Install dependencies
    ✓ may succeed

Install package
    ✗ may fail

Run application
    ✗ may fail
```

Many modern packages check:

```toml
requires-python
```

during installation.

For example:

```toml
requires-python = ">=3.12"
```

If your virtual environment is using Python 3.11, package installation may fail with an error indicating that the active interpreter does not satisfy the project's declared Python requirement.

In other words:

```text
Project Requirement:
    Python >=3.12

Virtual Environment:
    Python 3.11

Result:
    Configuration mismatch
```

The virtual environment itself can still be created successfully, but the project may not install or run correctly.

A future version of the helper may warn when:

```text
Minimum Python Version:
    3.12

Selected Interpreter:
    Python 3.11
```

because the selected interpreter does not satisfy the declared project requirement.

---

## Recommended Practice

Keep these values aligned:

```text
Project Requirement:
    >=3.12

Virtual Environment:
    Python 3.12

Pip:
    Latest or pinned version
```

In other words:

```text
Choose Python requirement
    ↓
Install that Python version
    ↓
Create venv using that interpreter
    ↓
Install dependencies
    ↓
Develop and run project
```

This is the workflow the helper is designed to encourage.

---

## Managing Pip Inside the Virtual Environment

Once the virtual environment exists, pip is managed inside that environment.

Upgrade to the latest pip:

```bash
.venv/bin/python -m pip install --upgrade pip
```

Or install a specific pip version:

```bash
.venv/bin/python -m pip install --upgrade pip==24.3.1
```

Verify the active pip version:

```bash
python -m pip --version
```

Because pip is running inside `.venv`, these changes do not affect your system-wide Python installation.

---

## Putting It All Together

This teaches an important distinction:

```text
Choose Python version
    ↓
Select Python interpreter
    ↓
Create virtual environment
    ↓
Upgrade or pin pip
    ↓
Install project dependencies
    ↓
Run project
```

For example:

```text
Python Requirement:
    >=3.12

Python Interpreter:
    /opt/homebrew/bin/python3.12

Pip Version:
    24.3.1

Virtual Environment:
    .venv/
```

All four values are related, but they serve different purposes and should be understood separately.


# Three Ways To Run The Helper

## Method 1

```bash
project-setup-helper
```

Uses:

```toml
[project.scripts]
```

---

## Method 2

```bash
python -m project_setup_helper
```

Uses:

```text
__main__.py
```

---

## Method 3: Direct file execution

This is not recommended for normal use because package-relative imports may not behave the same way as installed execution.

Prefer: `python -m project_setup_helper`

```bash
python src/project_setup_helper/cli.py
```

Development only.

Not typically used after installation.

---

# Generated Requirements Project

Example:

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
```

The generated README and setup notes also record the selected Python requirement, Python interpreter, and pip version used for the project.

Run:

```bash
source .venv/bin/activate
python main.py
```

Windows:

```powershell
.venv\Scripts\activate
python main.py
```

When a user pulls your repo, they can simply create a virtual environment:

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Then install the dependencies into the virtual environment from `requirements.txt`:

```bash
pip install -r requirements.txt
```

If the project also includes development dependencies:

```bash
pip install -r requirements-dev.txt
```

Verify the installed packages:

```bash
pip list
```

Then run the application:

```bash
python main.py
```

Because the virtual environment is activated, all packages are installed only inside `.venv/` and do not affect your system-wide Python installation.

Overall, the workflow using requirements.txt project is as follows:

```text
Create venv
    ↓
Activate venv
    ↓
Install dependencies
    ↓
Verify installation
    ↓
Run application
```
---

# Generated Package Project

Example:

```text
weather-cli/
├── .gitignore
├── .venv/
├── README.md
├── pyproject.toml
├── src/
│   └── weather_cli/
│       ├── __init__.py
│       ├── __main__.py
│       └── cli.py
├── tests/
└── setup_logs/
```

Install:

```bash
pip install -e .
```

Run:

```bash
weather-cli Demetrius
```

or:

```bash
python -m weather_cli Demetrius
```

When a user pulls your repo, they can create and activate a virtual environment:

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Then install the package into the virtual environment:

```bash
pip install -e .
```

If the project includes development dependencies:

```bash
pip install -e ".[dev]"
```

The `-e` flag means:

```text
Editable Install
```

Rather than copying the package into the virtual environment, Python creates a link to the source code.

This means changes made to:

```text
src/weather_cli/
```

are immediately available without reinstalling the package.

Verify the installation:

```bash
pip list
```

You should see:

```text
weather-cli
```

among the installed packages.

Run the CLI command:

```bash
weather-cli Demetrius
```

or execute the package directly:

```bash
python -m weather_cli Demetrius
```

Because the package is installed in editable mode, changes to the source code are available immediately:

```text
Edit code
    ↓
Save file
    ↓
Run command again
```

No reinstall is required.

Overall, the workflow using a pyproject.toml package is as follows:

```text
Create venv
    ↓
Activate venv
    ↓
Install package (editable mode)
    ↓
Verify installation
    ↓
Run CLI command
    ↓
Edit source code
    ↓
Run again without reinstalling
```


---

# macOS Apple Silicon Support

The helper includes dedicated support for:

* Homebrew detection
* Homebrew Python installation
* PATH verification
* Python resolution checks
* optional Homebrew `python@3.x` interpreter selection

Relevant submodule:

```text
project_setup_helper.installers.macos_apple_silicon
```

File path:

```text
src/project_setup_helper/installers/macos_apple_silicon.py
```

The goal is to help ensure virtual environments are created using Homebrew-managed Python rather than Apple's system Python.

---

# Testing

Compile-check:

```bash
python -m compileall src tests
```

Run tests:

```bash
pytest
```

or:

```bash
PYTHONPATH=src pytest
```

---

# Summary

This repository intentionally demonstrates:

```text
Functions
    ↓
Modules
    ↓
Imports
    ↓
Packages
    ↓
Subpackages
    ↓
Submodules
    ↓
Virtual Environments
    ↓
Editable Installs
    ↓
Python Version Requirements
    ↓
Pip Version Management
    ↓
pyproject.toml
    ↓
CLI Entry Points
    ↓
Project Scaffolding
```

The helper is both a working tool and a complete example of modern Python project structure.
