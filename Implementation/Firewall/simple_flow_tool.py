#!/bin/env python2
# -*- coding: utf-8 -*-

import hpsdnclient as hp
import requests, json, os

# Suppress InsecureRequestWarning in urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Controller variables
controller_ip = '10.0.1.210'
auth = hp.XAuthToken(user='sdn', password='skyline', server=controller_ip)
api = hp.Api(controller=controller_ip, auth=auth)
dpid = '00:00:70:b3:d5:6c:d6:39'

# Add all the .json files from "flows" directory
for filename in os.listdir('flows'):
    if filename.endswith('.json'):
        flow = json.loads(open('flows/' + filename).read())
        print(flow)
        api.add_flows(dpid, flow)
