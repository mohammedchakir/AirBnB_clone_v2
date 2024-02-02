#!/usr/bin/env python3
"""
Fabric script that deletes out-of-date archives
"""
from fabric.api import env, run, local
import os

env.hosts = ['34.207.57.228', '54.160.106.44']


def do_clean(number=0):
    """Remove outdated archives

    Args:
        number (int): The quantity of archives to retain

    If the number is 0 or 1, only the latest archive is retained.
    For a number of 2, both the most recent and second-most recent
    archives are kept, and so forth
    """
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
