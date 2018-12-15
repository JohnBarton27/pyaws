# Module for ec2-related aws functionality
import config
import subprocess
import json
import Utils


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


def getallinstancestatuses():
    """Gets the status of all ec2 instances"""
    allinstances = getallinstances()

    allinstancestatuses = {}

    for instance in allinstances:
        name = getinstancename(instance)
        state = getinstancestate(instance)
        allinstancestatuses[name] = state

    return allinstancestatuses


def getinstancename(instance):
    """Given a JSON instance, get the name"""
    tags = instance["Tags"]
    for tag in tags:
        if tag["Key"] == "Name":
            return tag["Value"]


def getinstancestate(instance):
    """Given a JSON instance, get its state"""
    return instance["State"]["Name"]


def getinstancestatusbyname(name):
    """Gets the state of an instance, given its name"""
    allstatuses = getallinstancestatuses()
    if name in allstatuses:
        return allstatuses[name]
    else:
        return "'" + name + "' is not the name of an EC2 instance you currently have access to!"
