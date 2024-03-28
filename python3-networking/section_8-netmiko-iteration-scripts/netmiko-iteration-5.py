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

# Open devices file, split lines, read to variable
with open('commands_file') as f:
    commands_list = f.read().splitlines()

# Open devices file, split lines, read to variable
with open('devices_file') as f:
    devices_list = f.read().splitlines()

# Iterate over each device, using specified credentials
# passed from vars
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
    except (SSHException):
        print ('SSH is not enabled for device: ' + device)
        continue
    except (EOFError):
        print ('End of file while attempting device ' + device)
        continue
    except Exception as unknown_error:
        print ('Some other error: ' + str(unknown_error))
        continue

    # Open connection, send commands, print output
    output = net_connect.send_config_set(commands_list)
    print (output)