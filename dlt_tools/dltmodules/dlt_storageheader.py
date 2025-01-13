"""For the header of .dlt files
by Friedrich Zimmer
Copyright ARRK Enineering 2019-2021
"""

from time import localtime, strftime

DLTSTORAGESTART = b'DLT\x01'


class DltStorageHeader:
    """for both binary to variables and variables to binary"""

    def __init__(self, binst=None, ecu=None, s=0, ms=0):
        """creates the storageheader according to the diagnostic log and trace protocol"""
        if binst is not None:
            self.binst = binst
            if len(binst) != 16:
                print("Error: Storage Header must have the length of exactly 16 bytes")
                return

            # interpreting the binary string
            # 32 bit time format + another 32 bit for the microseconds
            self.tmsp_seconds = int.from_bytes(binst[4:8], "little")
            self.tmsp_ms = int.from_bytes(binst[8:12], "little")

            # Internal ECU seems to be ignored by the DLT viewer
            self.ecu = binst[12:16].decode("utf-8", "ignore")
        else:
            self.ecu = ecu
            self.tmsp_ms = ms
            self.tmsp_seconds = s
            # creating the binary string
            try:
                self.binst = DLTSTORAGESTART + self.tmsp_seconds.to_bytes(4, byteorder='little') + \
                         self.tmsp_ms.to_bytes(4, byteorder='little') + self.ecu.encode('ascii')
            except UnicodeEncodeError:
                print("Error: Unicode error in DLT Storage header!")
                self.binst = b''

    def timestring(self):
        """returns the current time in the required format"""
        return str(strftime("%Y:%m:%d %H:%M:%S", localtime(self.tmsp_seconds))) + " " + str(self.tmsp_ms) + "ms"
