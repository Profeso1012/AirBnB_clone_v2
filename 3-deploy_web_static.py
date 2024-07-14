#!/usr/bin/python3
# Fabfile to create and distribute an archive to web servers.
from fabric.api import env, local, put, run
from datetime import datetime
import os.path

env.hosts = ["100.25.165.20", "52.91.133.191"]  # Replace with your actual IPs
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'  # Replace with your actual key path


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""
    local("mkdir -p versions")
    dt = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(dt)
    result = local("tar -cvzf {} web_static".format(archive_path),
                   capture=True)
    if result.succeeded:
        archive_size = local("du -b {} | cut -f1".format(archive_path),
                             capture=True).stdout.strip()
        print("web_static packed: {} -> {}Bytes".format(archive_path,
                                                        archive_size))
        return archive_path
    else:
        return None


def do_deploy(archive_path):
    """Distributes an archive to a web server."""
    if not os.path.isfile(archive_path):
        return False
    try:
        file_name = archive_path.split("/")[-1]
        no_ext = file_name.split(".")[0]
        release_dir = "/data/web_static/releases/{}".format(no_ext)
        put(archive_path, "/tmp/{}".format(file_name))
        run("mkdir -p {}".format(release_dir))
        run("tar -xzf /tmp/{} -C {}".format(file_name, release_dir))
        run("rm /tmp/{}".format(file_name))
        run("mv {0}/web_static/* {0}/".format(release_dir))
        run("rm -rf {}/web_static".format(release_dir))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_dir))
        print("Deployment successful.")
        return True
    except Exception as e:
        print("Deployment failed:", e)
        return False


def deploy():
    """Creates and distributes an archive to web servers."""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
