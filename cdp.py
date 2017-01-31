#! /usr/bin/env python
#
# This Python Application will use CDP to determine what port we are attached to in a switch.
# It is very generic but can be extended to gather different fields within the CDP packet.

import pcapy

from dpkt import ethernet


def on_cdp_packet(header, data):
    ether_frame = ethernet.Ethernet(data)

    # The Start of the CDP Packet is at byte position 22, but the important data starts at byte 26.
    # Let's also grab the len of the entire frame

    eth_len = len (ether_frame)

    start_of_cdp = 22

    start_of_cdp_data = 26

    # Start Iterating through the packet until we find the appropriate typeID fields.

    counter = start_of_cdp_data

    while counter<eth_len:

        # Grab first two bytes, these are the TYPEID of the CDP Packet
        typeid = 256 * ord(data[counter]) + ord(data[counter+1])
        # Grab the next two bytes which represent the length of this setion of the CDP Packet
        length = 256 * ord(data[counter+2]) + ord(data[counter+3])

#       print "Typeid: "+str(typeid) + " Length: "+str(length)

        # Finally, let's grab the entire data portion. This part houses the information fields
        cdp_field = data[counter+4:counter+length]

        # We are only looking for the Device ID (i.e., Switchname) and the Port ID that we are connected to.
        # However, this code can grab and parse any other data that we received.

        if typeid == 1:
            #print "Device ID Found: "+cdp_field
            switch_name = cdp_field
        elif typeid == 3:
            #print "Port ID Found: "+cdp_field
            port_id = cdp_field
        elif typeid == 6:
            #print "Switch Type Found: "+cdp_field
            switch_type = cdp_field

        # Let's increment past that current field and move to the next "TYPEID" location
        counter = counter + length



    print "\nWe are currently attached to: "+switch_name + " which is a: "+switch_type+ " on Port: "+ port_id






print "CDP Discover Application Starting..."

print "All network interfaces on the computer are listed below:\n"

print pcapy.findalldevs()
print "\n"

disc_port = "en5"
print "Currently Discovering CDP messages on port: "+disc_port

try:
    # Let's Open up a live capture of the port

    pcap = pcapy.open_live(disc_port, 65535, 1, 100)

    # Let's set up a filter for the CDP packet ID 0x2000

    pcap.setfilter('ether[20:2] == 0x2000')  # CDP filter

    try:
        while True:
            # When the packet is received, we can call "on_cdp_packet" to process the data
            pcap.dispatch(1, on_cdp_packet)
    except KeyboardInterrupt, e:
        pass
except Exception, e:
    print e
