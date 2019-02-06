# Copyright (c) 2017 Alex Socha
# https://alexsocha.github.io/pynode

import os
import shutil
import zipfile
import urllib.request

from pynode.src import communicate

_WEBSITE = "https://alexsocha.github.io/offline_downloads"

is_updating = False

def check_update():
    try:
        update_file = open(os.path.join(os.path.dirname(__file__), "../autoupdate.txt"))
        do_update = True if update_file.readlines()[0].strip().lower() == "true" else False
        update_file.close()
        if not do_update: return

        version_file = open(os.path.join(os.path.dirname(__file__), "version.txt"))
        cur_version = version_file.readlines()[0].strip()
        version_file.close()
        if cur_version != "latest":
            version_number = int(cur_version)
            latest_version = int(urllib.request.urlopen(_WEBSITE + "/latest_version.txt").read())
            if latest_version > version_number and communicate.is_running:
                global is_updating
                is_updating = True
                print("Updating PyNode to version " + str(latest_version) + ". Please do not exit the program...")

                zip_local = os.path.join(os.path.dirname(__file__), "../src_temp.zip")
                folder_local = os.path.join(os.path.dirname(__file__), "../src_temp")
                if os.path.exists(zip_local): os.remove(zip_local)
                if os.path.exists(folder_local): shutil.rmtree(folder_local)

                urllib.request.urlretrieve(_WEBSITE + "/latest_src.zip", zip_local)
                zip_ref = zipfile.ZipFile(zip_local, 'r')
                zip_ref.extractall(folder_local)
                zip_ref.close()
                os.remove(zip_local)
                print("PyNode successfully updated to version " + str(latest_version) + ". Restart the program to finish updating.")
    except: pass
