# Module for ec2-related aws functionality
import config
import subprocess
import json


def getinstancejson(name):
    """Given the name (or ID) of an instance, get its JSON representation"""
    allinstances = getallinstances()

    for instance in allinstances:
        if getinstancename(instance) == name:
            return instance

        if getinstanceid(instance) == name:
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
    if "Tags" in instance:
        tags = instance["Tags"]
        for tag in tags:
            if tag["Key"] == "Name":
                return tag["Value"]
    return ""


def getinstancestate(instance):
    """Given a JSON instance, get its state"""
    instance = getinstancejson(instance)
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


def getallelasticips():
    """Gets all elastic IP addresses associated with your account"""
    command = config.awsexe + " ec2 describe-addresses --profile " + config.profilename
    p = subprocess.Popen(command.split(" "), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = p.communicate()
    addresses = json.loads(out)
    return addresses["Addresses"]


def getipjson(ip):
    if type(ip) is dict:
        return ip
    allips = getallelasticips()

    for allip in allips:
        if ip == getelasticpublicip(allip):
            return allip


def getassociatedinstance(ip):
    """Gets the InstanceId of the Elastic IP Address"""
    if "InstanceId" in ip:
        return getinstancejson(ip["InstanceId"])
    else:
        return ""


def getelasticallocationid(ip):
    """Gets the AllocationId of the given Elastic IP Address"""
    ip = getipjson(ip)
    return ip["AllocationId"]


def getelasticpublicip(ip):
    """Gets the PublicIp address of the Elastic IP Address"""
    return ip["PublicIp"]


def createip():
    """Create a new elastic IP address"""
    command = config.awsexe + " ec2 allocate-address --profile " + config.profilename
    p = subprocess.Popen(command.split(" "), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = p.communicate()

    print(err.decode("utf-8"))

    return out


def associateip(ip, instance):
    """Associates the given Elastic IP Address with the given EC2 Instance"""
    if type(ip) is str:
        ip = getipjson(ip)

    if type(instance) is str:
        instance = getinstancejson(instance)

    command = config.awsexe + " ec2 associate-address --allocation-id " + getelasticallocationid(ip) + " --instance-id " + getinstanceid(instance) + " --profile " + config.profilename
    p = subprocess.Popen(command.split(" "), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = p.communicate()

    print(err.decode("utf-8"))


def disassociateip(ip):
    """Disassociates the given Elastic IP Address from its EC2 instance"""
    if type(ip) is str:
        ip = getipjson(ip)

    command = config.awsexe + " ec2 disassociate-address --public-ip " + getelasticpublicip(ip) + " --profile " + config.profilename
    p = subprocess.Popen(command.split(" "), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = p.communicate()

    print(err.decode("utf-8"))



def releaseip(ip):
    """Destroys the elastic ip address specified"""
    ip = getipjson(ip)

    command = config.awsexe + " ec2 release-address --allocation-id " + getelasticallocationid(ip) + " --profile " + config.profilename
    p = subprocess.Popen(command.split(" "), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = p.communicate()

    print(err.decode("utf-8"))

    return out


def displayelasticdashboard():
    """Display a dashboard with info on the Elastic IPs"""
    allips = getallelasticips()

    names = []
    publicips = []

    # Populate column data
    for ip in allips:
        instance = getassociatedinstance(ip)

        if instance == "":
            names.append("UNASSIGNED")
        else:
            names.append(getinstancename(instance))
        publicips.append(getelasticpublicip(ip))

    # ID
    idcol = createdashcol("Instance", names, leftborder=True)

    # Public IP
    publicipcol = createdashcol("Public IP", publicips)

    for x in range(0, len(idcol)):
        print(idcol[x] + publicipcol[x])


def displaydashboard():
    """Display a dashboard with all EC2 information"""
    import Utils
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
    namescol = Utils.createdashcol("Name", names, leftborder=True)

    # States
    statescol = Utils.createdashcol("State", states)

    # IP Addresses
    ipadressescol = Utils.createdashcol("IP Address", ipaddresses)

    for x in range(0, len(namescol)):
        print(namescol[x] + statescol[x] + ipadressescol[x])
