# NanoMi Optics Technical Documentation

## System Architecture

This software is contained in one large package with two other software: qEELS and Tomography Alignment Software. For each software, there is a GUI and an engine package. The engine package contains all of the core logic, processing, and math behind the software. The engine must have zero dependencies on the GUI packages and GUI libraries. The GUI package focuses on handling user interaction and displays.

Learn more about the system architecture in the Design document on this project’s GitHub repository.

## Engine Code Explanation

The engine code does not have any dependencies on the GUI.

**Notable differences:**
There are some notable differences in the MATLAB and Python code. This does not necessarily mean that the Python calculations are incorrect. The packages used in the Python code are not exactly the same as the MATLAB, meaning that calculations will not be executed in the exact same way. To ensure code quality and correct calculations, make sure that all values are thoroughly tested and reviewed.

Differences:
- One single window GUI separated by frames
- Result table at the top of the window that summarizes the settings for all lenses
- Keeps the same ray color between the input and output ray, now just line thickness changes
- The output image for each lens is plotted with a black line
- The optimization tolerances settings are lower and the optimizer is finds values very close to zero or even zero

**Tools:** Various tools are used in the engine.

How tools are used:
- Matplotlib: used for rendering and drawing lenses, focal lengths, ray paths, and magnification
- Scipy optimization: after selecting a lens the optimizer will use least squares in two different ways:
  - Image mode: for the selected lens, it will find a focal length that brings the red ray as close to zero in the scintillator
  - Diffraction mode: for the selected lens, it will find a focal length that brings the red and green ray as close to each other in the scintillator

**Testing:**
Each mathematical expression and method must be tested using unit testing. Use test cases that cover a variety of inputs and outputs. NumPy’s test support allows for test scripts to be  imported and work right away. Use these assertions to test functions.
