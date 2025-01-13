"""class for the dlt extended header
by Friedrich Zimmer
Copyright ARRK Enineering 2019-2021
"""


class DltExtHeader:
    """class for the dlt extended header"""

    def __init__(self, binst, header):
        """creating the extended header from the bytearray and header
            Args:
                binst(bytearray): the remaining byte string from the message
                header(DltHeader): the header object
        """

        if not header.htyp_UEH or len(binst) < 10:
            # Extended header is not used.
            self.verb = False
            self.mstp = 0
            self.mtin = 0
            self.noar = 0
            self.apid = ""
            self.ctid = ""
            # length of the header for pos in payload
            self.laenge = 0
        else:
            # binst of the extended header must be 10 byte binary string according to spec
            if len(binst) < 10:
                print("Error in packet " + str(header.ecuid) + " " + str(header.seid) + ": Ext header must be 10 bytes long")

            # Byte 0: MSIN (Message Info)
            msin = binst[0]

            # Bit 0: VERB (Verbose)
            self.verb = bool(msin & 0b0000001)
            # print("Verbose " + str(self.verb))

            # Bit 1-3: MSTP (Message Type)
            self.mstp = int(msin & 0b0001110) >> 1
            # For message type (mstp) only values 0 to 3 are defined. 4 will show "undefined"
            if self.mstp > 4 or self.mstp < 0:
                self.mstp = 4

            # Bit 4 - 7: MTIN(Message Type Info)
            self.mtin = int(msin & 0b11110000) >> 4

            # meaning of message type info (mtin) depends on the mstp. Siehe MESSAGETYPEINFO
            # only 1 to max 15 are defined. 0 will show "undefined"
            if self.mtin > 15 or self.mtin < 0:
                self.mtin = 0

            # Byte 1: NOAR (Number of Arguments)
            self.noar = int(binst[1])

            # Byte 2-5: APID (Application ID)
            self.apid = binst[2:6].decode("utf-8", "ignore")

            # Byte 6-9: CTID (Context ID)
            self.ctid = binst[6:10].decode("utf-8", "ignore")
            self.laenge = 10
