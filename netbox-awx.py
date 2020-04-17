#!/usr/bin/env python

import json
import requests

# Netbox URL
URL = ''

# Netbox API Token
TOKEN = ''

# AWX Filter Tags
FILTER_TAGS = []

headers = {
    'Accept': 'application/json ; indent=4',
    'Authorization': 'Token %s' % (TOKEN),
}

api_url = URL + '/api/dcim/devices/'
hosts_list = []
devices = []
sites = {}
racks = {}
platforms = {}
tenants = {}
tags = {}
inventory = {}
hostvars = {}

# Get data from netbox

while api_url:
    api_output = requests.get(api_url, headers=headers)
    api_output_data = api_output.json()

    if isinstance(api_output_data, dict) and "results" in api_output_data:
        hosts_list += api_output_data["results"]
        api_url = api_output_data["next"]

# Filter hosts for AWX

for i in hosts_list:
    if FILTER_TAGS:
        if any(item in FILTER_TAGS for item in i['tags']):
            devices.append(i)
    else:
        devices.append(i)

# Populate inventory

for i in devices:
    if i['name']:
        if i['config_context']:
            hostvars.setdefault('_meta', {'hostvars': {}})['hostvars'][i['name']] = i['config_context']
        if i['site']:
            sites.setdefault('site_' + i['site']['slug'], {'hosts': []})['hosts'].append(i['name'])
            hostvars.setdefault('_meta', {'hostvars': {}})['hostvars'][i['name']].setdefault('tags', {})['site'] = i['site']['slug']
        if i['rack']:
            racks.setdefault('rack_' + i['rack']['name'], {'hosts': []})['hosts'].append(i['name'])
            hostvars.setdefault('_meta', {'hostvars': {}})['hostvars'][i['name']].setdefault('tags', {})['rack'] = i['rack']['name']
        if i['platform']:
            platforms.setdefault('platform_' + i['platform']['slug'], {'hosts': []})['hosts'].append(i['name'])
            hostvars.setdefault('_meta', {'hostvars': {}})['hostvars'][i['name']].setdefault('tags', {})['platform'] = i['platform']['slug']
        if i['tenant']:
            tenants.setdefault('tenant_' + i['tenant']['slug'], {'hosts': []})['hosts'].append(i['name'])
            hostvars.setdefault('_meta', {'hostvars': {}})['hostvars'][i['name']].setdefault('tags', {})['tenant'] = i['tenant']['slug']
        for t in i['tags']:
            tags.setdefault(t, {'hosts': []})['hosts'].append(i['name'])
            hostvars.setdefault('_meta', {'hostvars': {}})['hostvars'][i['name']].setdefault('tags', {})[t] = True

inventory.update(sites)
inventory.update(racks)
inventory.update(platforms)
inventory.update(tenants)
inventory.update(tags)
inventory.update(hostvars)

print(json.dumps(inventory, indent=4))
