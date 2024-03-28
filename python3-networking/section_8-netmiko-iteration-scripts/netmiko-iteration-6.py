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
    print ('Connecting to device: ' + device)
    ios_device = {
        'device_type': 'cisco_ios',
        'ip': device, 
        'username': username,
        'password': password
    }

    # Error Handling
    try:
        net_connect = ConnectHandler(**ios_device)
    except (NetmikoAuthenticationException):
        print ('Authentication failure: ' + device)
        continue
    except (NetmikoTimeoutException):
        print ('Timeout to device: ' + device)
        continue
    except (EOFError):
        print ('End of file while attempting device ' + device)
        continue
    except (SSHException):
        print ('SSH is not enabled for device: ' + device)
        continue
    except Exception as unknown_error:
        print ('Some other error: ' + str(unknown_error))
        continue

    # Types of devices
    list_versions = ['vios_l2-ADVENTERPRISEK9-M', 
                     'VIOS-ADVENTERPRISEK9-M'
                     ]

    # Check software versions
    for software_ver in list_versions:
        print ('Checking for ' + software_ver)
        output_version = net_connect.send_command('show version')
        int_version = 0 # Reset integer value
        int_version = output_version.find(software_ver) # Check software version
        if int_version > 0:
            print ('Software version found: ' + software_ver)
            break
        else:
            print ('Did not find ' + software_ver)

    if software_ver == 'vios_l2-ADVENTERPRISEK9-M':
        print ('Running ' + software_ver + ' commands')
        output = net_connect.send_config_set(commands_list_switch)
    elif software_ver == 'VIOS-ADVENTERPRISEK9-M':
        print ('Running ' + software_ver + ' commands')
        output = net_connect.send_config_set(commands_list_router)
    elif software_ver == 'C3750-ADVIPSERVICESK9-M':
        print ('Running ' + software_ver + ' commands')
        output = net_connect.send_config_set(commands_list_switch) 
    else:
        break   
    print (output)