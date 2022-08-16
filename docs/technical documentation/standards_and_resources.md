# Tkinter Standards

The GUI layout is closely related to the legacy MATLAB code, but with some improvements for better usability. The majority of the GUI is programmed using Tkinter.

Follow these practices to standardize Tkinter code:
- Always comment each method.
- Use object oriented Tkinter.
- Always use pack or grid immediately after creating a widget.
- If a widget uses grid layout, perform row and column configuration at the top of the constructor.
- When a specific padding value is repeated many times, use a constant.
- Use ttk for most widgets.
- Use tk for frames.
- Use tk Scale when discrete slider values are needed.
- For sub-windows use tk.TopLevel.
- Configuration of window geometry and title should be done in the window's constructor.
- Do not use place for widget placement.
- Do not use tk.Style.

**Testing:**
Test each call made from the GUI to the engine. Usability testing.

# Resources

Learn how to use GitHub and Git workflow:
https://docs.github.com/en 
https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow 

The three software use various packages and libraries. Use the following linked documentation to learn more:

Tkinter - https://tkdocs.com 
https://docs.python.org/3/library/tk.html 
Matplotlib - https://matplotlib.org/stable/index.html 
NumPy- https://numpy.org/doc/
SciPy - https://docs.scipy.org/doc/scipy/ 
Flake8 - https://flake8.pycqa.org/en/latest/ 
Poetry - https://python-poetry.org/docs/basic-usage/ 

# Standards

There are some standard practices in place to keep the code style and quality consistent across the qEELS, NanoMi Optics, and Tomography Alignment Software:
tKinter standardization
Linting, using Flake8
Thorough testing practices