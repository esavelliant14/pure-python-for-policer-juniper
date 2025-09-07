#!/usr/bin/env python3
from jnpr.junos import Device
from lxml import etree
import json
import re

# === KONFIG DEVICE ===
HOST = '192.168.147.222'
USER = 'juniper'
PASS = 'juniper123'

# === KONEKSI ===
dev = Device(host=HOST, user=USER, passwd=PASS)
dev.open()

# === AMBIL SEMUA INTERFACE ===
rpc_reply = dev.rpc.get_interface_information(
    interface_name='em1',  # filter langsung ke em1
    detail=True,
    normalize=True
)

result = []
for phy in rpc_reply.findall('.//physical-interface'):
    phy_name = phy.findtext('name')
    
    phy_vlan_tagging = phy.findtext('vlan-tagging')  # None kalau tidak ada

    for logi in phy.findall('.//logical-interface'):
        logical_name = logi.findtext('name')
        logical_desc = logi.findtext('description')

        # Ambil IP address (family inet)
        ip = logi.find('.//address-family[address-family-name="inet"]/interface-address/ifa-local')
        ip_addr = ip.text if ip is not None else None

        # Ambil VLAN ID
        vlan_id = None
        # cek node encapsulation-vlan-id atau vlan-id
        vlan_node = logi.findtext('encapsulation-vlan-id') or logi.findtext('vlan-id')
        if vlan_node:
            vlan_id = vlan_node
        else:
            # cek di link-address [ 0x8100.xx ]
            link_addr = logi.findtext('link-address')
            if link_addr and '0x8100.' in link_addr:
                # ambil angka setelah 0x8100.
                match = re.search(r'0x8100\.(\d+)', link_addr)
                if match:
                    vlan_id = match.group(1)

        result.append({
            'interface': phy_name,
            'logical_interface': logical_name,
            'description': logical_desc,
            'vlan_id': vlan_id,
            'ip_address': ip_addr
        })

dev.close()

# === CETAK JSON RAPI ===
print(json.dumps(result, indent=2))
