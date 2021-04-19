#!/usr/bin/python3
"""This fabric file compress the directory to be sent"""

from fabric.api import env, local, run, put
from datetime import datetime
import os

env.hosts = ['35.196.27.222', '184.73.135.160']
env.user = 'ubuntu'


def do_pack():
    """Sets the folder structure up and compresses directory"""

    check = local('mkdir -p versions')
    if (check.failed):
        return None
    now = datetime.now()
    file_name = "versions/web_static_" + \
                "{}{:02d}{:02d}{:02d}{:02d}{:02d}".format(now.year,
                                                          now.month,
                                                          now.day,
                                                          now.hour,
                                                          now.minute,
                                                          now.second) + \
                ".tgz"
    check = local('tar -zcvf {} ./web_static'.format(file_name))
    size_of = os.stat(file_name)
    if (check.failed):
        return None
    else:
        print("web_static packed: {} -> ".format(file_name) +
              "{}Bytes".format(size_of.st_size))
    return("versions/{}".format(file_name))


def do_deploy(archive_path):
    """Upload a compressed file and unpacks it in the servers"""
    try:
        check = put(archive_path, '/tmp/')
        if check.failed:
            return False
    except ValueError:
        return False

    # Get The destination path (filename without extension)
    destination_path = "/data/web_static/releases/" + \
                       "{}".format(archive_path.split('.')[0].split('/')[1])

    # Create the folder
    check = run('mkdir -p {}'.format(destination_path))
    if check.failed:
        return False

    # Unpack the .tgz tho desired path
    check = run('tar -xzf /tmp/{} -C '.format(archive_path.split('/')[1]) +
                '{}'.format('{}'.format(destination_path)))
    if check.failed:
        return False

    # Move the unpacked files
    check = run('mv {}/web_static/* '.format(destination_path) +
                '{}/'.format(destination_path))
    if check.failed:
        return False

    check = run('rm {}/* 2>/dev/null'.format(destination_path)
    if check.failed:
        return False

    # remove the empty folder
    check = run('rm -rf {}/web_static'.format(destination_path))
    if check.failed:
        return False

    # Delete the compressed original file
    check = run('rm -f /tmp/{}'.format(archive_path))
    if check.failed:
        return False

    # Remove the previous symlink
    check = run('rm -rf /data/web_static/current')
    if check.failed:
        return False

    # Creates a symlink between unpacked files in served location
    check = run('ln -s {} /data/web_static/current'.format(destination_path))
    if check.failed:
        return False

    return True


def deploy():
    """This function do a whole deploy"""

    main_path = do_pack()
    if main_path is None:
        return False
    result = do_deploy(main_path)

    return result
