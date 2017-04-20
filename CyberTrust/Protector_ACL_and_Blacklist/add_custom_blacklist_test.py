#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, getopt, json, uuid, datetime, time
import requests, string, random

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
    parameters = arguments(sys.argv[1:])
    counter = 0
    for i in range(2000):
        add_urls_to_blacklist(parameters, counter)
        counter = counter + 1
        print(counter)

def arguments(argv):
    '''
    Parse commandline arguments
    '''
    try:
        opts, args = getopt.getopt(argv, "h", ["help", "policy="])
    except getopt.GetoptError as e:
        print("\n")
        print(str(e))
        usage()
        sys.exit(2)
    policy = None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt == "--policy":
            policy = arg
        else:
            usage()
            sys.exit()
    return policy


def add_urls_to_blacklist(policy, counter):
    '''
    Add URLs from a file to a custom profile
    '''
    flow = {}
    flow['name'] = str(counter) + '_' + randomName(10)
    flow['desc'] = "Test list"
    flow['type'] = "Blacklist"
    list_id = str(uuid.uuid4())
    flow['id'] = list_id
    entries = []
    for i in range(1000):
        entry = {}
        entry['domain'] = '*.' + randomName(randomNumber(2, 10)) + '.' + randomName(randomNumber(2, 4))
        entry['active'] = True

        entries.append(entry)


    flow['entries'] = entries
    #print(json.dumps(flow, indent=4))

    response = requests.post(api_path_list, data=json.dumps(flow), headers=headers, verify=False)

    #  Create custom policy if required by the user
    createPolicyBasedOnList(str(counter) + '_' + randomName(12), list_id)


def createPolicyBasedOnList(name,  uuid_blacklist):
    '''
    Create custom policy using the blacklist provided
    '''
    flow = {}
    flow['id'] = ""
    flow['name'] = name
    flow['description'] = "temp"
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

    #print(json.dumps(policyEntry, indent=4))

    response = requests.put(api_path_policy, data=json.dumps(policyEntry), headers=headers, verify=False)

def randomName(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

def randomNumber(start, limit):
    return random.randint(start, limit)

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
