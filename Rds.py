# Module for RDS-related aws functionality
import config
import subprocess
import json


def getallrdsinstances():
    """Get all RDS Instances"""
    command = config.awsexe + " rds describe-db-instances --profile " + config.profilename
    p = subprocess.Popen(command.split(" "), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = p.communicate()
    jsonout = json.loads(out)

    jsoninstances = jsonout["DBInstances"]

    return jsoninstances


def getjson(instance):
    if type(instance) in [dict]:
        return instance

    allinstances = getallrdsinstances()

    for allinstance in allinstances:
        if getresourceid(allinstance) == instance:
            return allinstance

        if getdbidentifier(allinstance) == instance:
            return allinstance

        if getdbname(allinstance) == instance:
            return allinstance

    raise Exception("Cannot find instance '" + instance + "'!")


def getresourceid(instance):
    """Gets the resource ID of the RDS instance"""
    instance = getjson(instance)
    return instance["DbiResourceId"]


def getdbname(instance):
    """Gets the Database Name of the RDS instance"""
    instance = getjson(instance)
    if "DBName" in instance:
        return instance["DBName"]
    else:
        return ""


def getdbidentifier(instance):
    """Gets the identifier of the RDS instance"""
    instance = getjson(instance)
    return instance["DBInstanceIdentifier"]


def getdballocatedsize(instance):
    """Gets the allocated size of the RDS isntance"""
    instance = getjson(instance)
    return str(instance["AllocatedStorage"]) + " GiB"


def getdbengine(instance):
    """Gets the engine of the RDS instance"""
    instance = getjson(instance)
    return instance["Engine"]


def getdbstatus(instance):
    """Gets the status of the RDS instance"""
    instance = getjson(instance)
    return instance["DBInstanceStatus"]


def startdb(instance):
    """Starts an RDS database instance"""
    instance = getjson(instance)
    identifier = getdbidentifier(instance)
    command = config.awsexe + " rds start-db-instance --db-instance-identifier " + identifier + " --profile " + config.profilename
    p = subprocess.Popen(command.split(" "), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = p.communicate()
    return out


def stopdb(instance):
    """Stops an RDS database instance"""
    instance = getjson(instance)
    identifier = getdbidentifier(instance)
    command = config.awsexe + " rds stop-db-instance --db-instance-identifier " + identifier + " --profile " + config.profilename
    p = subprocess.Popen(command.split(" "), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = p.communicate()
    return out


def displaydashboard():
    """Display a dashboard with all RDS information"""
    import Utils
    allinstances = getallrdsinstances()

    identifiers = []
    names = []
    statuses = []
    allocatedsizes = []
    engines = []

    # Populate column data
    for instance in allinstances:
        identifiers.append(getdbidentifier(instance))
        names.append(getdbname(instance))
        statuses.append(getdbstatus(instance))
        allocatedsizes.append(getdballocatedsize(instance))
        engines.append(getdbengine(instance))

    # Identifiers
    identifierscol = Utils.createdashcol("Identifier", identifiers, leftborder=True)

    # Name
    namescol = Utils.createdashcol("Name", names)

    # Statuses
    statuscol = Utils.createdashcol("Status", statuses)

    # Allocated Sizes
    allocatedsizescol = Utils.createdashcol("Allocated Size", allocatedsizes)

    # Engines
    enginescol = Utils.createdashcol("Engine", engines)

    for x in range(0, len(namescol)):
        print(identifierscol[x] + namescol[x] + statuscol[x] + allocatedsizescol[x] + enginescol[x])
