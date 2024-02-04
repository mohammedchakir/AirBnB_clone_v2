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
<<<<<<< HEAD
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
=======
        """Deploy web files to server
        """
        try:
                if not (path.exists(archive_path)):
                        return False

                # upload archive
                put(archive_path, '/tmp/')

                # create target dir
                timestamp = archive_path[-18:-4]
                run('sudo mkdir -p /data/web_static/\
releases/web_static_{}/'.format(timestamp))

                # uncompress archive and delete .tgz
                run('sudo tar -xzf /tmp/web_static_{}.tgz -C \
/data/web_static/releases/web_static_{}/'
                    .format(timestamp, timestamp))

                # remove archive
                run('sudo rm /tmp/web_static_{}.tgz'.format(timestamp))

                # move contents into host web_static
                run('sudo mv /data/web_static/releases/web_static_{}/web_static/* \
/data/web_static/releases/web_static_{}/'.format(timestamp, timestamp))

                # remove extraneous web_static dir
                run('sudo rm -rf /data/web_static/releases/\
web_static_{}/web_static'
                    .format(timestamp))

                # delete pre-existing sym link
                run('sudo rm -rf /data/web_static/current')

                # re-establish symbolic link
                run('sudo ln -s /data/web_static/releases/\
web_static_{}/ /data/web_static/current'.format(timestamp))
        except:
                return False

        # return True on success
>>>>>>> cf190dc211eae8eaec8caba6b276072a05eb4bad
        return True
