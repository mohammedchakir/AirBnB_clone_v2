#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to local directory
"""

from fabric.api import local, env
import os
from datetime import datetime
import logging

env.hosts = ['localhost']

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def do_pack():
    """Archives the static files."""
    if not os.path.isdir("versions"):
        os.mkdir("versions")

    cur_time = datetime.now()
    output = os.path.join("versions", "web_static_{}{}{}{}{}{}.tgz".format(
        cur_time.year,
        cur_time.month,
        cur_time.day,
        cur_time.hour,
        cur_time.minute,
        cur_time.second
    ))

    try:
        logger.info("Packing web_static to %s", output)
        local("tar -cvzf {} web_static my_index.html".format(output))
        archive_size = os.stat(output).st_size
        logger.info("web_static packed: %s -> %s Bytes", output, archive_size)
    except Exception as e:
        logger.error("Failed to pack web_static: %s", e)
        output = None

    return output


def do_deploy(archive_path):
    """Deploys the static files to the local directory.
    Args:
        archive_path (str): The path to the archived static files.
    """
    if not os.path.exists(archive_path):
        logger.error("Archive not found at %s", archive_path)
        return False

    try:
        local("mkdir -p /data/web_static/releases/")
        local("tar -xzf {} -C /data/web_static/releases/".format(archive_path))
        file_name = os.path.basename(archive_path)
        folder_name = file_name.replace(".tgz", "")
        run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(folder_name, folder_name))
        local("rm -rf /data/web_static/releases/{}/web_static".format(folder_name))
        local("rm -rf /data/web_static/current")
        local("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(folder_name))
        logger.info('New version is now LIVE!')
        return True
    except Exception as e:
        logger.error("Deployment failed: %s", e)
        return False


def deploy():
    """Archives and deploys the static files to the local directory."""
    archive_path = do_pack()
    if archive_path:
        return do_deploy(archive_path)
    else:
        return False


if __name__ == "__main__":
    deploy()
