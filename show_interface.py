from jnpr.junos import Device
from lxml import etree  # untuk pretty print XML

HOST = '192.168.147.222'
USER = 'juniper'
PASS = 'juniper123'

dev = Device(host=HOST, user=USER, passwd=PASS)
dev.open()

rpc_reply = dev.rpc.get_interface_information(detail=True, normalize=True)

# cetak XML mentah supaya lihat semua node
print(etree.tostring(rpc_reply, pretty_print=True).decode())

dev.close()
