#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers
"""
import re
import os.path
from fabric.api import *
from datetime import datetime
import sys


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    target = local("mkdir -p ./versions")
    name = str(datetime.now()).replace(" ", '')
    opt = re.sub(r'[^\w\s]', '', name)
    tar = local('tar -cvzf versions/web_static_{}.tgz web_static'.format(opt))
    if os.path.exists("./versions/web_static_{}.tgz".format(opt)):
        return os.path.normpath("./versions/web_static_{}.tgz".format(opt))
    else:
        return None


def do_deploy(archive_path):
    """Distributes an archive to both of webservers 01 & 02.

    Args:
        archive_path (str): Path of archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error appears - False.
        Otherwise - True.
    """
    if os.path.exists(archive_path) is False:
        return False
    try:
        arc = archive_path.split("/")
        base = arc[1].strip('.tgz')
        put(archive_path, '/tmp/')
        sudo('mkdir -p /data/web_static/releases/{}'.format(base))
        main = "/data/web_static/releases/{}".format(base)
        sudo('tar -xzf /tmp/{} -C {}/'.format(arc[1], main))
        sudo('rm /tmp/{}'.format(arc[1]))
        sudo('mv {}/web_static/* {}/'.format(main, main))
        sudo('rm -rf /data/web_static/current')
        sudo('ln -s {}/ "/data/web_static/current"'.format(main))
        return True
    except:
        return False


def deploy():
    """Create and distribute an archive to a web server."""
    path = do_pack()
    if path is None:
        return False
    result = do_deploy(path)
    return result


def do_clean(number=0):
    """
    Deletes out-of-date archives
    """
    try:
        number = int(number)
        if number < 2:
            number = 1
        else:
            number -= 1
        local("cd versions && ls -t | tail -n +{} | xargs -I {{}} rm -- {{}}".format(number + 1))
        run("cd /data/web_static/releases && ls -t | tail -n +{} | xargs -I {{}} sudo rm -rf -- {{}}".format(number + 1))
    except ValueError:
        pass


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: {} <SSH_key_path> <username> <number>".format(sys.argv[0]))
        sys.exit(1)

    env.user = sys.argv[2]
    env.key_filename = sys.argv[1]

    if len(sys.argv) == 4:
        do_clean(sys.argv[3])
