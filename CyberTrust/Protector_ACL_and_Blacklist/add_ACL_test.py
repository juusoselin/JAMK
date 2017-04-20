#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, getopt, csv, json, uuid, datetime
import requests, random, string

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
    parameters = arguments(sys.argv[1:])
    add_rules_to_ACL(parameters)


def arguments(argv):
    '''
    Parse commandline arguments
    '''
    try:
        opts, args = getopt.getopt(argv, "h", ["help", "amount="])
    except getopt.GetoptError as e:
        print("\n")
        print(str(e))
        usage()
        sys.exit(2)
    amount = 1000
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt == "--amount":
            amount = arg
        else:
            usage()
            sys.exit()
    return amount

def add_rules_to_ACL(amount):
    '''
    Add rules from a file to ACL
    '''
    rules = []
    for i in range(1000):
        rule = {}
        rule['id'] = str(uuid.uuid4())
        rule['name'] = randomName(10)
        rule['src'] = None
        rule['srcPort'] = randomNumber(49151)
        rule['srcMask'] = None
        rule['dst'] = str(randomNumber(255)) + '.' + str(randomNumber(255)) + '.' + str(randomNumber(255)) + '.' + str(randomNumber(255))
        rule['dstPort'] = randomNumber(49151)
        rule['dstMask'] = None
        rule['protocol'] = "ANY"
        rule['action'] = "BLOCK"
        rule['appId'] = None
        rule['bidirectional'] = True
        rule['vlanId'] = None
        rule['disabled'] = False
        rule['scheduledInitialDate'] = None
        rule['scheduledFinalDate'] = None
        rules.append(rule)
    print(json.dumps(rules, indent=4))

    for item in rules:
        response = requests.post(api_path, data=json.dumps(item), headers=headers, verify=False)

def randomName(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

def randomNumber(limit):
    return random.randint(1, limit)

def usage():
    '''
    Print usage info
    '''
    print(
    '''
    USAGE:

    --help          Display this help
    --amount         CSV file containing all the rules
    ''')

if __name__ == "__main__":
    main()
