#!/usr/bin/env python3

from jnpr.junos import Device
import json

# parameter device
HOST = '192.168.147.222'
USER = 'juniper'
PASS = 'juniper123'

# connect
dev = Device(host=HOST, user=USER, passwd=PASS)
dev.open()

# get RPC interface info
rpc_reply = dev.rpc.get_interface_information(detail=True, normalize=True)

result = []
for phy in rpc_reply.findall('.//physical-interface'):
    desc = phy.findtext('description')
    vlan_tagging = phy.findtext('vlan-tagging')
    for logi in phy.findall('.//logical-interface'):
        ip = logi.find('.//address-family[address-family-name="inet"]/interface-address/ifa-local')
        result.append({
            'interface': phy.findtext('name'),
            'logical_interface': logi.findtext('name'),
            'description': desc,
            'vlan_tagging': vlan_tagging,
            'ip_address': ip.text if ip is not None else None
        })

dev.close()

# print as JSON
print(json.dumps(result, indent=2))
