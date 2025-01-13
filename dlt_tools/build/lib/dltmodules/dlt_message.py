""" by Friedrich Zimmer
# 18.11.2019
Copyright ARRK Engineering 2019-2021
# Classes for the dlt message that gets created from a binary string
# No executable functions inside
# needed by filereader, pcapreader and connector
# https://www.autosar.org/fileadmin/user_upload/standards/foundation/1-0/AUTOSAR_PRS_DiagnosticLogAndTraceProtocol.pdf
"""

from dltmodules.dlt_readcontrolpayload import DltReadControlPayload
from dltmodules.dlt_readextheader import DltExtHeader
from dltmodules.dlt_readlogpayload import DltReadNonVerbose, DltReadVerbose

# Meaning of the message types in the extended header
MESSAGETYPE = ["Log", "Trace", "Network", "Control", "Undefined"]
# 2D ARRAY 5x16; 5= amount of messagetypes; 16 = max amount of MTINs in Networkmessage
MESSAGETYPEINFO = [["", "Fatal", "Error", "Warning", "Info", "Debug", "Verbose", "Undefined", "Undefined", "Undefined",
                    "Undefined", "Undefined", "Undefined", "Undefined", "Undefined", "Undefined"],
                   ["", "Variable", "Function In", "Function Out", "State", "VFB", "Undefined", "Undefined",
                    "Undefined", "Undefined", "Undefined", "Undefined", "Undefined", "Undefined", "Undefined",
                    "Undefined"],
                   ["", "IPC", "CAN", "FlexRay", "Most", "Ethernet", "SomeIP", "UserDefined", "UserDefined",
                    "UserDefined", "UserDefined", "UserDefined", "UserDefined", "UserDefined", "UserDefined",
                    "UserDefined"],
                   ["", "Request", "Response", "Undefined", "Undefined", "Undefined", "Undefined", "Undefined",
                    "Undefined", "Undefined", "Undefined", "Undefined", "Undefined", "Undefined", "Undefined",
                    "Undefined"],
                   ["", "Undefined", "Undefined", "Undefined", "Undefined", "Undefined", "Undefined", "Undefined",
                    "Undefined", "Undefined", "Undefined", "Undefined", "Undefined", "Undefined", "Undefined",
                    "Undefined"]]


class DltMessage:
    """ class for dlt Message objects
    includes also header and extended header
    """

    def __init__(self, binst, header, interpreted=True):
        """ creating the message object from the header and the remaining binary string
            Args:
                binst(bytearray): the remaining Byte string from the message
                header(DltHeader): the header object
                interpreted(Bool): If the DLT message has to be interpreted or not
        """
        self.binst = binst
        self.error = False
        self.header = header
        self.interpreted = interpreted

        # extended header of DLT protocol according to sepcification chapter 5.1.1.2
        # needed for apid and ctid filter
        self.ext_header = DltExtHeader(binst, header)

        # not needed if only conversion from pcap to dlt-file
        if interpreted:
            if header.htyp_MSBF:
                endian = "big"
            else:
                endian = "little"

            # Start Payload
            # control message (mstp == 3) is always non verbose
            if self.ext_header.mstp == 3:
                self.payload_ctrl = DltReadControlPayload(binst[self.ext_header.laenge:], endian, self.ext_header.mtin)
            elif not self.ext_header.verb:
                # Non Verbose Mode (= short Data format that has to be interpreted with a FIBEX file
                # FIBEX is not implemented, yet
                self.payload_nvb = DltReadNonVerbose(binst[self.ext_header.laenge:], endian)
            else:
                # Datamessage in Verbose Mode
                self.payload_verbose = DltReadVerbose(binst[self.ext_header.laenge:], endian, self.ext_header.noar, header)

    def gettext(self):
        """returns the complete payload as text"""

        if self.ext_header.mstp == 3:  # Command
            return self.payload_ctrl.gettext()
        if self.ext_header.verb:
            # Text DataMessage at Verbose Mode
            text = ""
            # gibt alle Argumente mit Semikolon getrennt aus
            # outputs all arguments separated by semicolon
            for i in range(0, self.ext_header.noar):
                text += self.getargtext(i) + "; "
            return text
        # Data Message Non-Verbose Mode ist nicht implementiert
        # Data Message Non-Verbose Mode is not implemented
        return "Non Verbose MsgId: " + str(self.payload_nvb.msgid)

    def getargtext(self, arg):
        """returns a single Argument of the payload as text"""
        if self.ext_header.mstp == 3:  # Command
            # anzahl der argumente ist Kommando + Anzahl der Parameter
            # Number of arguments is Command + Number of Parameters
            if not hasattr(self, 'payload_ctrl') or arg > len(self.payload_ctrl.par):
                return ""
            return self.payload_ctrl.gettextlist()[arg]

        if not hasattr(self, 'payload_verbose') or arg >= self.ext_header.noar:
            return ""

        if (arg >= len(self.payload_verbose.variable)) or (arg >= len(self.payload_verbose.argument)):
            print("Error:  It is based on a non-existent argument " + str(arg) + " accessed!")
            return ""

        return self.payload_verbose.variable[arg] + self.payload_verbose.argument[arg]

    def getverboseasstring(self):
        """ returns the verbose status as string"""
        if self.ext_header.verb:
            return "verbose"

        return "non-verbose"
