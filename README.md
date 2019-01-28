# cdp
This python module implement the CDP protocol on Cisco switches and will determine the following information about the switch that we are plugged into:

* The port
* Type of switch
* The name of the switch

## Requirements
This module requires two main libraries to access the ethernet port.

[pcapy library - https://pypi.python.org/pypi/pcapy] (https://pypi.python.org/pypi/pcapy)


[dpkt library - https://pypi.python.org/pypi/dpkt] (https://pypi.python.org/pypi/dpkt)


## Output
```
CDP Discover Application Starting...
All network interfaces on the computer are listed below:

['en0', 'p2p0', 'awdl0', 'bridge0', 'utun0', 'en1', 'utun1', 'vmnet1', 'en2', 'utun2', 'vmnet2', 'vmnet3', 'vmnet4', 'utun4', 'vmnet5', 'utun5', 'en5', 'vmnet8', 'lo0', 'gif0', 'stf0']


Currently Discovering CDP messages on port: en5

We are currently attached to: 881544e3e4ce which is a: MS220-8P on Port: Port 5

We are currently attached to: BasementSwitch which is a: WS-C3560G-24PS on Port: Gigabit Ethernet 1/0/1

We are currently attached to: 00180a526978 which is a: MS22 on Port: Port 14
```
## Limitations
The application does not have alot of error checking, therefore your usage may vary.   In addition, I have only tested this on the Mac OSX and it works fine.    The switches that I have tested are:

* Meraki MS 220
* Meraki MS 22
* Cisco 3560G

I'm making the assumption that it works with all switches running Version 2 of CDP.