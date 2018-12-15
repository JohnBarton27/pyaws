# Main file in pyaws

import config
import Configure
import Utils
import Ec2
import MenuTemplates


def startmenu():
    print("Checking 'config' file based on your config.py...")
    Configure.createconfigfile(config.defaultregion)

    print("Checking 'credentials' file based on your config.py...")
    Configure.createcredentialsfile(config.accesskey, config.secretkey)

    selection = input(MenuTemplates.getmenu(MenuTemplates.mainmenu))
    print(selection)

    Utils.printjson(Ec2.getallinstancenames())


if __name__ == '__main__':
    startmenu()
