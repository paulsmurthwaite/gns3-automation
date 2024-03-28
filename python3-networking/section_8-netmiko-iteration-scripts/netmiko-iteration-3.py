"""
Connect to devices specified in devices_file
Apply commands specified in commands_list
"""

from netmiko import ConnectHandler

# Open commands file, split lines, read to variable
with open('commands_file') as f:
    commands_list = f.read().splitlines()

# Open devices file, split lines, read to variable
with open('devices_file') as f:
    devices_list = f.read().splitlines()

# Iterate over each device, using specified account
for devices in devices_list:
    print ('Connecting to device: ' + devices)
    ip_address_of_device = devices
    ios_device = {
        'device_type': 'cisco_ios',
        'ip': ip_address_of_device,
        'username': 'psmurthw',
        'password': 'cisco'
    }

    # Open connection, send commands, print output
    net_connect = ConnectHandler(**ios_device)
    output = net_connect.send_config_set(commands_list)
    print (output)