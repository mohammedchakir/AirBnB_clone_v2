#!/usr/bin/python3
"""
Fabric script (based on the file 2-do_deploy_web_static.py) 
"""
do_pack = __import__('1-pack_web_static')
do_deploy = __import__('2-do_deploy_web_static')


def deploy():
    """
    rchives and deploys the static files to the host servers.
    """
    filepath = do_pack.do_pack()
    if not filepath:
        return False
    return do_deploy.do_deploy(filepath)
