import sys

from scapy.layers.inet import IP
from scapy.layers.l2 import Ether, Dot1Q
from scapy.packet import Raw, Padding, bind_layers
from scapy.sendrecv import sniff

# from DLT_Tools.dlt_logreciever import DEFAULT_IP
from dltmodules import dlt_message, dlt_readheader


class DltListener:
    """needed by pcapreader and the sniffer
    the arguments are read by the child"""

    def __init__(self, ip, export, dltfilter):
        """ initiating the variables and the export. Called by child classes"""

        self._stop = False
        self.__carryover = []  # Carryover of the remaining bytes of the tcp payload to the next packet
        self._ips = []
        # self.__paketnumber = 0  # counter for the imported DLT TCP Packets

        self.exp = export
        self.interpreting = self.exp.interpreting_needed()

        self.ipfilter = ip
        if self.ipfilter != "":
            print("Lese Daten von IP " + self.ipfilter)
        else:
            print("Lese Daten von allen IP Adressen")

        self.filter = dltfilter

    def sniffer_dlt(self, pkt):
        """ for interpreting a packet recieved from scapy
            Args:
                pkt: a scapy packet

        """

        if self._stop:
            exit()

        if IP not in pkt:
            return

        current_src_ip = pkt[IP].src
        # pkt.show()
        # IP Filter shows only messages from and to a certain IP
        if self.ipfilter != "" and self.ipfilter != current_src_ip and self.ipfilter != pkt[IP].dst:
            return

        # ToDo: unification with previous packet will happen here. The old payload will be concatenated with the new payload. pl = carryover+ new payload

        # only by tcp or udp
        if "UDP" in pkt:
            tcp_udp = pkt["UDP"]
        elif "TCP" in pkt:
            tcp_udp = pkt["TCP"]
        else:
            return
        # print('Number2')
        # Only Source Port 349x for DLT
        if tcp_udp.sport != 3490 and tcp_udp.dport != 3490 and tcp_udp.sport != 3491 and tcp_udp.dport != 3491 and \
                tcp_udp.dport != 3492 and tcp_udp.dport != 3492:
            return
        # print('Number3')
        ip_id = self.get_ipid(current_src_ip)

        # print("Carryover: " + str(self.__carryover[ip_id]))
        # print("raw: " + str(bytes(pkt["Raw"])))

        # the needed data are included in "raw"
        # rest of the previous tcp-payload and the new tcp payload will be the new binary string to read from
        if Raw in pkt:
            pl = self.__carryover[ip_id] + bytes(pkt["Raw"])  # + bytes(tcp_udp.payload)
        else:
            return
        # print('Number4')

        # the padding part of the ethernet protocol is accidently added to the TCP payload by scapy
        # These 3-6 Byte get subtracted by this function
        if Padding in pkt:
            print("Warning: Padding is removed")
            # pkt.show()
            pl = pl[:-len(pkt["Padding"])]
        # print('Number5')

        # Reading DLT Headers
        header = dlt_readheader.DltHeader(pl[0:16])

        # print("Filter " + self.filter.ecuid + " ECUID: " + header.ecuid)

        # if the packetlenth is extremely large or small, it's a sign, that we're reading at the wrong position
        # This can happen at a packet loss
        # Rest of the packet gets ignored and reading starts with the new packet
        if (header.packetlength > 3000 or header.packetlength < 8) and "TCP" in pkt:
            print("WARNING: DLT-Packet length " + str(header.packetlength) +
                  " from " + current_src_ip + " is not plausible. There probably is a packet loss. "
                                              "The rest of the TCP Paket is ignored.")
            self.__carryover[ip_id] = b""
            return
        # print('Number6')
        len_remaining_payload = len(pl)

        # if the remaining string is shorter than 16 bytes, the header can't be read
        # will be carried over into the next string
        if len_remaining_payload < 16:
            print("WARNING: Payload is only " + str(len_remaining_payload))
            if "TCP" in pkt:
                self.__carryover[ip_id] = pl
            return
        # print('Number7')

        # print('Number8')
        pos = 0
        error = False
        # reading all dlt Packet from the binary tcp payload
        # print('payload ' + str(len_remaining_payload))
        # print('Packetlength' + str(header.packetlength))
        if ("UDP" in pkt) and len_remaining_payload < header.packetlength:
            print("WARNING: DLT packet length of " + str(header.packetlength) + " is bigger than payload " +
                  str(len_remaining_payload))
            # ToDo: Instead of just skipping the big payloads, we should combine the different parts of this ethernet
            #  frame. This way, we can also interpret the big DLTs. carryover =
            return

        # reading dlt packets of the
        while len_remaining_payload >= header.packetlength:
            # print('Number9')
            message = dlt_message.DltMessage(
                binst=pl[pos + header.headerlength():pos + header.packetlength],
                header=header,
                interpreted=self.interpreting)
            # print('Number10')
            # filter appid and ctid in message.ext_header.apid and message.ext_header.ctid

            #  print("APID: " + message.ext_header.apid)

            # First part is regarding if the filter is exists or not ... Second Part is regarding
            # The inside context of the filter...
            if (not self.filter.ecuid or (self.filter.ecuid == header.ecuid)) \
                    and (not self.filter.apid or (self.filter.apid == message.ext_header.apid)) \
                    and (not self.filter.ctid or (self.filter.ctid == message.ext_header.ctid)):

                # saving the read data into screen, csv or dlt. Returns true if maximum amount of messages
                if self.exp.export_message(message, pkt=pkt):
                    print(str(self.exp.amount) + " messages were exported")
                    self.exp.end_export()
                    sys.exit()
                # print('Number11')
            # Manual cancellation or by external program

            # print('Number12')
            if hasattr(message, 'payload-verbose') and message.payload_verbose.error:
                error = True
                break
            pos += header.packetlength
            len_remaining_payload -= header.packetlength
            # print('Number13')
            # reading the header of the next message
            # checks if the remaining binary string is long enough for a header
            # then it chekcs if the complete next dlt message fits into the remaining binary string
            if len_remaining_payload < 16:
                break
            else:
                header = dlt_readheader.DltHeader(pl[pos:pos + 16])

                if header.packetlength < 5:
                    print("WARNING: DLT-packet length " + str(header.packetlength) + " Byte from " + current_src_ip +
                          " according to header.")
                    error = True
                    break

        # The rest of the binary string is stored and will be attached in front of the next TCP packet
        if error:
            print("Warning: Because of an Error no Bytes will be carried over to the next cycle")
            self.__carryover[ip_id] = b""
        else:
            self.__carryover[ip_id] = pl[pos:]

    def get_ipid(self, ip):

        for i in range(0, len(self._ips)):
            if self._ips[i] == ip:
                return i
        # new ip
        self._ips.append(ip)
        self.__carryover.append(b"")
        return len(self._ips) - 1


class DltPcapReader(DltListener):
    """ for reading from pcap file. For example recorded by wireshark"""

    def __init__(self, filename, ip, exporter, dltfilter=None):
        """ initiating from command line"""

        super().__init__(ip, exporter, dltfilter)

        # Source pcap file:
        self.filename = filename
        print('File source: ' + str(self.filename))
        if len(self.filename) < 5:
            print("Invalid filename")
            exit(-1)
        if self.filename[-4:] != "apng" and self.filename[-4:] != "pcap":
            print("Warning: Unknown filename extension: " + self.filename[-4:])

        self.exp.start_export()

        print("Data is read from file")

        # Bind vlan layers
        bind_layers(Ether, Dot1Q, type=0x9100)
        bind_layers(Dot1Q, Dot1Q, type=0x8100)

        try:
            sniff(offline=self.filename, prn=self.sniffer_dlt, store=False)
        except FileNotFoundError:
            print("ERROR: File not found")

        print("End of data")

        self.exp.end_export()

        return
