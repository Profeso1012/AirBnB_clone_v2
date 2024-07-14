#!/usr/bin/python3
# Fabric script that generates a .tgz archive
from fabric.api import local
from datetime import datetime


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""
    # Create the versions directory if it does not exist
    local("mkdir -p versions")
    # Generate the archive name using the current date and time
    dt = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(dt)
    # Create the archive using the tar command and capture the output
    print("Packing web_static to {}".format(archive_path))
    result = local("tar -cvzf {} web_static".format(archive_path),
                   capture=True)
    # Print the output of the tar command
    print(result)
    # Check if the tar command was successful
    if result.succeeded:
        archive_size = local("du -b {} | cut -f1".format(archive_path),
                             capture=True).stdout.strip()
        print("web_static packed: {} -> {}Bytes".format(archive_path,
                                                        archive_size))
        return archive_path
    else:
        return None
