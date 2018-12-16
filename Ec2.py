# Module for ec2-related aws functionality
import config
import subprocess
import json


def getinstancejson(name):
    """Given the name of an instance, get its JSON representation"""
    allinstances = getallinstances()

    for instance in allinstances:
        if getinstancename(instance) == name:
            return instance

    raise Exception("Could not find instance with name '" + name + "'!")


def getallinstances():
    """Gets information on all instances"""
    command = config.awsexe + " ec2 describe-instances --profile " + config.profilename
    p = subprocess.Popen(command.split(" "), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = p.communicate()
    jsonout = json.loads(out)

    allreservations = jsonout["Reservations"]
    allinstances = []

    for reservation in allreservations:
        for instance in reservation["Instances"]:
            allinstances.append(instance)

    return allinstances


def getallinstancenames():
    """Gets the names of all ec2 instances"""
    allinstances = getallinstances()

    allinstancenames = []

    for instance in allinstances:
        allinstancenames.append(getinstancename(instance))

    return allinstancenames


def getallinstancestates():
    """Gets the status of all ec2 instances"""
    allinstances = getallinstances()

    allinstancestatuses = {}

    for instance in allinstances:
        name = getinstancename(instance)
        state = getinstancestate(instance)
        allinstancestatuses[name] = state

    return allinstancestatuses


def getinstanceid(instance):
    """Given a JSON instance, get the instance ID"""
    return instance["InstanceId"]


def getinstancename(instance):
    """Given a JSON instance, get the name"""
    tags = instance["Tags"]
    for tag in tags:
        if tag["Key"] == "Name":
            return tag["Value"]


def getinstancestate(instance):
    """Given a JSON instance, get its state"""
    return instance["State"]["Name"]


def getinstancepublicip(instance):
    """Given a JSON instance, get its public IP address"""
    if "PublicIpAddress" in instance:
        return instance["PublicIpAddress"]
    else:
        return ""


def getinstancestatebyname(name):
    """Gets the state of an instance, given its name"""
    allstates = getallinstancestates()
    if name in allstates:
        return allstates[name]
    else:
        return "'" + name + "' is not the name of an EC2 instance you currently have access to!"


def startinstance(instance):
    """Starts an instance, given the JSON of the instance"""
    instanceid = getinstanceid(instance)
    command = config.awsexe + " ec2 start-instances --instance-ids " + instanceid + " --profile " + config.profilename
    p = subprocess.Popen(command.split(" "), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = p.communicate()
    return out


def startinstancebyname(name):
    """Starts an EC2 instance, given its name"""
    instance = getinstancejson(name)
    return startinstance(instance)


def stopinstance(instance):
    """Stops an instance, given the JSON of the instance"""
    instanceid = getinstanceid(instance)
    command = config.awsexe + " ec2 stop-instances --instance-ids " + instanceid + " --profile " + config.profilename
    p = subprocess.Popen(command.split(" "), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = p.communicate()
    return out


def stopinstancebyname(name):
    """Stops an EC2 instance, given its name"""
    instance = getinstancejson(name)
    return stopinstance(instance)


def displaydashboard():
    """Display a dashboard with all EC2 information"""
    allinstances = getallinstances()

    names = []
    states = []
    ipaddresses = []

    # Populate column data
    for instance in allinstances:
        names.append(getinstancename(instance))
        states.append(getinstancestate(instance))
        ipaddresses.append(getinstancepublicip(instance))

    # Name
    namescol = createdashcol("Name", names, leftborder=True)

    # States
    statescol = createdashcol("State", states)

    # IP Addresses
    ipadressescol = createdashcol("IP Address", ipaddresses)

    for x in range(0, len(namescol)):
        print(namescol[x] + statescol[x] + ipadressescol[x])


def createdashcol(title, data, leftborder=False):
    """Create a data for the dashboard"""
    rows = []
    maxdatalen = len(max(data, key=len))

    # Header
    rows.append(pad(title, maxdatalen, leftborder=leftborder))

    # Header line
    rows.append(pad("", maxdatalen, padchar="-", leftborder=leftborder))

    # Data
    for dataval in data:
        rows.append(pad(dataval, maxdatalen, leftborder=leftborder))

    return rows


def pad(content, maxlength, padchar=" ", leftborder=False):
    """Pad a cell for dashboard display"""
    if leftborder:
        data = "|"
    else:
        data = ""
    data += content
    spacesneeded = maxlength - len(content)
    for x in range(0, spacesneeded):
        data += padchar
    return data + "|"

