#!/usr/bin/env python3
"""
Fabric script that generates a .tgz archive from the contents
of the web_static folder
"""
from fabric.api import local
from datetime import date
from time import strftime


def do_pack():
    """
    Creates a .tgz archive from the contents of the web_static folder
    """
        current_time = strftime("%Y%m%d%H%M%S")
    try: 
        local("mkdir -p versions")
        local("tar -czvf versions/web_static_{}.tgz web_static/"
              .format(current_time))

        return "versions/web_static_{}.tgz".format(current_time)
    except Exception as e:
        return None
