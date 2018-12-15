# Python wrapper for 'aws configure'
from pathlib import Path
import os
import config


def createcredentialsfile(accesskey, secretkey):
    """Creates a credentials file"""
    filename = str(Path.home()) + "/.aws/credentials"

    if os.path.exists(filename):
        f = open(filename, "r")

        # Check to see if config contains pyaws profile
        filedata = f.readlines()

        for line in filedata:
            if config.profilename in line:
                return

    f = open(filename, "a+")

    f.write(config.profilename + "\n")
    f.write("aws_access_key_id = " + accesskey + "\n")
    f.write("aws_secret_access_key = " + secretkey)
    f.close()


def createconfigfile(region):
    """Create a config file"""
    filename = str(Path.home()) + "/.aws/config"

    if os.path.exists(filename):
        f = open(filename, "r")

        # Check to see if config contains pyaws profile
        filedata = f.readlines()

        for line in filedata:
            if config.profilename in line:
                return

    f = open(filename, "a+")

    f.write(config.profilename + "\n")
    f.write("region = " + region)
    f.close()
