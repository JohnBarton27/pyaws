# Main file in pyaws

import config
import Configure
import MenuTemplates


def startmenu():
    print("Checking 'config' file based on your config.py...")
    Configure.createconfigfile(config.defaultregion)

    print("Checking 'credentials' file based on your config.py...")
    Configure.createcredentialsfile(config.accesskey, config.secretkey)

    MenuTemplates.startmenu(MenuTemplates.mainmenu)


if __name__ == '__main__':
    startmenu()
