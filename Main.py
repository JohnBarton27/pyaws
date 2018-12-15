# Main file in pyaws

import config
import Configure


def startmenu():
    print("Checking 'config' file based on your config.py...")
    Configure.createconfigfile(config.defaultregion)

    print("Checking 'credentials' file based on your config.py...")
    Configure.createcredentialsfile(config.accesskey, config.secretkey)

    command = "aws configure --profile " + config.profilename


if __name__ == '__main__':
    startmenu()
