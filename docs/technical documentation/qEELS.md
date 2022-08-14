# qEELS Technical Documentation

## System Architecture

This software is contained in one large package with two other software: NanoMi Optics and Tomography Alignment Software. For each software, there is a GUI and an engine package. The engine package contains all of the core logic, processing, and math behind the software. The engine must have zero dependencies on the GUI packages and GUI libraries. The GUI package focuses on handling user interaction and displays. There are also two other packages: testing and common. The testing package holds all of the tests that are run on the software. The common package holds shared common functions that are reused across the software.

Learn more about the system architecture in the Design document on this project’s GitHub repository.

## Engine Code Explanation

-The engine code does not have any dependencies on the GUI.

**Notable differences:**
There are some notable differences in the MATLAB and Python code. This does not necessarily mean that the Python calculations are incorrect. The packages used in the Python code are not exactly the same as the MATLAB, meaning that calculations will not be executed in the exact same way. To ensure code quality and correct calculations, make sure that all values are thoroughly tested and reviewed.

Differences:
- Python optimization sometimes produces a different(better) result than MATLAB result
- Detect selection boxes auto fill
- Added contrast adjustments to spectrogram/spectrum
- Added dropdown menu for selecting material type

**Tools:** Various tools are used in the engine.

How tools are used in engine:
- Scipy optimizations - Uses scipy's least squares optimization for all the calculated results (ev/pixel, micro-rad/pixel(upper and lower))
- Scipy transformations - used scipy's ndimage transformations in intermediate steps of peak detection to help with calculations(peak position calculations)
- MatplotLib - Used for rendering and drawing(both boxes and points) on the spectrogram/spectrum

**Testing:**
Each mathematical expression and method must be tested using unit testing. Use test cases that cover a variety of inputs and outputs. NumPy’s test support allows for test scripts to be  imported and work right away. Use these assertions to test functions.
