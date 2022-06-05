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

## Dev Getting Started
MacOs python does not include Tcl/Tk library. To install run:
```
brew install python-tk
```

Install dependencies
```shell
poetry install
```

Run virtual shell
```
poetry shell
```

Run a program
```
python nrcemt/qeels/gui/main.py
python nrcemt/nanomi_optics/gui/main.py
python nrcemt/alignment_software/gui/main.py
```

Use flake8 to lint
```
flake8 nrcemt
```

