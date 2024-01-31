#!/usr/bin/env python3
"""
Fabric script that creates and distributes an archive to your web servers
"""

from fabric.api import local, run, put, env
from os.path import exists
from datetime import datetime

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'
env.key_filename = ['my_ssh_private_key']


def do_pack():
    """
    Creates a .tgz archive from the contents of the web_static folder
    """
    try:
        # Create the 'versions' folder if it doesn't exist
        local("mkdir -p versions")

        # Generate the file name with the current date and time
        current_time = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        archive_name = "web_static_{}.tgz".format(current_time)

        # Compress the web_static folder into a .tgz file
        local("tar -cvzf versions/{} web_static".format(archive_name))

        return "versions/{}".format(archive_name)
    except Exception as e:
        return None


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


def deploy():
    """
    Deploys a new version on the web servers
    """
    archive_path = do_pack()
    if archive_path is None:
        return False

    return do_deploy(archive_path)
