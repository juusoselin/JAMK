#!/bin/env python2
# -*- coding: utf-8 -*-

import web
import hpsdnclient as hp
import requests, json
from collections import OrderedDict

# Suppress InsecureRequestWarning in urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Web application parameters
urls = (
    '/', 'Index',
    '/delete', 'Delete',
    '/static'
)
app = web.application(urls, globals())
render = web.template.render('templates/')

# Controller variables
controller_ip = '10.0.1.210'
auth = hp.XAuthToken(user='sdn', password='skyline', server=controller_ip)
api = hp.Api(controller=controller_ip, auth=auth)
dpid = '00:00:70:b3:d5:6c:d6:39'

#####################
#   Web pages       #
#####################

message = ""
non_match_list = ['action', 'priority', 'table_id', 'output', 'ipv4_src_mask', 'ipv4_dst_mask']

class Index:
    def GET(self):
        return render.index(flows = listFlows(), message = message)

    def POST(self):
        values = []
        form = web.input()
        if form.action == 'Delete All Flows':
            for flow in getFlows():
                deleteFlows(dpid, flow)
            message = "All flows has been deleted"
        elif form.action == 'Insert Flow':
            ipv4_src_mask = form.ipv4_src_mask
            ipv4_dst_mask = form.ipv4_dst_mask
            for key, value in form.items():
                tmp_value = {}
                if (value) and (key not in non_match_list):
                    if key == 'ipv4_src':
                        dict_tmp = {}
                        dict_tmp[key] = value.encode('ascii', 'ignore')
                        if ipv4_src_mask:
                            dict_tmp['mask'] = ipv4_src_mask.encode('ascii', 'ignore')
                        tmp_value = dict_tmp
                    elif key == 'ipv4_dst':
                        dict_tmp = {}
                        dict_tmp[key] = value.encode('ascii', 'ignore')
                        if ipv4_src_mask:
                            dict_tmp['mask'] = ipv4_dst_mask.encode('ascii', 'ignore')
                        tmp_value = dict_tmp
                    else:
                        tmp_value[key] = value.encode('ascii', 'ignore')

                    values.append(tmp_value)

            addFlow(values, form.table_id.encode('ascii', 'ignore'), form.priority.encode('ascii', 'ignore'), form.output.encode('ascii', 'ignore'))
            message = "Flow added"
        else:
            print("Not yet implemented")

        return render.index(flows = listFlows(), message = message)

class Delete:
    def GET(self):
        data = web.input()
        if data.id >= 0:
            deleteFlows(dpid, getFlows()[int(data.id)])

        return render.index(flows = listFlows(), message = "Flow deleted")

#####################
#   Functions       #
#####################

def addFlow(match_list, table_id=None, priority=None, output_port=None):
    '''
        Add new flow to the flow table
    '''

    if table_id is None:
        table_id = '0'
    if priority is None:
        priority = '100'
    if output_port is None:
        output_port = ''

    # Define output port
    output = {}
    output['output'] = output_port

    # Define instructions
    instructions = []
    actions = []
    actions.append(output)
    apply_actions = {}
    apply_actions['apply_actions'] = actions
    instructions.append(apply_actions)

    # Generate flow
    flow = {}
    flow['priority'] = priority
    flow['table_id'] = table_id
    flow['match'] = match_list
    flow['instructions'] = instructions

    # Generate payload for REST api
    payload = {}
    payload['flow'] = flow

    # Push flow to a flow table
    payload_json = json.dumps(payload, indent=4)
    print(payload_json)
    api.add_flows(dpid, payload)

def getFlows():
    '''
        Get all the flows from the flow table
    '''
    current_flows = []
    flows = api.get_flows(dpid)
    for flow in flows['flows']:
        current_flows.append(flow)
    return current_flows

def listFlows():
    '''
        List all the flows from the flow table
    '''
    current_flows = getFlows()
    flows_list = []
    for flow in current_flows:
        tmp_flow = []
        for key, value in flow.items():
            tmp = {}
            tmp[key] = (value)
            tmp_flow.append(tmp)
        flows_list.append(tmp_flow)
    return flows_list

def deleteFlows(dpid, flow):
    '''
        Delete flow from the flow table
    '''
    payload = {}
    payload['flow'] = flow
    api.delete_flows(dpid, payload)

if __name__ == "__main__":
    app.run()
