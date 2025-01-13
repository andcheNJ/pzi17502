import threading
from time import sleep

from scapy.layers.l2 import Ether, Dot1Q
from scapy.packet import bind_layers
from scapy.sendrecv import sniff

from dlt_logger import DEFAULT_IP
from dltmodules import pcap_reading
from dltmodules.dlt_export import DltExport


class DltSnifferThread(pcap_reading.DltListener):
    """ inherits the methods __init__ and sniffer_dlt from DltListener

        Args:
            ip(int) : ip adress of loggiong device
            pkt: a scapy packet
            exporter: Export to .dlt or .csv
            dltfilter: Optional requriement for filter

        Returns:
             the message as binary string that can be sent by TCP """

    def __init__(self, iface, ip=DEFAULT_IP, exporter=DltExport(), dltfilter=None):
        """ initiating parameters from command line"""

        super().__init__(ip, exporter, dltfilter)

        self.iface = iface

        # sniff(iface=iface, prn=self.sniffer_dlt, store=False)
        self._t = threading.Thread(target=self.sniffthread, daemon=True)

    def sniffthread(self):
        sniff(iface=self.iface, prn=self.sniffer_dlt, store=False)

    def start_sniffing(self):

        print("Verbindung mit Interface " + self.iface + " wird hergestellt")
        self.exp.start_export()

        if self.ipfilter != "":
            print("Daten werden von " + self.ipfilter + " empfangen...")

        # Bind vlan layers
        bind_layers(Ether, Dot1Q, type=0x9100)
        bind_layers(Dot1Q, Dot1Q, type=0x8100)

        self._t.start()

    def stop_sniffing(self):
        """ for stopping the sniffing """
        self._stop = True
        print("Reading was stopped by input")
        sleep(1)
        self.exp.end_export()

        # reading is running in a thread,
