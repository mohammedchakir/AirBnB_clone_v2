#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""
from fabric.api import env, run, put
import os

env.hosts = ['18.233.62.225', '52.91.116.153']
env.user = 'ubuntu'
env.key_filename = ['~/.ssh/school']


def do_deploy(archive_path):
    """
    Distributes an archive to web servers.

    :param archive_path: Path to the archive to be deployed.
    :return: True if successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        print(f"Error: Archive not found at {archive_path}")
        return False

    try:
        archive_filename = os.path.basename(archive_path)
        archive_no_ext = os.path.splitext(archive_filename)[0]
        remote_tmp_path = '/tmp/'
        remote_release_path = '/data/web_static/releases/'
        remote_current_path = '/data/web_static/current'

        # Upload archive to /tmp/ directory of the web server
        put(archive_path, remote_tmp_path)

        # Uncompress the archive to /data/web_static/releases/
        run(f"mkdir -p {remote_release_path}{archive_no_ext}")
        run(f"tar -xzf {remote_tmp_path}{archive_filename} -C \
                {remote_release_path}{archive_no_ext}")

        # Delete the archive from the web server
        run(f"rm {remote_tmp_path}{archive_filename}")

        # Delete the symbolic link /data/web_static/current from the web server
        run(f"rm -f {remote_current_path}")

        # Create a new symbolic link /data/web_static/current linked to version
        run(f"ln -s {remote_release_path}{archive_no_ext} \
                {remote_current_path}")

        print("Deployment successful.")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False
