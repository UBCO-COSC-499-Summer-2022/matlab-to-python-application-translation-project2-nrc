# Tomography Alignment Software Technical Documentation

## System Architecture

This software is contained in one large package with two other software: NanoMi Optics and Tomography Alignment Software. For each software, there is a GUI and an engine package. There is also a common package that shares common functions that are reused across the software. The engine package contains all of the core logic, processing, and math behind the software. The engine must have zero dependencies on the GUI packages and GUI libraries. The GUI package focuses on handling user interaction and displays. 

Learn more about the system architecture in the Design document on this project’s GitHub repository.

## Engine Code Explanation

The engine code does not have any dependencies on the GUI.

**Notable differences:**
There are some notable differences in the MATLAB and Python code. This does not necessarily mean that the Python calculations are incorrect. The packages used in the Python code are not exactly the same as the MATLAB, meaning that calculations will not be executed in the exact same way. To ensure code quality and correct calculations, make sure that all values are thoroughly tested and reviewed.

**Testing:**
Each mathematical expression and method must be tested using unit testing. Use test cases that cover a variety of inputs and outputs. NumPy’s test support allows for test scripts to be  imported and work right away. Use these assertions to test functions.