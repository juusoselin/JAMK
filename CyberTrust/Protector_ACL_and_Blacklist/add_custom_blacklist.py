#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, getopt, json, uuid, datetime, time
import requests

# Suppress InsecureRequestWarning in urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

## Define variables
controller_ip = '192.168.83.211'
auth = json.loads('{"login":{"user":"sdn","password":"skyline","domain":"sdn"}}')
auth_path = 'https://' + controller_ip + ':8443/sdn/v2.0/auth'
api_path_list = 'https://' + controller_ip + ':8443/sdn/networkprotector/v1.1/customlist'
api_path_policy = 'https://' + controller_ip + ':8443/sdn/networkprotector/v1.1/policies/dnsinspectionpolicy/8d205e5d-bc8b-4355-bac9-d9dfe16a5ae5'
headers = {'content-type': 'application/json'}

response = requests.post(auth_path, data=json.dumps(auth), headers=headers, verify=False)
data = response.json()
token = data[u'record'][u'token']
timestamp = data[u'record'][u'expiration'] / 1000
token_expiration = datetime.datetime.fromtimestamp(timestamp)
headers['X-Auth-Token'] = token


def main():
    file = arguments(sys.argv[1:])
    print("Using file:\t" + str(file[0]))
    add_urls_to_blacklist(file[0], file[1], file[2], file[3])


def arguments(argv):
    '''
    Parse commandline arguments
    '''
    try:
        opts, args = getopt.getopt(argv, "h", ["help", "input=", "name=", "desc=", "policy="])
    except getopt.GetoptError as e:
        print("\n")
        print(str(e))
        usage()
        sys.exit(2)
    input_file = None
    name = None
    desc = None
    policy = None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt == "--input":
            input_file = arg
        elif opt == "--name":
            name = arg
        elif opt == "--desc":
            desc = arg
        elif opt == "--policy":
            policy = arg
        else:
            usage()
            sys.exit()
    if input_file and name and desc is not None:
        return input_file, name, desc, policy
    else:
        usage()
        sys.exit()

def add_urls_to_blacklist(list_of_urls, name, desc, policy):
    '''
    Add URLs from a file to a custom profile
    '''
    flow = {}
    flow['name'] = name
    flow['desc'] = desc
    flow['type'] = "Blacklist"
    list_id = str(uuid.uuid4())
    flow['id'] = list_id
    entries = []
    f = open(list_of_urls, 'rt')
    try:
        for line in f.readlines():
            line = line.strip("\n")
            if line.startswith('www'):
                line = line.replace('www', '*')
            else:
                line = '*.' + line
            entry = {}
            entry['domain'] = line
            entry['active'] = True

            entries.append(entry)

    finally:
        f.close()

    flow['entries'] = entries
    print(json.dumps(flow, indent=4))

    response = requests.post(api_path_list, data=json.dumps(flow), headers=headers, verify=False)

    #  Create custom policy if required by the user
    if policy is not None:
        createPolicyBasedOnList(policy, list_id)


def createPolicyBasedOnList(name,  uuid_blacklist):
    '''
    Create custom policy using the blacklist provided
    '''
    flow = {}
    flow['id'] = ""
    flow['name'] = name
    flow['description'] = "Services on RGCE"
    flow['state'] = "ENABLED"
    flow['createTime'] = "1489753736668"
    flow['isDefault'] = False
    flow['type'] = "dnsinspectionpolicy"
    flow['vlanGroup'] = "38eec098-492b-4390-9310-f3c35893af0d"
    flow['blackList'] = uuid_blacklist
    flow['greyList'] = ""
    flow['repdvFilter'] = ""
    flow['whiteList'] = "default-whitelist-id"
    flow['schedule'] = "default-always-uid"
    flow['action'] = "Drop"

    policyEntry = {}
    policyEntry['policyEntry'] = flow

    print(json.dumps(policyEntry, indent=4))

    response = requests.put(api_path_policy, data=json.dumps(policyEntry), headers=headers, verify=False)

def usage():
    '''
    Print usage info
    '''
    print(
    '''
    USAGE:

    --help          Display this help
    --input         Text file containing all the FQDNs to be blocked
    --name          Name of the blacklist
    --desc          Description of the blacklist

    --policy [x]    Create policy with provided name (x)
    ''')

if __name__ == "__main__":
    main()
