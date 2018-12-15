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
        tags = instance["Tags"]
        for tag in tags:
            if tag["Key"] == "Name":
                allinstancenames.append(tag["Value"])

    return allinstancenames
