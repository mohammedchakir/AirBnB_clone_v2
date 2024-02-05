#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents
of the web_static folder
"""
from fabric.api import *
from datetime import datetime
import os


def do_pack():
    local('sudo mkdir -p versions')

    t = datetime. now()
    t_str = t.strftime('%Y%m%d%H%M%S')

    local(f'sudo tar -cvzf versions/web_static_{t_str}.tgz web_static')

    f_path = f"versions/web_static_{t_str}.tgz"
    f_size = os. path.getsize(f_path)

    print(f"web_static packed: {f_path} -> {f_size}Bytes")

    return f_path
