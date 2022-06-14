# COSC 499 Project 2 NRC Electron Microscope Tools

A set of in-development Python tools ported from Matlab for calibrating and processing electron microscope imagery.

## Documentation

- [Scope & Charter](./docs/scope-charter)
- [Design](./docs/design)
- [Communication](./docs/communication)
- [Weekly Logs](./docs/weekly%20logs)
- [Final](./docs/communication)

## Team Members

- Garrett Cook 
- Jasmine Mishra 
- Jose Pena Revelo
- Lucas Towers

## Windows Installation

1. Install a stable version of [Python 3](https://www.python.org/downloads/windows/) (must be >=3.9)
2. Make sure Python is [available in the command prompt](https://docs.python.org/3/using/windows.html#finding-the-python-executable)
3. Extract the full source code to a folder on your device.
4. See the [scripts](./scripts) folder for one-click installation and launch scripts.

## Mac/Linux Installation

1. Install a stable version of Python 3 (must be >=3.9), using a package manager such as `brew` or `apt` is recommended.
   - `brew install python@3.9`
   - `sudo apt install python3.9`
2. Install supporting libraries for Tcl/Tk
   - `brew install python-tk`
   - `sudo apt install python3-tk`
3. Ensure `pip` is installed
   - `python -m ensurepip`
4. Extract the full source code to a directory on your device.
5. Install the nrcemt python package
   - `python -m pip install path/to/source/directory`

## Run via command line

```shell
python -m nrcemt.qeels.gui.main
python -m nrcemt.nanomi_optics.gui.main
python -m nrcemt.alignment_software.gui.main
```

## Development Environment

1. Install [Poetry](https://python-poetry.org/docs/#installation) for Python
2. Clone the repository and `cd` into it
3. Install dependencies with `poetry install`
4. Enter a virtual shell with `poetry shell`

## Useful Development Commands

- Run all tests: `pytest`
- Lint all code: `flake8 nrcemt`
