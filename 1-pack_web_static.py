#!/usr/bin/env python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static folder
"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Creates a .tgz archive from the contents of the web_static folder
    """
    try:
        # Create the 'versions' folder if it doesn't exist
        local("mkdir -p versions")

        # Generate the file name with the current date and time
        current_time = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        archive_name = "web_static_{}.tgz".format(current_time)

        # Compress the web_static folder into a .tgz file
        local("tar -cvzf versions/{} web_static".format(archive_name))

        return "versions/{}".format(archive_name)
    except Exception as e:
        return None
