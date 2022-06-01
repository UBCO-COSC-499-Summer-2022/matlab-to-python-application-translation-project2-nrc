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

Install dependencies

```shell
pipenv install
```

Run virtual shell

```
pipenv shell
```

Install package

```
pip install -e .
```

Run a program

```
python -m nrcemt.alignment_software.main
```

After you're done programming run linter:

```
flake8 script_name.py
```

