#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
import os.path
from fabric.api import env, put, run

env.hosts = ["100.25.165.20", "52.91.133.191"]  # Replace with your actual IPs
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'  # Replace with your actual key path


def do_deploy(archive_path):
    """Distributes an archive to a web server.
    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if not os.path.isfile(archive_path):
        return False
    try:
        file_name = archive_path.split("/")[-1]
        no_ext = file_name.split(".")[0]
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/{}".format(file_name))
        # Create the release directory
        run("mkdir -p /data/web_static/releases/{}".format(no_ext))
        # Uncompress the archive to the folder
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}".format(
            file_name, no_ext))
        # Delete the archive from the web server
        run("rm /tmp/{}".format(file_name))
        # Move the contents to the correct folder
        run("mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/".format(no_ext, no_ext))
        run("rm -rf /data/web_static/releases/{}/web_static".format(no_ext))
        # Delete the current symbolic link
        run("rm -rf /data/web_static/current")
        # Create a new symbolic link
        run("ln -s /data/web_static/releases/{} /data/web_static/current".
            format(no_ext))
        return True
    except Exception:
        return False
