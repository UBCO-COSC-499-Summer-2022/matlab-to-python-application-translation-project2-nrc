# Tomography Alignment Software Technical Documentation

## System Architecture

This software is contained in one large package with two other software: NanoMi Optics and qEELS. For each software, there is a GUI and an engine package. The engine package contains all of the core logic, processing, and math behind the software. The engine must have zero dependencies on the GUI packages and GUI libraries. The GUI package focuses on handling user interaction and displays.

Learn more about the system architecture in the Design document on this project’s GitHub repository.

## Engine Code Explanation

The engine code does not have any dependencies on the GUI.

**Notable differences:**
There are some notable differences in the MATLAB and Python code. This does not necessarily mean that the Python calculations are incorrect. The packages used in the Python code are not exactly the same as the MATLAB, meaning that calculations will not be executed in the exact same way. To ensure code quality and correct calculations, make sure that all values are thoroughly tested and reviewed.

Differences:
+ Improved automatic contrast adjustment
+ Image display is kept in main window rather than drawing images in each step's window
+ Move transforms into their own window
+ Transforms can be controlled by sliders rather than text entries
+ Previewing transforms before coarse alignment
+ Prevent parts of the image from getting cut off after multiple transforms
+ Revamp how automatic tracking works
+ Add interpolation options to automatic and manual tracking
+ Add restore previous session button, rather than restoring without being asked
- Remove cropping options from optimize step (not needed anymore)

**Tools:** Various tools are used in the engine.

How tools are used:

- Matplotlib used for rendering all graphs and images.
- Pillow for saving intermediate tiff images
- Scipy ndimage affine transforms for manipulating images
- SciPy optimize for final optimization step
- SciPy convolve2d for particle tracking

**Testing:**
Each mathematical expression and method must be tested using unit testing. Use test cases that cover a variety of inputs and outputs. NumPy’s test support allows for test scripts to be  imported and work right away. Use these assertions to test functions.