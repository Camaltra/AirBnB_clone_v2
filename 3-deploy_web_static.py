#!/usr/bin/python3

"""
Deploy all static hbnb into our 2 web servers.
"""

from fabric.api import put, run, env, local
from os.path import exists
import time

env.hosts = ['34.148.245.248', '34.138.44.159']


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


def do_deploy(archive_path):
    """
    Deplay all the static files in the nginx servers
    args:
        archive_path (str): String to the path of the archive
    """
    if exists(archive_path) is False:
        return False
    try:
        fileAndExent = archive_path.split('/')[-1]
        nameFile = fileAndExent.split('.')[0]
        path = '/data/web_static/releases'
        print(nameFile)

        put(archive_path, f'/tmp/{fileAndExent}')
        run(f'rm -rf {path}/{nameFile}')
        run(f'mkdir -p {path}/{nameFile}')
        run(f'tar -xzf /tmp/{fileAndExent} -C {path}/{nameFile}/')
        run(f'mv {path}/{nameFile}/web_static/* {path}/{nameFile}')
        run(f'rm /tmp/{fileAndExent}')
        run('rm /data/web_static/current')
        run(f'ln -sf {path}/{nameFile} /data/web_static/current')

    except Exception:
        return False


def deploy():
    """
    Deploy all the web static
    Using do_pack to enpackage all the html and css static
    Using do_deploy to send and deploy file on the web site
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
