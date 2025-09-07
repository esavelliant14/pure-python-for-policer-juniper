from jnpr.junos import Device
from lxml import etree


device_ip = input("Masukkan IP Router (misal 192.168.147.222): ")
iface_name = input("Masukkan nama interface (misal em1): ")

dev = Device(host=device_ip, user='juniper', passwd='juniper123')
dev.open()

# Ambil config interface
filter_xml = etree.XML(f'''
<configuration>
  <interfaces>
    <interface>
      <name>{iface_name}</name>
    </interface>
  </interfaces>
</configuration>
''')

cfg = dev.rpc.get_config(filter_xml=filter_xml)

# Parsing data
interface_name = cfg.findtext('.//interface/name')



for unit in cfg.xpath('.//unit'):
    unit_name = unit.findtext('name')
    attr_unit = unit.get('inactive')
    if attr_unit:
        status_unit = "Inactive"
    else:
        status_unit = "Active"
    #ip_list = [addr.text for addr in unit.xpath('family/inet/address/name')]
    #ip = ", ".join(ip_list) if ip_list else "None"
    ip_list = []
    for addr_el in unit.xpath('family/inet/address'):
        ip_addr = addr_el.findtext('name')
        inactive_attr = addr_el.get('inactive')
        if inactive_attr:  # ada attribute inactive
            ip_list.append(f"{ip_addr}(inactive)")
        else:
            ip_list.append(ip_addr)
    ip = ", ".join(ip_list) if ip_list else "None"
    description = unit.findtext('description')
    #status policer
    find_status_policer = unit.find('.//family/inet/policer')
    if find_status_policer is None:
        status_policer = "None"
    else:
        attr_policer = find_status_policer.get('inactive')
        if attr_policer:
            status_policer = "Inactive"
        else:
            status_policer = "Active"

    #status policer input
    find_status_input_policer = unit.find('.//family/inet/policer/input')
    if find_status_input_policer is None:
        status_input_policer = "None"
    else:
        attr_input_policer = find_status_input_policer.get('inactive')
        if attr_input_policer:
            status_input_policer = "Inactive"
        else:
            status_input_policer = "Active"
    #status policer output
    find_status_output_policer = unit.find('.//family/inet/policer/output')
    if find_status_output_policer is None:
        status_output_policer = "None"
    else:
        attr_output_policer = find_status_output_policer.get('inactive')
        if attr_output_policer:
            status_output_policer = "Inactive"
        else:
            status_output_policer = "Active"
    #value policer input & output
    input_policer = unit.findtext('family/inet/policer/input')
    output_policer = unit.findtext('family/inet/policer/output')
    vlan_id = unit.findtext('vlan-id')
    

    print(f"Hostname: {dev.facts['hostname']}" )
    print(f"Interface: {interface_name}")
    print(f"Unit: {unit_name}")
    print(f"Status Unit: {status_unit}")
    print(f"Description: {description}")
    print(f"IP Address: {ip}")
    print(f"VLAN ID: {vlan_id}")
    print(f"Policer status: {status_policer}")
    print(f"Policer Input status: {status_input_policer}")
    print(f"Policer Output status: {status_output_policer}")
    print(f"Input policer: {input_policer}")
    print(f"Output policer: {output_policer}\n")

dev.close()
