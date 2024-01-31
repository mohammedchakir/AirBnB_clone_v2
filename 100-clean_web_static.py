#!/usr/bin/env python3
"""
Fabric script that deletes out-of-date archives
"""

from fabric.api import env, run, local
from datetime import datetime

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'
env.key_filename = ['my_ssh_private_key']


def do_clean(number=0):
    """
    Deletes out-of-date archives
    """
    try:
        number = int(number)
        if number < 0:
            return

        # Get the list of archives sorted by modification time
        archives = local("ls -1tr versions", capture=True).split("\n")

        # Keep only the most recent 'number' archives
        archives_to_keep = archives[-number:]

        # Delete unnecessary archives in the versions folder
        for archive in archives:
            if archive not in archives_to_keep:
                local("rm -f versions/{}".format(archive))

        # Delete unnecessary archives in the /data/web_static/releases folder on both servers
        releases = run("ls -1tr /data/web_static/releases").split("\n")
        releases_to_keep = releases[-number:]

        for release in releases:
            if release not in releases_to_keep:
                run("rm -rf /data/web_static/releases/{}".format(release))

        print("Cleaned up old archives.")
    except Exception as e:
        pass


if __name__ == "__main__":
    do_clean()
