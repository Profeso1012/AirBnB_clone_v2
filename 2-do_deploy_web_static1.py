#!/usr/bin/python3
import os.path
from fabric.api import env, put, run

# Replace with the IP addresses of your web servers
env.hosts = ['100.25.165.20', '52.91.133.191']

def do_deploy(archive_path):
  """
  Distributes an archive to web servers.

  Args:
      archive_path (str): The path to the archive file for deployment.

  Returns:
      bool: True if deployment is successful, False otherwise.
  """

  if not os.path.isfile(archive_path):
    return False

  try:
    # Extract filename and remove extension
    filename = archive_path.split("/")[-1]
    no_ext = filename.split(".")[0]

    # Upload archive to /tmp/ directory
    put(archive_path, "/tmp/{}".format(filename))

    # Create release directory
    run("mkdir -p /data/web_static/releases/{}".format(no_ext))

    # Uncompress archive to release directory
    run("tar -xzf /tmp/{} -C /data/web_static/releases/{}".format(filename, no_ext))

    # Delete archive from server
    run("rm /tmp/{}".format(filename))

    # Move content to root of release directory (if needed)
    # This step might be necessary depending on your archive structure
    # run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(no_ext, no_ext))

    # Delete the empty web_static directory within the release directory (if needed)
    # run("rm -rf /data/web_static/releases/{}/web_static".format(no_ext))

    # Delete existing symbolic link
    run("rm -rf /data/web_static/current")

    # Create new symbolic link to the new release
    run("ln -s /data/web_static/releases/{} /data/web_static/current".format(no_ext))

    return True
  except Exception as e:
    print("An error occurred during deployment: {}".format(e))
    return False
