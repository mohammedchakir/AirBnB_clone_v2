#!/usr/bin/env python3
"""
Fabric script that generates a .tgz archive from the contents
of the web_static folder
"""
from fabric.api import local
from datetime import datetime
from time import strftime


def do_pack():
    """
    Creates a .tgz archive from the contents of the web_static folder
    """
    try:
        current_time = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        archive_name = "web_static_{}.tgz".format(current_time)
        local("mkdir -p versions")
        local("tar -cvzf versions/{} web_static".format(archive_name))

        return "versions/{}".format(archive_name)
    except Exception as e:
        return None
