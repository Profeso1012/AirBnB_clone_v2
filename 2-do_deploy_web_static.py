#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
import os.path
from fabric.api import env, put, run, sudo, local

env.hosts = ["100.25.165.20", "52.91.133.191"]
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """Distributes an archive to a web server.
    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if not os.path.isfile(archive_path):
        print("Archive path does not exist.")
        return False

    try:
        file_name = archive_path.split("/")[-1]
        no_ext = file_name.split(".")[0]
        release_dir = "/data/web_static/releases/{}".format(no_ext)
        print("Uploading archive to /tmp/...")
        put(archive_path, "/tmp/{}".format(file_name))

        print("Creating release directory: {}".format(release_dir))
        run("mkdir -p {}".format(release_dir))

        print("Uncompressing archive to release directory...")
        run("tar -xzf /tmp/{} -C {}".format(file_name, release_dir))

        print("Removing archive from /tmp/...")
        run("rm /tmp/{}".format(file_name))

        print("Moving contents to correct folder...")
        run("mv {0}/web_static/* {0}/".format(release_dir))
        run("rm -rf {}/web_static".format(release_dir))

        print("Removing current symbolic link...")
        run("rm -rf /data/web_static/current")

        print("Creating new symbolic link...")
        run("ln -s {} /data/web_static/current".format(release_dir))

        print("Deployment successful.")
        return True
    except Exception as e:
        print("Deployment failed:", e)
        return False
