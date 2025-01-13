"""for reading and interpreting DLT package headers
by Friedrich Zimmer
Copyright ARRK Enineering 2019-2021
"""


class DltHeader:
    """ Standard Header of DLT protocol according to spec chapter 5.1.1.1"""

    def __init__(self, binst):
        """header must be 4 to 16 byte according to spec.
        Args:
            binst(bytes): byte string with exactly 16 bytes
        """
        upper_limit = 16
        lower_limit = 4

        # if lower_limit <= len(binst) <= upper_limit:
        #    # print("CORRECT DLT Format")
        #    pass
        # else:

        if (len(binst) < 4) or (len(binst) > 16):
            print("Error: Header String must have 4 to 16 Bytes and not " + str(len(binst)))
            self.htyp_UEH = False
            self.htyp_WEID = False
            self.htyp_WSID = False
            self.htyp_WTMS = False
            self.packetlength = 0
            self.ecuid = ""
            self.binst = None
            return
        # print('Binary_String '+ str(binst.hex()))
        # Byte 0: HTYP (Header Type)
        htyp = binst[0]

        # Bit 0: UEH (Use Extended Header)
        self.htyp_UEH = bool(htyp & 0b0000001)
        # print("Use Extended Header:" + str(self.htyp_UEH))
        # Bit 1: MSBF (Most Significant Byte First)
        self.htyp_MSBF = bool(htyp & 0b0000010)
        # print("Most Significant Byte First:" + str(self.htyp_MSBF))
        # Bit 2: WEID (With ECU ID)
        self.htyp_WEID = bool(htyp & 0b00000100)
        # print("With ECU ID:" + str(self.htyp_WEID))
        # Bit 3: WSID (With Session ID)
        self.htyp_WSID = bool(htyp & 0b00001000)
        # print("With Session ID:" + str(self.htyp_WSID))
        # Bit 4: WTMS (With Timestamp)
        self.htyp_WTMS = bool(htyp & 0b00010000)
        # print("With Timestamp:" + str(self.htyp_WSID))
        # Bit 5-7: VERS (Version Number)
        self.htyp_VERS = int(htyp & 0b11100000) >> 5
        # print("Version Number:" + str(self.htyp_VERS))

        # Byte    1: MCNT(Message    Counter)
        self.mcnt = int.from_bytes(binst[1:2], "big")
        # print("Message Counter:" + str(self.mcnt))

        # Byte    2 - 3: LEN(Length)
        # print('Binary_Conversion_of_srting'+str(binst[2:4]))
        self.packetlength = int.from_bytes(binst[2:4], "big", signed=False)
        # print('Packet length' + str(self.packetlength))
        # print("Packet Length:" + str(self.packetlength))

        if len(binst) < self.headerlength():
            print("Error: header Bytestring is only " + str(len(binst)) + " Bytes, while it should be " +
                  str(self.headerlength()) + " according to optional header fields")
            self.ecuid = ""
            self.binst = None
            return

        # Byte    4 - 7: ECU(ECU    ID)
        pos = 4
        if self.htyp_WEID:
            self.ecuid = binst[4:8].decode("utf-8", "ignore")
            pos += 4
        else:
            self.ecuid = "    "

        # Byte    8 - 11: SEID(Session    ID)
        if self.htyp_WSID:
            self.seid = int.from_bytes(binst[pos:pos + 4], "big", signed=False)
            pos += 4
        else:
            self.seid = 0
        # Byte    12 - 15: TMSP(Timestamp)
        if self.htyp_WTMS:
            self.tmsp = int.from_bytes(binst[pos:pos + 4], "big", signed=False)
        else:
            self.tmsp = 0
        self.binst = binst[:self.headerlength()]

    def headerlength(self):
        """ calculates the rel length of the header
        Returns:
            hl(int): header length
        """
        hl = 4
        if self.htyp_WEID:
            hl = hl + 4
        if self.htyp_WSID:
            hl = hl + 4
        if self.htyp_WTMS:
            hl = hl + 4
        return hl
