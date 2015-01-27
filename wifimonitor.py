from scapy.all import *

PROBE_REQUEST_TYPE = 0
PROBE_REQUEST_SUBTYPE = 4

def PacketHandler(pkt):
	if pkt.haslayer(Dot11):
		if pkt.type == PROBE_REQUEST_TYPE and pkt.subtype == PROBE_REQUEST_SUBTYPE:
			print "MAC address: %s, SSID: %s" % (pkt.addr2, pkt.getlayer(Dot11ProbeReq).info)

def AllPacketHandler():
	data = {'last_mac': None}
	def packetHandler(pkt):
		if pkt.haslayer(Dot11) and pkt.addr2 != data['last_mac']:
				data['last_mac'] = pkt.addr2
				print "MAC address: %s" % (pkt.addr2)
	return packetHandler

sniff(iface='wlan1', prn = AllPacketHandler())