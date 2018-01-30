#!/bin/bash
cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release ..
make -j4 cefclient cefsimple

