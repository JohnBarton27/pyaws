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


def getresourceid(instance):
    """Gets the resource ID of the RDS instance"""
    return instance["DbiResourceId"]


def getdbname(instance):
    """Gets the Database Name of the RDS instance"""
    if "DBName" in instance:
        return instance["DBName"]
    else:
        return ""


def getdbidentifier(instance):
    """Gets the identifier of the RDS instance"""
    return instance["DBInstanceIdentifier"]


def getdballocatedsize(instance):
    """Gets the allocated size of the RDS isntance"""
    return str(instance["AllocatedStorage"]) + " GiB"


def getdbengine(instance):
    """Gets the engine of the RDS instance"""
    return instance["Engine"]


def getdbstatus(instance):
    """Gets the status of the RDS instance"""
    return instance["DBInstanceStatus"]


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
