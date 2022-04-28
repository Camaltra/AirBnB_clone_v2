#!/usr/bin/python3

"""
Create an .tgz archive with all the statoc content of
my AirBnB static clone
"""

from fabric.api import local
import time


def do_pack():
    """
    Enpack all the static content of AirBnB clone
    """
    date = time.strftime("%Y%m%d%H%M%S")
    try:
        local('mkdir -p versions')
        local(f'tar -czvf versions/web_static_{date}.tgz web_static')
        return f'versions/web_static_{date}.tgz'
    except Exception:
        return None
