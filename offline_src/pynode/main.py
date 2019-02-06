# Copyright (c) 2017 Alex Socha
# https://alexsocha.github.io/pynode

import os
import shutil

# Automatic Updating
if os.path.exists(os.path.join(os.path.dirname(__file__), "src_temp")):
    shutil.rmtree(os.path.join(os.path.dirname(__file__), "src"))
    os.rename(os.path.join(os.path.dirname(__file__), "src_temp"), os.path.join(os.path.dirname(__file__), "src"))

from pynode.src import communicate
from pynode.src.launcher import *
from pynode.src.pynode_graphlib import *
