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


def do_local_pack():
    """Archives the static files locally."""
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


def do_local_deploy(archive_path):
    """Deploys the static files locally."""
    if not os.path.exists(archive_path):
        logger.error("Archive not found at %s", archive_path)
        return False

    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = os.path.join(
        os.getcwd(), "data", "web_static", "releases", folder_name)

    try:
        local("mkdir -p {}".format(folder_path))
        local("tar -xzf {} -C {}".format(archive_path, folder_path))
        local("mv {}/web_static/* {}".format(folder_path, folder_path))
        local("rm -rf {}/web_static".format(folder_path))
        local("rm -rf data/web_static/current")
        local("ln -s {} data/web_static/current".format(folder_path))
        logger.info('Local deployment completed successfully!')
        return True
    except Exception as e:
        logger.error("Local deployment failed: %s", e)
        return False


def deploy_local():
    """Archives and deploys the static files locally."""
    archive_path = do_local_pack()
    if archive_path:
        return do_local_deploy(archive_path)
    else:
        return False


if __name__ == "__main__":
    deploy_local()
