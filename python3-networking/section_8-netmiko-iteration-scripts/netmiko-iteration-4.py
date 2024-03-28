"""
Author: Paul Smurthwaite
Purpose: Prompt for credentials.  Connect to devices specified in devices_file.  Apply commands specified in commands_list.
"""


from getpass import getpass
from netmiko import ConnectHandler


# Prompt for credentials
username = input('SSH username: ')
password = getpass()

# Open commands file, split lines, read to variable
with open('commands_file') as f:
    commands_list = f.read().splitlines()

# Open devices file, split lines, read to variable
with open('devices_file') as f:
    devices_list = f.read().splitlines()

# Iterate over each device, using specified credentials
# passed from vars
for device in devices_list:
    print ('Connecting to device" ' + device)
    ios_device = {
        'device_type': 'cisco_ios',
        'ip': device, 
        'username': username,
        'password': password
    }

    # Open connection, send commands, print output
    net_connect = ConnectHandler(**ios_device)
    output = net_connect.send_config_set(commands_list)
    print (output)