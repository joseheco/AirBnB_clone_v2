#!/usr/bin/python3
# Write a Fabric script (based on the file 1-pack_web_static.py)
# that distributes an archive to your web server
from datetime import datetime
from fabric.api import local, put, env, run
import os
env.hosts = ['34.138.9.75', '54.86.211.56']
env.user = "ubuntu"


def do_deploy(archive_path):
    if os.path.isfile(archive_path) is False:
        return False
    try:
        put(archive_path, "/tmp/")
        arch_filename_tgz = archive_path.split('/')[1]
        arch_filename_no_tgz = arch_filename_tgz.split('.')[0]
        target_path = "/data/web_static/releases/{}/".format(
            arch_filename_no_tgz)
        run("sudo mkdir -p {}".format(target_path))
        run("sudo tar -xzf /tmp/{} -C {}"
            .format(arch_filename_tgz, target_path))
        run("sudo rm /tmp/{}".format(arch_filename_tgz))
        run("sudo mv {}web_static/* {}".format(target_path, target_path))
        run("sudo rm -rf {}web_static".format(target_path))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(target_path))
        return True
    except:
        return False
