"""
Author: Paul Smurthwaite
Purpose: Prompt for credentials.  Connect to devices specified in devices_file.  Apply commands specified in commands_list.
"""


from getpass import getpass
from netmiko import ConnectHandler, NetmikoTimeoutException 
from netmiko.exceptions import NetmikoAuthenticationException
from paramiko.ssh_exception import SSHException


# Prompt for credentials
username = input('SSH username: ')
password = getpass()

# Read switches file
with open('commands_file_switch') as f:
    commands_list_switch = f.read().splitlines()

# Read routers file
with open('commands_file_router') as f:
    commands_list_router = f.read().splitlines()

# Read devices file
with open('devices_file') as f:
    devices_list = f.read().splitlines()

# Iterate over devices
for device in devices_list:
    print('Connecting to device: ' + device)
    ios_device = {
        'device_type': 'cisco_ios',
        'ip': device, 
        'username': username,
        'password': password
    }

    try:
        net_connect = ConnectHandler(**ios_device)
        output_version = net_connect.send_command('show version')
        
        # Initialize the version_found flag to False
        version_found = False
        software_ver = ''  # Keep track of the matched version

        # Check software versions
        for potential_version in ['vios_l2-ADVENTERPRISEK9-M', 'VIOS-ADVENTERPRISEK9-M']:
            if potential_version in output_version:
                print('Software version found: ' + potential_version)
                version_found = True
                software_ver = potential_version
                break  # Exit the loop if a version is found
            else:
                print('Did not find ' + potential_version)

        # Apply commands based on the found version
        if version_found:
            if software_ver == 'vios_l2-ADVENTERPRISEK9-M':
                print('Running ' + software_ver + ' commands')
                output = net_connect.send_config_set(commands_list_switch)
            elif software_ver == 'VIOS-ADVENTERPRISEK9-M':
                print('Running ' + software_ver + ' commands')
                output = net_connect.send_config_set(commands_list_router)
            # Add more conditions if there are other versions to handle
            print(output)
        else:
            print('No matching software version found for device commands.')

    except (NetmikoAuthenticationException, NetmikoTimeoutException, EOFError, SSHException) as e:
        print(f'Connection to device failed: {e}')
    finally:
        if 'net_connect' in locals():  # Check if net_connect is defined
            net_connect.disconnect()  # Ensure the connection is closed
