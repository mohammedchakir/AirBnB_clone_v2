#!/usr/bin/env python3
"""
Fabric script that distributes an archive to your web servers
"""

from fabric.api import env, put, run
from os.path import exists

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'
env.key_filename = ['my_ssh_private_key']


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory on the web server
        put(archive_path, "/tmp/")

        # Extract the archive to /data/web_static/releases/
        archive_filename = archive_path.split("/")[-1]
        release_path = "/data/web_static/releases/" + archive_filename.split(".")[0]
        run("mkdir -p {}".format(release_path))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, release_path))

        # Move contents out of web_static/ directory
        run("mv {}/web_static/* {}".format(release_path, release_path))

        # Remove the now empty web_static/ directory
        run("rm -rf {}/web_static".format(release_path))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(archive_filename))

        # Delete the existing symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link pointing to the new version
        run("ln -s {} /data/web_static/current".format(release_path))

        print("New version deployed!")
        return True

    except Exception as e:
        return False
