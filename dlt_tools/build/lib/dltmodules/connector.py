from dltmodules import dlt_readheader
from dltmodules import dlt_message
from dltmodules import dlt_export, dlt_createcontrolrequest

import socket
import threading


# this class is also used by the control message tools like dlt_getSoftwareVersion.py
class DltConnectorThread:
    """Class for connecting to an ECU via DLT, recieving and sending messages"""

    # screen=True, csv_filename=None, dlt_filename=None,
    def __init__(self, ip, exp=dlt_export.DltExport(), dltfilter=None, buffering=False):
        """
            Initiating the connecttion and reading in a thread

            Args:
                ip (str): IPv4 as String
                exp(DltExport): Exporter Object including target, amount...
                dltfilter(DltFilter): filterobject, where the various filters are stored
                buffering(bool): if you want to store the messages in a buffer list
        """

        # self._screen = screen
        # amount = 0 means, that reading won't stop until an error or a stop from outside
        self.filter = dltfilter
        self.ip = ip

        self.exp = exp
        self.interpreting = exp.interpreting_needed()

        self._buffering = buffering
        if self._buffering:
            self.buffer = []

        # rownumber is the number of rows after the filter, allrownumber is the number of rows before the filter
        # this also includes the sent messages
        self.rownumber = 0
        self.allrownumber = 0
        # counts the sent messages
        self.countersent = 0

        print("Starting TCP/IP Socket...")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # reading is running in a thread,
        self.__stop = False
        self._t = threading.Thread(target=self._do_reading)

    def start_reading(self):
        self.exp.start_export()

        print("Connect with IP " + self.ip + "...")
        try:
            self.sock.connect((self.ip, 3490))
        except ConnectionRefusedError:
            print("Error! [WinError 10061] Unable to connect, "
                  "because the target computer refused to connect")
            exit()

        print("Recieving Data...")
        self._t.start()

    def _do_reading(self):
        """ loop for reading the log messages"""

        # Übertrag des Byterests des Payloads an das nächste Paket
        # Transfer of the byte remainder of the payload to the next packet
        stream = b""
        # paketnummer = 0
        pos = 0
        error = False

        # for packetnumber in range(0, amount):
        while not self.__stop:
            msg = self.sock.recv(2048)
            stream += msg

            # first reading of a header
            header = dlt_readheader.DltHeader(stream[0:16])

            while header.packetlength <= len(stream):
                message = dlt_message.DltMessage(
                    stream[pos + header.headerlength():pos + header.packetlength],
                    header,
                    interpreted=self.interpreting)

                self.allrownumber += 1

                if message.error:
                    break

                # message only gets exported if there is no filter or it passes the filter
                if self.filter is None or self.filter.ok(message) is True:
                    if self.export_message(message):
                        print("Requested amount of " + str(self.exp.counter) + " rows finished")
                        self.__stop = True

                if self.__stop:
                    break

                # next row:
                # the already read part of the stream gets cut off
                stream = stream[header.packetlength:]

                if len(stream) < 16:
                    break

                header = dlt_readheader.DltHeader(stream[0:16])
                if header.packetlength < 16:
                    print("WARNING: DLT-packetlength " + str(header.packetlength) + "Byte")
                    error = True
                    break

            if error:
                print("Because of an error, reading was stopped")
                self.__stop = True

            if self.__stop:
                break

        print("Reading ended after " + str(self.rownumber) + " rows.")
        self.sock.close()
        self.exp.end_export()

        print("Connection closed")

    def stop_reading(self):
        """ for stopping the recieving and disconnecting properly"""
        print("Reading was stopped manually")
        self.__stop = True

    def export_message(self, message):
        """ exporting to screen, csv, dlt and buffer

            Args:
                message(DLtMessage): the message that is exported
        """
        if self._buffering:
            self.buffer.append(message)
        return self.exp.export_message(message=message)

    def send_message(self, ctrlpayload):
        """ for sending a control message to the ECU
            Args:
                ctrlpayload(bytearray): the payload as binary string
        """

        if self._t.is_alive():
            print("sending control message ...")
            message = dlt_createcontrolrequest.sendrequest(ctrlpayload, counter=self.countersent)
            self.sock.sendall(message)
            self.countersent += 1

            # convert binary string back into an dlt message object
            header = dlt_readheader.DltHeader(message[0:16])
            message = dlt_message.DltMessage(message[16:header.packetlength], header)
            self.export_message(message)
            return self.rownumber
        else:
            print("Error: control message could not be sent, because there is no connection.")
            return -1

    def message_from_buffer(self, number):
        """ for accessing the buffer"""
        if not self._buffering:
            print("Warning: Buffering is deactivated")
            return None

        return self.buffer[number]
