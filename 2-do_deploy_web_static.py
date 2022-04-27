#!/usr/bin/python3

"""
Create an .tgz archive with all the statoc content of
my AirBnB static clone
"""

from fabric.api import put, run, env
from os.path import exists

env.hosts = ['34.148.245.248', '34.138.44.159']


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
