#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives
"""
from fabric.api import *
import os.path

env.hosts = ['18.233.62.225', '52.91.116.153']


def do_clean(number=0):
    """Delete out-of-date the archives.

    Args:
    number (int): Number of archives to keep.

    If number is 0 or 1, keeps only most recent archive. If
    number is 2, keeps most and second recent archives
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
