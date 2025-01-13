"""for filtering dlt messages
by Friedrich Zimmer
Copyright ARRK Engineering 2019-2023
"""


class DltFilter:
    """for filtering dlt messages"""

    def __init__(self, ecuid=None, apid=None, ctid=None, mstp=None, dltcommand=None):
        """defining the filter
        Args:
            ecuid(str): The ID of the ecu in the header(up to four letters)
            apid(str): The application-ID in the ext header(up to four letters)
            ctid(str): The context-ID in the ext header (up to four letters)
            mstp(int): The message type according to the ext header(0=log,1=trace,2=network,3=command)
            dltcommand(int): the dlt command id
        """

        self.ecuid = ecuid
        if self.ecuid is not None:
            # if length of ecuid is smaller than 4, the remaining bytes are filled with 0x00
            if len(self.ecuid) > 4:
                self.ecuid = self.ecuid[:4]
            while len(self.ecuid) < 4:
                self.ecuid += chr(0)

        self.apid = apid
        if self.apid is not None:
            if len(self.apid) > 4:
                self.apid = self.apid[:4]
            while len(self.apid) < 4:
                self.apid += chr(0)

        self.ctid = ctid
        if self.ctid is not None:
            if len(self.ctid) > 4:
                self.ctid = self.ctid[:4]
            while len(self.ctid) < 4:
                self.ctid += chr(0)

        self.mstp = mstp
        self.dltcommand = dltcommand

        print("Filter for ECU_ID  :" + str(self.ecuid))
        print("Filter for Application_ID  :" + str(self.apid))
        print("Filter for Context_ID  :" + str(self.ctid))

    def ok(self, msg):
        """checks if a message is ok or filtered out
        Returns:
            ok(bool): if it's ok to export this message or not
        """

        if self.ecuid is not None and self.ecuid != msg.header.ecuid:
            return False
        if self.apid is not None and (msg.header.htyp_UEH is False or self.apid != msg.ext_header.apid):
            return False
        if self.ctid is not None and (msg.header.htyp_UEH is False or self.ctid != msg.ext_header.ctid):
            return False
        if self.mstp is not None and (msg.header.htyp_UEH is False or self.mstp != msg.ext_header.mstp):
            return False
        if self.dltcommand is not None and (
                msg.h.htyp_UEH is False or msg.eh.mstp != 3 or msg.payloadctrl.dltcommand != self.dltcommand):
            return False

        return True
