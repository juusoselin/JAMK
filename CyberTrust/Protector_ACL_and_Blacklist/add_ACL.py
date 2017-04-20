#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, getopt, csv, json, uuid, datetime
import requests

# Suppress InsecureRequestWarning in urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

## Define variables
controller_ip = '192.168.83.211'
auth = json.loads('{"login":{"user":"sdn","password":"skyline","domain":"sdn"}}')
auth_path = 'https://' + controller_ip + ':8443/sdn/v2.0/auth'
api_path = 'https://' + controller_ip + ':8443/sdn/fw/v1.0/firewall'
headers = {'content-type': 'application/json'}

## Manage authentication
response = requests.post(auth_path, data=json.dumps(auth), headers=headers, verify=False)
data = response.json()
token = data[u'record'][u'token']
timestamp = data[u'record'][u'expiration'] / 1000
token_expiration = datetime.datetime.fromtimestamp(timestamp)
headers['X-Auth-Token'] = token


def main():
    file = arguments(sys.argv[1:])
    print("Using file:\t" + str(file))
    add_rules_to_ACL(file)


def arguments(argv):
    '''
    Parse commandline arguments
    '''
    try:
        opts, args = getopt.getopt(argv, "h", ["help", "input="])
    except getopt.GetoptError as e:
        print("\n")
        print(str(e))
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt == "--input":
            return arg
        else:
            usage()
            sys.exit()

def add_rules_to_ACL(list_of_rules):
    '''
    Add rules from a file to ACL
    '''
    rules = []
    f = open(list_of_rules, 'rt')
    try:
        reader = csv.reader(f)
        for line in reader:
            rule = {}
            if line[0] is not "":
                rule['id'] = line[0]
            else:
                rule['id'] = str(uuid.uuid4())
            rule['name'] = line[1]
            rule['src'] = line[2]
            rule['srcPort'] = line[3]
            rule['srcMask'] = line[4]
            rule['dst'] = line[5]
            rule['dstPort'] = line[6]
            rule['dstMask'] = line[7]
            rule['protocol'] = line[8]
            rule['action'] = line[9]
            rule['appId'] = line[10]
            rule['bidirectional'] = line[11].lower()
            rule['vlanId'] = line[12]
            rule['disabled'] = line[13].lower()
            if line[14] is not "":
                rule['scheduledInitialDate'] = line[14]
            else:
                rule['scheduledInitialDate'] = None
            if line[15] is not "":
                rule['scheduledFinalDate'] = line[15]
            else:
                rule['scheduledFinalDate'] = None
            rules.append(rule)
        print(json.dumps(rules, indent=4))

    finally:
        f.close()

    for item in rules:
        response = requests.post(api_path, data=json.dumps(item), headers=headers, verify=False)

def usage():
    '''
    Print usage info
    '''
    print(
    '''
    USAGE:

    --help          Display this help
    --input         CSV file containing all the rules
    ''')

if __name__ == "__main__":
    main()
