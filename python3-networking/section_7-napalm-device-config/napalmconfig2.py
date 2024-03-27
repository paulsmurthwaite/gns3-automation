import json
from napalm import get_network_driver
driver = get_network_driver('ios')
iosvl2 = driver('192.168.122.72', 'lab', 'cisco')
iosvl2.open()

print ('Accessing 192.168.122.72')
iosvl2.load_merge_candidate(filename='acl.cfg')

diffs = iosvl2.compare_config()
if len(diffs) > 0:
    print(diffs)
    iosvl2.commit_config()
    print('Changes committed.')
else:
    print('No changes required.')
    iosvl2.discard_config()

iosvl2.close()