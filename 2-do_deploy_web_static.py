#!/usr/bin/python3
"""Fabric script (based on the file 1-pack_web_static.py) that distributes an
archive to your web servers"""
import fabric
from fabric.api import local, env, put, run
from datetime import datetime
from os import path

env.hosts = ['35.237.172.160', '35.237.222.103']


def do_deploy(archive_path):
    """ * Prototype: def do_deploy(archive_path):
    * Returns False if the file at the path archive_path doesn’t exist
    * The script should take the following steps:
    ** Upload the archive to the /tmp/ directory of the web server
    ** Uncompress the archive to the folder
    /data/web_static/releases/<archive filename without extension> on the web
    server
    ** Delete the archive from the web server
    ** Delete the symbolic link /data/web_static/current from the web server
    ** Create a new the symbolic link /data/web_static/current on the web
    server, linked to the new version of your code
    (/data/web_static/releases/<archive filename without extension>)
    * All remote commands must be executed on your both web servers
    (using env.hosts = ['<IP web-01>', 'IP web-02'] variable in your script)
    * Returns True if all operations have been done correctly,
    otherwise returns False
    * You must use this script to deploy it on your
    servers: xx-web-01 and xx-web-02
    In the following example, the SSH key and the username used for accessing
    to the server are passed in the command line. Of course, you could define
    them as Fabric environment variables (ex: env.user =...)

    Disclaimer: commands execute by Fabric displayed below are linked to the
    way we implemented the archive
    function do_pack
    - like the mv command
    - depending of your implementation of it, you may don’t need it """

    if not path.exists(archive_path):
        return False
    try:
        NameArchive = archive_path[9:]
        NameArchiveWitoutExtension = NameArchive[:-4]
        put(archive_path, "/temp/" + NameArchive)
        run("mkdir -p /data/web_static/releases/" + NameArchiveWitoutExtension)
        run("tar -xzvf /tmp/" + NameArchive + " -C /data/web_static/releases/"
            + NameArchiveWitoutExtension + " --strip-components=1")
        run("rm -rf /tmp/" + NameArchive)
        run("rm -rf /data/web_static/current")
        run("sudo ln -sf /data/web_static/releases/"
            + NameArchiveWitoutExtension + "/data/web_static/current")

        return True
    except Exception:
        return False


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
