'''
In order to properly run, ensure that |iface| is in monitor mode.
Furthermore, run this Python script as sudo.
'''

import sys, os, signal
from scapy.all import *
from multiprocessing import Process

PROBE_REQUEST_TYPE = 0
PROBE_REQUEST_SUBTYPE = 4

# Set non-statically in the future.
iface = 'wlan1'
channel = 1

seen_mac_addresses = set()
seen_SSIDs = set()

def PacketHandler(pkt):
	if pkt.haslayer(Dot11):
		if pkt.type == PROBE_REQUEST_TYPE and pkt.subtype == PROBE_REQUEST_SUBTYPE:
			seen_mac_addresses.add(pkt.addr2)
			if pkt.getlayer(Dot11ProbeReq).info not in seen_SSIDs:
				seen_SSIDs.add(pkt.getlayer(Dot11ProbeReq).info)
			if pkt.getlayer(Dot11ProbeReq).info:
				print "MAC address: %s, SSID: %s" % (pkt.addr2, pkt.getlayer(Dot11ProbeReq).info)

def AllPacketHandler():
	data = {'last_mac': None}
	def packetHandler(pkt):
		if pkt.haslayer(Dot11) and pkt.addr2 != data['last_mac'] and pkt.addr2 not in seen_mac_addresses:
				data['last_mac'] = pkt.addr2
				seen_mac_addresses.add(pkt.addr2)
				print "MAC address detected: %s" % (pkt.addr2)
	return packetHandler

def hop_channels():
	channel = 0
	while True:
		try:
			channel = (channel % 14 + 1)
			os.system('iw dev %s set channel %d' % (iface, channel))
			print 'setting channel to %d' % (channel)
			time.sleep(5)
		except Exception as e:
			print "Channel hopping ceased."
			print e
			break

def signal_handler(signal, frame):
	p.terminate()
	p.join()
	print "Terminating monitoring."
	print "Now displaying detected IP addresses..."
	for address in seen_mac_addresses:
		print address

	print "Now printing observed SSID probe requests"
	for ssid in seen_SSIDs:
		print ssid

	sys.exit(0)

if __name__ == '__main__':
	print "Beginning packet capture..."
	p = Process(target = hop_channels)
	p.start()
	signal.signal(signal.SIGINT, signal_handler)
	sniff(iface=iface, prn = PacketHandler)