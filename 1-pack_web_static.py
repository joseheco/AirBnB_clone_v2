#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents of the
web_static"""
import fabric
from fabric.api import local
from datetime import datetime


def do_pack():
    """ Prototype: def do_pack():
    * All files in the folder web_static must be added to the final archive
    * All archives must be stored in the folder versions (your function should
    create this folder if it doesn’t exist)
    * The name of the archive created must be
    web_static_<year><month><day><hour><minute><second>.tgz
    * The function do_pack must return the archive path if the archive has
    been correctly generated. Otherwise, it should return None """
    try:
        now = datetime.now()
        NameArchive = "web_static" + now.strftime("%Y%m%d%H%M%S")+".tgz"

        PathArchive = "versions/" + NameArchive

        local("sudo mkdir -p versions")
        local("tar -czvf" + PathArchive + " web_static")
        return PathArchive
    except Exception:
        return None
