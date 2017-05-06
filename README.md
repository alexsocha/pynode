# PyNode: Graph Theory Visualizer
<a href="http://www.alexsocha.com/pynode"><img src="http://www.alexsocha.com/images/pynode/logo.png" align="left" hspace="10" vspace="6" width="100px" height="100px"></a>
**PyNode** is a Python library for visualizing Graph Theory. PyNode can be used to develop algorithm prototypes, or to demonstrate how algorithms work in a visual, interactive way. This is the full, offline version of PyNode; the online version can be found <a href="http://www.alexsocha.com/pynode">here</a>.
<br><br>

## How it works
* The main Python code interacts with the custom-designed PyNode GraphLib API, which provides all of the available Graph Theory functions.
* Python then runs pynode.exe/.app, which provides the main PyNode interface window, and communicates all changes made to the graph through standard input/output. The interface application is built in C++, using the <a href="https://bitbucket.org/chromiumembedded/cef">Chromium Embedded Framework.</a>
* The application is responsible for displaying the html interface, and running all associated JavaScript files. PyNode uses a modified version of the <a href="https://github.com/maurizzzio/greuler">Greuler API</a> for visualizing the graph, which itself uses <a href="https://github.com/tgdwyer/WebCola">WebCola</a> for layout calculation, and <a h href="https://github.com/d3/d3">D3</a> for graphics.
* All events are then handled within JavaScript. When required, information is communicated back to C++, and then back to Python.

## Project structure
* **demo.py** - A basic example of a PyNode script, and the entry point for the project. It should have the following structure:
```Python
from pynode.main import *
def run():
    # User-created PyNode script, called when the 'Play' button is pressed
begin_pynode(run)
```
* **/pynode** - The main folder for the PyNode library
  * **main.py** - Imports all relevant Python functions, and installs updates before the rest of the code is run
  * **autoupdate.txt** - Can be used to turn off automatic updating
  * **/cef** - Contains the final build of the C++ application (doesn't update automatically). Note that this folder is not available in this repository due to its large size and OS dependence. Download it <a href="http://www.alexsocha.com/pynode#download">here</a>.
    * **os.txt** - Provides the operating system of the PyNode distribution (win64/win32/macosx), allowing the correct version of the application to be run.
    * **/win64** - Binaries for 64-bit Windows.
    * **/win32** - Binaries for 32-bit Windows.
    * **/macosx** - Binaries for macOS.
  * **/cef-project** - Contains the files used for developing the C++ application. Based on the CEF project found <a href="https://bitbucket.org/chromiumembedded/cef-project">here</a>. This folder if for development only.
    * **/pynode** - Contains all C++ files, for both Windows and macOS, used in the application.
    * **/build** - Contains scripts (build_win64.bat, build_win32.bat, build_macosx.bat) which automatically generate the project for each operating system. Once run, open build/cef.sln and build the project with Visual Studio 2015 (Update 3) for Windows, or open build/cef.xcodeproj and build the project with Xcode for macOS (Note that C++11 is required, and may need to be manually specified in Xcode).
  * **/src** - Contains the main Python/HTML/JavaScript code, and will be overridden when an update is available.
    * **pynode_graphlib.py** - Contains the PyNode Graphlib API, which provides all Graph Theory-related functions. NOTE: This file should be compatible with the online version of PyNode (<a href="http://www.alexsocha.com/pynode_graphlib.py">here</a>).
    * **pynode_core.py** - Handles the internal functions of PyNode Graphlib API, and allows the pynode_graphlib.py file to be compatible with both the offline and online versions of PyNode by implementing functionality which would otherwise be unavailable (e.g. the Timer class).
    * **communicate.py** - Opens the C++ application, and communicates information through standard input, while monitoring output on a separate thread.
    * **update.py** - Downloads and unpackages updates when available.
    * **launcher.py** - Provides basic functions for initializing PyNode (e.g. begin_pynode).
    * **version.txt** - Specifies the current version of the src folder. Updates will take place when a version with a greater number is made available.
    * **/html** - Contains all HTML, JavaScript and CSS files.
      * **pynode_output.html** - The PyNode interface.
      * **/css** - Contains custom fonts and the main style sheet.
      * **/images** - Contains all icons used in the interface.
      * **/js** - Contains all JavaScript code.
        * **graph_api.js** - Contains all functions referenced by pynode_graphlib.py, and handles all updates made to the graph. Also communicates information back to C++ (and hence to Python) through the JavaScript console.
        * **d3_controls.js** - Handles interface events such as panning and zooming.
        * **resize.js** - Handles resizing of the window, and includes functions which manage node layout/positioning.
        * **/greuler** - The (modified) <a href="https://github.com/maurizzzio/greuler">Greuler API</a>.
        * **/cola** - The <a href="https://github.com/tgdwyer/WebCola">WebCola API</a>.
        * **/d3** - The <a href="https://github.com/d3/d3">D3 API</a>.
