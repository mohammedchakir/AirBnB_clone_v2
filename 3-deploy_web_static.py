#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers
"""

from fabric.api import local, run, put, env
import os
from datetime import datetime
import logging

env.hosts = ['18.233.62.225', '52.91.116.153']

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
        local("tar -cvzf {} web_static".format(output))
        archive_size = os.stat(output).st_size
        logger.info("web_static packed: %s -> %s Bytes", output, archive_size)
    except Exception as e:
        logger.error("Failed to pack web_static: %s", e)
        output = None

    return output


def do_deploy(archive_path):
    """Deploys the static files to the host servers.
    Args:
        archive_path (str): The path to the archived static files.
    """
    if not os.path.exists(archive_path):
        logger.error("Archive not found at %s", archive_path)
        return False

    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = "/data/web_static/releases/{}/".format(folder_name)

    try:
        put(archive_path, "/tmp/{}".format(file_name))
        run("mkdir -p {}".format(folder_path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder_path))
        run("rm -rf /tmp/{}".format(file_name))
        run("mv {}web_static/* {}".format(folder_path, folder_path))
        run("rm -rf {}web_static".format(folder_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_path))
        logger.info('New version is now LIVE!')
        return True
    except Exception as e:
        logger.error("Deployment failed: %s", e)
        return False


def deploy():
    """Archives and deploys the static files to the host servers."""
    archive_path = do_pack()
    if archive_path:
        return do_deploy(archive_path)
    else:
        return False
