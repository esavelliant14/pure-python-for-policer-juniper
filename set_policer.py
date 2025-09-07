#!/usr/bin/env python3
from jnpr.junos import Device
from jnpr.junos.utils.config import Config

# ambil input dari user
device_ip = input("Masukkan IP Router: ")
username = "juniper"
password = "juniper123"
iface_name = input("Masukkan nama interface (misal em1): ")
unit_name = input("Masukkan unit (misal 10): ")
policer_input_value = input("Masukkan nilai policer INPUT (misal 30M): ")
policer_output_value = input("Masukkan nilai policer OUTPUT (misal 30M): ")

# buka koneksi ke device
with Device(host=device_ip, user=username, passwd=password) as dev:
    with Config(dev, mode='exclusive') as cu:
        # Buat konfigurasi dalam format XML
        config_xml = f"""
        <configuration>
          <interfaces>
            <interface>
              <name>{iface_name}</name>
              <unit>
                <name>{unit_name}</name>
                <family>
                  <inet>
                    <policer>
                      <input>{policer_input_value}</input>
                      <output>{policer_output_value}</output>
                    </policer>
                  </inet>
                </family>
              </unit>
            </interface>
          </interfaces>
        </configuration>
        """
        # load configuration
        cu.load(config_xml, format='xml')
        # commit perubahan
        cu.commit()
        print(f"Policer input/output berhasil diset pada {iface_name} unit {unit_name}.")
