# PyNode: Graph Theory Visualizer
<a href="https://alexsocha.github.io/pynode/"><img src="https://alexsocha.github.io/pynode/images/logo.png" align="left" hspace="10" vspace="6" width="100px" height="100px"></a>
**PyNode** is a Python library for visualizing Graph Theory. It can be used to develop algorithm prototypes, or to demonstrate how algorithms work in a visual, interactive way. It is available in both an online version (current directory) and offline version (<a href="https://github.com/alexsocha/pynode/tree/master/offline_src">/offline_src</a>). The official website can be found <a href="https://alexsocha.github.io/pynode">here</a>.
<br><br>

## How It Works
### Online Version
* When the 'Play' button is pressed, the Python code written in the editor (provided by <a href="https://ace.c9.io/#nav=about">Ace</a>) is transpiled to JavaScript (using <a href="https://github.com/mauriciopoppe/greuler">Brython</a>).
* The code is then executed instantaneously, and all API calls are added to a queue, ready to be executed sequentially.
* The API calls trigger visual animations (using a modified version of <a href="https://github.com/maurizzzio/greuler">Greuler</a>, built on <a href="https://github.com/d3/d3">D3</a> and <a href="https://github.com/tgdwyer/WebCola">WebCola</a>).

## Project Structure
### Online Version
* **pynode_graphlib.py\*** - The PyNode Graphlib API, which provides all Graph-related functions. This file maintains the current state of the graph, and informs graph_api.js of all the events that need to be visually displayed.
* **pynode_core.py** - Handles the internal functions of the API, and acts as a bridge between pynode_graphlib.py and graph_api.js, allowing the API to be compatible with both the online and offline versions of PyNode.
* **index.html** - The main page of the online version, which includes the editor, console, and output window. Also provides documentation for all features.
* **pynode_editor.html, pynode_console.html, pynode_output.html** - Detachable editor/console/output windows.
* **pynode_pojects/** - Contains the Python code for the examples provided on the website.
* **/css/\*** - Contains custom fonts and the main style sheet.
* **/images/pynode\*** - Contains all icons used in the interface.
* **/js/\*** - Contains all JavaScript code.
    * **graph_api.js** - Visually updates the graph, in parallel with the calls that were made to the GraphLib API.
    * **d3_controls.js** - Handles interface events such as panning and zooming.
    * **resize.js** - Handles resizing of the window, and includes functions which manage node layout/positioning.
    * **/greuler** - The (modified) <a href="https://github.com/maurizzzio/greuler">Greuler API</a>.
    * **/cola** - The <a href="https://github.com/tgdwyer/WebCola">WebCola API</a>.
    * **/d3** - The <a href="https://github.com/d3/d3">D3 API</a>.
### Offline Version
* **offline_src/** - Contains the source code for the offline version of PyNode. Further details are provided within the directory.
* **offline_downloads/** - Contains packaged downloads for the offline version.
    * **latest_version.zip** - Contains the latest version of the <a href="https://github.com/alexsocha/pynode/tree/master/offline_src/pynode/src">/offline_src/pynode/src</a> folder packaged in a zip file, allowing for automatic updates.
    * **latest_version.txt** - Specifies the current version number.
    * **pynode_win64.zip, pynode_macosx.zip, etc.** - Contains the fully packaged offline versions of PyNode for various operating systems.

_\* These files should be kept in sync between the online and offline versions._

## Publishing
All pull requests and changes should be made to the master branch. Once thoroughly tested, changes in the master branch should be pushed to the gh-pages branch, and can be viewed at <a href="https://alexsocha.github.io/pynode/">alexsocha.github.io/pynode</a>.

### Offline Version
If changes are made to files that are also used in the offline version (indicated by a '\*'), the corresponding files in the <a href="https://github.com/alexsocha/pynode/tree/master/offline_src">/offline_src</a> folder should also be updated, and the procedure for publishing the offline version (specifically the "PyNode Files" section) should be followed.
