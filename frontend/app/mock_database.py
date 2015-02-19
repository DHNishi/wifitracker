import datetime

class Packet(object):
    def __init__(self):
        self.id = 0
        self.mac = "AA:AA:AA:AA:AA:AA"
        self.ssid = "Pretty Fly for a Wifi"
        self.time = datetime.datetime.now()
        self.signal = 60

def getPackets(number):
    items = []
    for _ in xrange(number):
        items.append(Packet())
    return items