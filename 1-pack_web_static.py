#!/usr/bin/python3
"""Fabric script that generates a .tgz"""
import fabric
from fabric.api import local
from datetime import datetime


def do_pack():
    """ Prototype: def do_pack():"""
    try:
        now = datetime.now()
        NameArchive = "web_static" + now.strftime("%Y%m%d%H%M%S")+".tgz"
        PathArchive = "versions/" + NameArchive
        local("sudo mkdir -p versions")
        local("tar -czvf" + PathArchive + " web_static")
        return PathArchive
    except Exception:
        return None
