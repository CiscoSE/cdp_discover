#! /usr/bin/env python
# A small script for cdp devices discovery

import sys
import pcapy
import socket

from dpkt import ethernet
from dpkt import cdp


def discover_neighbors(interface, timeout=100):


    def on_cdp_packet(header, data):
        ether_frame = ethernet.Ethernet(data)

        start_of_cdp = 22
#        print "Version: {:02x}".format(ord(data[start_of_cdp]))
#        print "TTL: {:02x}".format(ord(data[start_of_cdp+1]))

        start_of_dev = 26
        devid_len = ord(data[start_of_dev+3])

#        print "Length = "+str(devid_len)
#        print "Length: {:02x} {:02x}".format(ord(data[28]),ord(data[29]))

        switch_name = data[start_of_dev+4:start_of_dev+devid_len]
#        print "Switch Name: "+switch_name

        start_of_addr = start_of_dev+devid_len+1
        addr_len = ord(data[start_of_addr+2])

#        print "Address fields start at byte position: "+str(start_of_addr)
#        print "Address length: "+str(addr_len)
#        print "Length: {:02x} {:02x}".format(ord(data[start_of_addr+1]), ord(data[start_of_addr+2]))

        start_of_portid = start_of_addr+addr_len
        portid_len = ord(data[start_of_portid + 2])
#        print "Port ID fields start at byte position: "+str(start_of_portid)
#        print "Port ID length: "+str(portid_len)

        port_id = data[start_of_portid+3:start_of_portid+portid_len-1]
#        print "Port ID: "+port_id

        print "Attached to: Switch Name: "+switch_name + " on Port: "+ port_id

#        print "{:02x}".format(ether_frame[23])


#        ip = ether_frame.data

#        for c in ether_frame:
#            print "{:02x}".format(ord(c))

#        cdp = ether_frame.CDP.data

#        cdp_packet = cdp.CDP(ether_frame)

#        print cdp_packet

#
#        cdp_packet = CDP.
#        cdp_packet = ether_frame.CDP
#        cdp_packet = ether_frame.data

#        cdp_info = {}
#        for info in cdp_packet.data:
#            cdp_info.update({info.type: info.data})

#        addresses = [socket.inet_ntoa(x.data) for x in cdp_info[cdp.CDP_ADDRESS]]
#        print "Hey, %s is at %s." % (cdp_info[cdp.CDP_DEVID], ", ".join(addresses))

    try:
        pcap = pcapy.open_live(interface, 65535, 1, timeout)
        pcap.setfilter('ether[20:2] == 0x2000')  # CDP filter

        try:
            while True:
                # this is more responsive to  keyboard interrupts
                pcap.dispatch(1, on_cdp_packet)
        except KeyboardInterrupt, e:
            pass
    except Exception, e:
        print e


print "CDP Discover Application Starting..."

print "All network interfaces on the computer are listed below:\n"

print pcapy.findalldevs()
print "\n"

disc_port = "en5"
print "Currently Discovering CDP messages on port: "+disc_port

discover_neighbors(disc_port)
