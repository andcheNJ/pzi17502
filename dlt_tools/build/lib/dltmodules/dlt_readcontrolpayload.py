"""
# Friedrich Zimmer November 2019
Copyright ARRK Enineering 2019-2021
# class for reading the payload of dlt control messages
# No executable
# the class is needed in the dlt message. The constants are also needed by the control messages
# https://www.autosar.org/fileadmin/user_upload/standards/foundation/1-0/AUTOSAR_PRS_DiagnosticLogAndTraceProtocol.pdf
"""

AMOUNTDLTCOMMAND = 36

# DLT Commands of chapter 5.3 of the specification including the old ones
DLTCOMMAND = ["0x0 Not Defined",
              "SetLogLevel",
              "SetTraceStatus",
              "GetLogInfo",
              "GetDefaultLogLevel",
              "StoreConfiguration",
              "RestoreToFactoryDefault",
              "SetComInterfaceStatus(only 4.0)",
              "SetComInterfaceMaxBandwidth(only 4.0)",
              "SetVerboseMode(only 4.0)",
              "SetMessageFiltering",
              "SetTimingPackets(only 4.0)",
              "GetLocalTime(only 4.0)",
              "SetUseECUID(only 4.0)",
              "SetUseSessionID(only 4.0)",
              "SetUseTimestamp(only 4.0)",
              "SetUseExtendedHeader(not supported)",
              "SetDefaultLogLevel",
              "SetDefaultTraceStatus",
              "GetSoftwareVersion",
              "MessageBufferOverflow(only 4.0)",
              "GetDefaultTraceStatus",
              "GetComInterfacelStatus (only 4.3)",
              "GetLogChannelNames",
              "GetComInterfaceMaxBandwidth(only 4.0)",
              "GetVerboseModeStatus(only 4.0)",
              "GetMessageFilteringStatus(not supported)",
              "GetIseECUID(not supported)",
              "GetUseSessionID(not supported)",
              "GetUseTimestamp(not supported)",
              "GetUseExtendedHeader(not supported)",
              "GetTraceStatus(only 4.3)",
              "SetLogChannelAssignment(only 4.3)",
              "SetLogChannelThreshold(only 4.3)",
              "GetLogChannelThreshold(only 4.3)",
              "BufferOverflowNotification(only 4.3)"]

# Servive IDs
# some of the services or only valid in 4.0 and some only in 4.3
# ToDo: Include the remaining 4.0 control type for reading
SET_LOGLEVEL = 0x1
SET_TRACESTATUS = 0x2
GET_LOGINFO = 0x3
GET_DEFAULTLOGLEVEL = 0x4
STORE_CONFIGURATION = 0x5
RESET_TOFACTORYDEFAULT = 0x6
SET_COMINTERFACESTATUS = 0x7  # Only DLT 4.0
SET_COMINTERFACEMAXBANDWIDTH = 0x8  # Only DLT 4.0
SET_VERBOSEMODE = 0x9  # Only DLT 4.0
SET_MESSAGEFILTERING = 0x0A
SET_TIMINGPACKETS = 0x0B
GET_LOCALTIME = 0x0C  # Only DLT 4.0
SET_USEECUID = 0x0D  # Only DLT 4.0
SET_USESESSIONID = 0x0E  # Only DLT 4.0
USE_TIMESTAMP = 0x0F  # Only DLT 4.0
SET_DEFAULTLOGLEVEL = 0x11
SET_DEFAULTTRACESTATUS = 0x12
GET_SOFTWAREVERSION = 0x13
MESSAGE_BUFFEROVERFLOW = 0x14  # Only DLT 4.0
GET_DEFAULT_TRACESTATUS = 0x15
GET_COMINTERFACESTATUS = 0x16
GET_LOGCHANNELNAMES = 0x17  # is the same like GetComInterfaceNames in 4.0
GET_COMINTERFACEMAXBANDWIDTH = 0x18
GET_VERBOSEMODESTATUS = 0x19  # Only 4.0
# The following are only valid in autosar 4.3:
GET_TRACESTATUS = 0x1F
SET_LOGCHANNELASSIGNMENT = 0x20
SET_LOGCHANNELTHRESHOLD = 0x21
GET_LOGCHANNELTHRESHOLD = 0x22
BUFFER_OVERFLOWNOTIFICATION = 0x23


class DltReadControlPayload:
    """
        binary -> object with variables
        is only called, if in the extended header the message type(mstp)=3
        endian and message type info (mtin) are already know from header and extended header
    """
    def __init__(self, binst, endian, mtin):
        """interprets the payload of a control message
            Args:
                binst(bytearray): payload of the control message as binary string
                endian(str): endian for interpreting the integer variables
                mtin(int): message type info
        """

        # first 4 Bytes are for the ID of the DLT Command
        self.dltcommand = int.from_bytes(binst[:4], endian)
        self.mtin = mtin

        self.par = []
        if self.mtin < 1 or self.mtin > 2:
            print("Error: Message Type info " + str(self.mtin) +
                  "does not exist. Only 1(Request) or 2(Response) are valid.")

        if self.dltcommand == 3842:  # connection_info ok found out by reverse engineering. Not found in specification!!
            self.par.append(int(binst[4]))
            self.par.append(binst[5:])
        elif self.dltcommand > AMOUNTDLTCOMMAND or self.dltcommand < 0:
            print("Warning: Control Messagetyp doesn't exit:" + str(self.dltcommand))
            self.dltcommand = 0
            if len(binst) > 4:
                self.par.append(binst[4:])
        # parameter (maximum 4, depending on the command)
        # starting at the fifth byte
        elif self.dltcommand == SET_LOGLEVEL:
            if mtin == 1:  # Request
                # 1: applicationid 4*uint 8
                self.par.append(binst[4:8].decode("ascii", "ignore"))
                # 2: contextidid 4*uint 8
                self.par.append(binst[8:12].decode("ascii", "ignore"))
                # 3 newLogLevel sint 8
                self.par.append(int(binst[12]))
                if self.par[2] > 127:
                    self.par[2] -= 256
                # 4 reserved/com interface  4*uint 8; must be empty according to 4.3
                self.par.append(binst[13:17].decode("ascii", "ignore"))
            else:  # Response
                # status uint 8
                self.par.append(int(binst[4]))
        elif self.dltcommand == SET_TRACESTATUS:
            if mtin == 1:  # Request
                # 1: applicationid 4*uint 8
                self.par.append(binst[4:8].decode("ascii", "ignore"))
                # 2: contextidid 4*uint 8
                self.par.append(binst[8:12].decode("ascii", "ignore"))
                # 3 newTraceStatus sint 8
                self.par.append(int(binst[12]))
                if self.par[2] > 127:
                    self.par[2] -= 256
                # 4 reserved/com interface  4*uint 8; must be empty according to 4.3
                self.par.append(binst[13:17].decode("ascii", "ignore"))
            else:  # response
                # status uint 8
                self.par.append(int(binst[4]))
        elif self.dltcommand == GET_LOGINFO:
            if mtin == 1:  # Request
                # 1: options uint 8
                self.par.append(int(binst[4]))
                # 1: applicationid 4*uint 8
                self.par.append(binst[5:9].decode("ascii", "ignore"))
                # 2: contextidid 4*uint 8
                self.par.append(binst[9:13].decode("ascii", "ignore"))
                # 4: reserved 4*uint8/com interface
                self.par.append(binst[13:17].decode("ascii", "ignore"))
            else:
                # 1 status uint8
                self.par.append(int(binst[4]))
                # 2 application IDs
                self.par.append(LogInfoType(binst[5:-4], self.par[0], endian))
                # self.par.append(binst[5:-4])  # .hex()?
                # 4 reserved/com interface  4*uint 8; must be empty according to 4.3
                self.par.append(binst[-4:].decode("ascii", "ignore"))
        elif self.dltcommand == SET_VERBOSEMODE:
            if mtin == 1:
                self.par.append(int(binst[4]))
            else:
                self.par.append(int(binst[4]))
        elif self.dltcommand == GET_DEFAULTLOGLEVEL:
            if mtin == 1:  # Request
                pass  # no parameter
            else:
                # status uint8
                self.par.append(int(binst[4]))
                # loglevel uint8
                self.par.append(int(binst[4]))
        elif self.dltcommand == STORE_CONFIGURATION:
            if mtin == 1:  # Request
                pass  # no parameter
            else:
                # 1 status uint8
                self.par.append(int(binst[4]))
        elif self.dltcommand == RESET_TOFACTORYDEFAULT:
            if mtin == 1:  # Request
                pass  # no parameter
            else:
                # 1 status uint8
                self.par.append(int(binst[4]))
        elif self.dltcommand == SET_COMINTERFACESTATUS:
            if mtin == 1:
                # 1: com interface
                self.par.append(binst[4:8].decode("ascii", "ignore"))
                self.par.append(int(binst[8]))
            else:
                # 1 status uint8
                self.par.append(int(binst[4]))
        elif self.dltcommand == SET_COMINTERFACEMAXBANDWIDTH:
            if mtin == 1:
                # 1: com interface
                self.par.append(binst[4:8].decode("ascii", "ignore"))
                self.par.append(int.from_bytes(binst[8:12], endian, signed=False))
            else:
                self.par.append(int(binst[4]))
        elif self.dltcommand == SET_MESSAGEFILTERING:
            if mtin == 1:
                self.par.append(int(binst[4]))
            else:
                # 1 status uint8
                self.par.append(int(binst[4]))
        elif self.dltcommand == SET_TIMINGPACKETS:
            if mtin == 1:
                self.par.append(int(binst[4]))
            else:
                # 1 status uint8
                self.par.append(int(binst[4]))
        elif self.dltcommand == GET_LOCALTIME:
            if mtin == 1:
                pass
            else:
                # 1 status uint8
                self.par.append(int(binst[4]))
        elif self.dltcommand == SET_USEECUID:
            if mtin == 1:
                self.par.append(int(binst[4]))
            else:
                # 1 status uint8
                self.par.append(int(binst[4]))
        elif self.dltcommand == SET_USESESSIONID:
            if mtin == 1:
                self.par.append(int(binst[4]))
            else:
                # 1 status uint8
                self.par.append(int(binst[4]))
        elif self.dltcommand == USE_TIMESTAMP:
            if mtin == 1:
                pass
            else:
                self.par.append(int(binst[4]))
                self.par.append(int(binst[5]))

        elif self.dltcommand == SET_DEFAULTLOGLEVEL:
            if mtin == 1:  # Request
                self.par.append(int(binst[4]))
                # 4 weitere Bytes sollen laut standard 4.3 ignoriert werden, laut standard 4.0 ist das jedoch
                # 4 more bytes are supposed to be ignored according to standard 4.3, but according to standard 4.0 this is
                # com_inferface
                # self.par.append(int.from_bytes(binst[5:9], endian, signed=False))
                self.par.append(binst[5:9].decode("ascii", "ignore"))
            else:  # Response
                self.par.append(int(binst[4]))
        elif self.dltcommand == SET_DEFAULTTRACESTATUS:
            if mtin == 1:  # Request
                self.par.append(int(binst[4]))
                # 4 weitere Bytes sind werden ignoriert und müssen leer sein standarf 4.0
                # additional bytes are ignored and must be blank standarf 4.0
                # self.par.append(int.from_bytes(binst[5:9], endian, signed=False))
                self.par.append(binst[5:9].decode("ascii", "ignore"))
            else:
                self.par.append(int(binst[4]))
        elif self.dltcommand == GET_SOFTWAREVERSION:
            if mtin == 1:  # Request
                # keine parameter
                pass
            else:  # response
                self.par.append(int(binst[4]))
                # länge wird ignoriert, da einfach bis zum Ende des bin Strings durchgelesen wird.
                # length is ignored because it simply reads through to the end of the bin string.
                self.par.append(int.from_bytes(binst[5:9], endian, signed=False))
                # until string end instead of 9+self.par[1]
                self.par.append(binst[9:].decode("ascii", "ignore"))
        elif self.dltcommand == MESSAGE_BUFFEROVERFLOW:
            if mtin == 1:  # Request
                # not provided for
                pass
            else:
                self.par.append(int(binst[4]))
                self.par.append(int(binst[5]))
        elif self.dltcommand == GET_DEFAULT_TRACESTATUS:
            if mtin == 1:  # Request
                pass
            else:  # response
                self.par.append(int(binst[4]))
                self.par.append(int(binst[5]))
        elif self.dltcommand == GET_COMINTERFACESTATUS:
            if mtin == 1:  # Request
                self.par.append(binst[4:8].decode("ascii", "ignore"))
            else:  # response
                self.par.append(int(binst[4]))
                self.par.append(int(binst[5]))
        elif self.dltcommand == GET_LOGCHANNELNAMES:
            if mtin == 1:  # Request
                # keine parameter
                # No parameters
                pass
            else:  # response
                self.par.append(int(binst[4]))
                self.par.append(int(binst[5]))
                # Liste aller log channel names mit jeweils 4 bytes
                # List of all log channel names with 4 bytes each
                self.par.append(binst[6:].decode("ascii", "ignore"))
        elif self.dltcommand == GET_COMINTERFACEMAXBANDWIDTH:
            if mtin == 1:  # Request
                self.par.append(binst[4:8].decode("ascii", "ignore"))
            else:  # response
                self.par.append(int(binst[4]))
                self.par.append(int.from_bytes(binst[5:9], endian, signed=False))
        elif self.dltcommand == GET_VERBOSEMODESTATUS:
            if mtin == 1:  # Request
                #  No parameters
                pass
            else:
                self.par.append(int(binst[4]))
                self.par.append(int(binst[5]))
        elif self.dltcommand == GET_TRACESTATUS:
            if mtin == 1:  # Request
                # 1: applicationid 4*uint 8
                self.par.append(binst[4:8].decode("ascii", "ignore"))
                # 2: contextidid 4*uint 8
                self.par.append(binst[8:12].decode("ascii", "ignore"))
            else:  # response
                self.par.append(int(binst[4]))
                if self.par[0] == 0:
                    self.par.append(int(binst[5]))
        elif self.dltcommand == SET_LOGCHANNELASSIGNMENT:
            if mtin == 1:  # Request
                # 1: applicationid 4*uint 8
                self.par.append(binst[4:8].decode("ascii", "ignore"))
                # 2: contextidid 4*uint 8
                self.par.append(binst[8:12].decode("ascii", "ignore"))
                self.par.append(binst[12:16].decode("ascii", "ignore"))
                self.par.append(int(binst[16]))
            else:  # response
                self.par.append(int(binst[4]))
        elif self.dltcommand == SET_LOGCHANNELTHRESHOLD:
            if mtin == 1:  # Request
                # 1: logchannelname 4*uint 8
                self.par.append(binst[4:8].decode("ascii", "ignore"))
                self.par.append(int(binst[8]))
                self.par.append(int(binst[9]))
            else:  # response
                self.par.append(int(binst[4]))
                self.par.append(int(binst[5]))
        elif self.dltcommand == GET_LOGCHANNELTHRESHOLD:
            if mtin == 1:  # Request
                # 1: logchannelname 4*uint 8
                self.par.append(binst[4:8].decode("ascii", "ignore"))
            else:
                self.par.append(int(binst[4]))
                self.par.append(int(binst[5]))
                self.par.append(int(binst[6]))
        elif self.dltcommand == BUFFER_OVERFLOWNOTIFICATION:
            if mtin == 1:
                pass
            else:
                self.par.append(int(binst[4]))
                # overflow counter uint 32
                self.par.append(int.from_bytes(binst[5:9], endian, signed=False))
        else:  # Control messages of DLT 4.0 that have not yet been implemented
            if len(binst) > 4:
                self.par.append(binst[4:])
            else:
                self.par.append("")
        # die DLT 4.0 commands müssen noch implementiert werden
        # the DLT 4.0 commands have yet to be implemented

    def gettext(self):
        """returns the payload of the control message as string"""
        textlist = self.gettextlist()
        text = ""
        for i in range(0, len(textlist)):
            text += textlist[i] + ";"
        return text

    def gettextlist(self):
        """converts the variables into a textlist
        textlist is maximum size 4
        """

        if self.dltcommand == 3842:  # from reverse engineering
            textlist = ["[connection_info]", self.statusstring(self.par[0]), str(self.par[1])]
        else:
            textlist = ["[" + DLTCOMMAND[self.dltcommand] + "] "]

        if self.dltcommand == 0:  # Bei Fehler
            textlist.append(str(self.par[0]))
        elif self.dltcommand == SET_LOGLEVEL:
            if self.mtin == 1:  # Request
                textlist.append("ApplicationID: " + self.par[0])
                textlist.append("ContextID: " + self.par[1])
                textlist.append("newLogLevel: " + str(self.par[2]))
                # com interface is only Autosar 4.0 but in 4.3 it's only empty space
                textlist.append("com_interface: " + self.par[3])
            else:  # Response
                textlist.append(self.statusstring(self.par[0]))
        elif self.dltcommand == SET_TRACESTATUS:
            if self.mtin == 1:  # Request
                textlist.append("ApplicationID: " + self.par[0])
                textlist.append("ContextID: " + self.par[1])
                textlist.append("newTraceStatus: " + str(self.par[2]))
                # com interface
                textlist.append("com_interface: " + self.par[3])
            else:  # Response
                textlist.append(self.statusstring(self.par[0]))
        elif self.dltcommand == GET_LOGINFO:
            if self.mtin == 1:  # Request
                textlist.append("Options: " + str(self.par[0]))
                textlist.append("ApplicationID: " + self.par[1])
                textlist.append("ContextID: " + self.par[2])
                textlist.append("com_interface: " + self.par[3])
            else:
                # at getLoginfo status 1-9 is possible
                textlist.append("Status: " + str(self.par[0]))
                # par[1] is an Object of the class LogInfoType
                textlist.append(self.par[1].tostring(self.par[0]))
                textlist.append("com_interface: " + self.par[2])
        elif self.dltcommand == SET_VERBOSEMODE:
            if self.mtin == 1:
                textlist.append("newStatus: " + str(self.par[0]))
            else:
                textlist.append(self.statusstring(self.par[0]))
        elif self.dltcommand == GET_DEFAULTLOGLEVEL:
            if self.mtin == 1:  # Request
                pass  # no parameter
            elif self.mtin == 2:  # Response
                textlist.append(self.statusstring(self.par[0]))
                textlist.append("LogLevel: " + str(self.par[1]))
        elif self.dltcommand == STORE_CONFIGURATION:
            if self.mtin == 1:  # Request
                pass  # no parameter
            elif self.mtin == 2:  # Response
                textlist.append(self.statusstring(self.par[0]))
        elif self.dltcommand == RESET_TOFACTORYDEFAULT:
            if self.mtin == 1:  # Request
                pass  # no parameter
            elif self.mtin == 2:  # Response
                textlist.append(self.statusstring(self.par[0]))
        elif self.dltcommand == SET_COMINTERFACESTATUS:
            if self.mtin == 1:
                textlist.append("com_interface: " + self.par[0])
                textlist.append("newStatus: " + str(self.par[1]))
            else:
                textlist.append(self.statusstring(self.par[0]))
        elif self.dltcommand == SET_MESSAGEFILTERING:
            if self.mtin == 1:  # Request
                textlist.append("newStatus: " + str(self.par[0]))
            elif self.mtin == 2:  # Response
                textlist.append(self.statusstring(self.par[0]))
        elif self.dltcommand == SET_TIMINGPACKETS:
            if self.mtin == 1:  # Request
                textlist.append("newStatus: " + str(self.par[0]))
            elif self.mtin == 2:  # Response
                textlist.append(self.statusstring(self.par[0]))
        elif self.dltcommand == GET_LOCALTIME:
            if self.mtin == 1:  # Request
                pass  # No additional parameters
            elif self.mtin == 2:  # Response
                textlist.append(self.statusstring(self.par[0]))
        elif self.dltcommand == SET_USEECUID:
            if self.mtin == 1:
                textlist.append("newStatus: " + str(self.par[0]))
            else:
                # 1 status uint8
                textlist.append(self.statusstring(self.par[0]))
        elif self.dltcommand == SET_USESESSIONID:
            if self.mtin == 1:
                textlist.append("newStatus: " + str(self.par[0]))
            else:
                # 1 status uint8
                textlist.append(self.statusstring(self.par[0]))
        elif self.dltcommand == USE_TIMESTAMP:
            if self.mtin == 1:
                textlist.append("newStatus: " + str(self.par[0]))
            else:
                # 1 status uint8
                textlist.append(self.statusstring(self.par[0]))
        elif self.dltcommand == SET_DEFAULTLOGLEVEL:
            if self.mtin == 1:  # Request
                textlist.append("New Log Level: " + str(self.par[0]))
                # empty; According to 4.0, the com_interface
                textlist.append("com Interface: " + self.par[1])
            else:
                textlist.append(self.statusstring(self.par[0]))
        elif self.dltcommand == SET_DEFAULTTRACESTATUS:
            if self.mtin == 1:  # Request
                textlist.append("New Trace Status: " + str(self.par[0]))
                textlist.append("com Interface: " + self.par[1])
            else:
                textlist.append(self.statusstring(self.par[0]))
        elif self.dltcommand == GET_SOFTWAREVERSION:
            if self.mtin == 1:  # Request
                pass  # No Parameters on Request
            else:  # Response
                textlist.append(self.statusstring(self.par[0]))
                # length of the string is also exported as else the number of parameters won't fit.
                textlist.append("Length: " + str(self.par[1]))
                textlist.append("swVersion: " + self.par[2])
        elif self.dltcommand == MESSAGE_BUFFEROVERFLOW:
            if self.mtin == 1:  # Request
                pass  # Does not exist
            else:
                textlist.append(self.statusstring(self.par[0]))
                textlist.append("status: " + str(self.par[1]))
        elif self.dltcommand == GET_DEFAULT_TRACESTATUS:
            if self.mtin == 1:  # Request
                pass  # No Parameters on Request
            else:  # Response
                textlist.append(self.statusstring(self.par[0]))
                textlist.append("tracestatus: " + str(self.par[1]))
        elif self.dltcommand == GET_COMINTERFACESTATUS:
            if self.mtin == 1:  # Request
                textlist.append("com_interface: " + self.par[0])
            else:  # Response
                textlist.append(self.statusstring(self.par[0]))
                textlist.append("Interface_status: " + str(self.par[1]))
        elif self.dltcommand == SET_COMINTERFACEMAXBANDWIDTH:
            if self.mtin == 1:  # Request
                textlist.append("com_interface: " + self.par[0])
                textlist.append("max_bandwidth: " + str(self.par[1]))
            else:  # Response
                textlist.append(self.statusstring(self.par[0]))
        elif self.dltcommand == GET_LOGCHANNELNAMES:
            if self.mtin == 1:  # Request
                pass  # No Parameters on Request
            else:  # Response
                textlist.append(self.statusstring(self.par[0]))
                textlist.append("CountInterfaceNames: " + str(self.par[1]))
                if len(self.par[2]) < self.par[1] * 4:
                    print("Error: Number of log channel names does not match string")
                textlist.append("Lgchannelnames: " + self.par[2])
                textlist.append(str(self.par[1]))
        elif self.dltcommand == GET_COMINTERFACEMAXBANDWIDTH:
            if self.mtin == 1:  # Request
                textlist.append("com_interface: " + self.par[0])
            else:
                textlist.append(self.statusstring(self.par[0]))
                textlist.append("max_bandwidth: " + self.par[1])
        elif self.dltcommand == GET_VERBOSEMODESTATUS:
            if self.mtin == 1:
                pass
            else:
                textlist.append(self.statusstring(self.par[0]))
                textlist.append("mode_status: " + self.par[1])
        elif self.dltcommand == GET_TRACESTATUS:
            if self.mtin == 1:  # Request
                textlist.append("ApplicationID: " + self.par[0])
                textlist.append("ContextID: " + self.par[1])
            else:
                textlist.append(self.statusstring(self.par[0]))
                if self.par[0] == 0:
                    textlist.append("traceStatus: " + str(self.par[1]))
        elif self.dltcommand == SET_LOGCHANNELASSIGNMENT:
            if self.mtin == 1:  # Request
                textlist.append("ApplicationID: " + self.par[0])
                textlist.append("ContextID: " + self.par[1])
                textlist.append("LogChannelName: " + self.par[2])
                textlist.append("addRemoveOp: " + str(self.par[3]))
            else:
                textlist.append(self.statusstring(self.par[0]))
        elif self.dltcommand == SET_LOGCHANNELTHRESHOLD:
            if self.mtin == 1:  # Request
                textlist.append("LogChannelName: " + self.par[0])
                textlist.append("logLevelThreshold: " + str(self.par[1]))
                textlist.append("traceStatus:" + str(self.par[2]))
            else:
                textlist.append(self.statusstring(self.par[0]))
                textlist.append("traceStatus:" + str(self.par[1]))
        elif self.dltcommand == GET_LOGCHANNELTHRESHOLD:
            if self.mtin == 1:
                textlist.append("LogChannelName: " + self.par[0])
            else:
                textlist.append(self.statusstring(self.par[0]))
                textlist.append("logLevelThreshold:" + str(self.par[1]))
                textlist.append("traceStatus:" + str(self.par[2]))
        elif self.dltcommand == BUFFER_OVERFLOWNOTIFICATION:
            if self.mtin == 1:
                pass
            else:
                textlist.append(self.statusstring(self.par[0]))
                textlist.append("overflowCounter:" + str(self.par[1]))
        else:  # not implemented control messages of DLT 4.0
            textlist.append(str(self.par[0]))

        return textlist

    @staticmethod
    def statusstring(a):
        if a > 2 or a < 0:
            return "Status: " + str(a)

        statusdesc = ["OK", "NOT_SUPPORTED", "ERROR"]

        return "Status: " + statusdesc[a]


class LogInfoType:
    """according to spec of Autosar 4.0 as the structure is not completely defined in 4.3"""

    def __init__(self, binst, options, endian):
        self.count_appids = int.from_bytes(binst[0:2], endian, signed=False)
        pos = 2
        self.app_ids = []
        for i in range(0, self.count_appids):
            self.app_ids.append(AppIDType(binst[pos:], options, endian))
            pos += self.app_ids[i].size

    def tostring(self, options):
        text = "Application IDs: "

        for i in range(0, self.count_appids):
            text += str(i) + self.app_ids[i].tostring(options)
        return text


class AppIDType:
    """only used inside of LogInfoType"""

    def __init__(self, binst, options, endian):
        self.app_id = binst[0:4].decode("ascii", "ignore")
        self.count_contextids = int.from_bytes(binst[4:6], endian, signed=False)
        self.size = 6
        self.context_id_info = []

        for i in range(0, self.count_contextids):
            self.context_id_info.append(ContextIDsInfoType(binst[self.size:], options, endian))
            self.size += self.context_id_info[i].size

        if options == 7:
            self.len_app_description = int.from_bytes(binst[self.size:self.size + 2], endian, signed=False)
            self.size += 2
            self.app_description = binst[self.size:self.size + self.len_app_description].decode("ascii", "ignore")
            self.size += self.len_app_description

    def tostring(self, options):
        text = "(AppId: " + self.app_id
        for i in range(0, self.count_contextids):
            text += str(i) + self.context_id_info[i].tostring(options)

        if options == 7:
            text += "App-Description: " + self.app_description

        text += ")"
        return text


class ContextIDsInfoType:
    """only used inside of AppIDType"""
    def __init__(self, binst, options, endian):
        self.context_id = binst[0:4].decode("ascii", "ignore")

        # size of the object
        self.size = 4

        if options == 4 or options == 6 or options == 7:
            self.loglevel = int(binst[4])
            if self.loglevel > 127:
                self.loglevel -= 256
            self.size += 1
        if options == 5:
            self.tracestatus = int(binst[4])
            self.size += 1
            if self.tracestatus > 127:
                self.tracestatus -= 256

        elif options == 6 or options == 7:
            self.tracestatus = int(binst[5])
            self.size += 1
            if self.tracestatus > 127:
                self.tracestatus -= 256
        if options == 7:
            self.lencontext_description = int.from_bytes(binst[6:8], endian, signed=False)
            self.context_description = binst[8:8 + self.lencontext_description].decode("ascii", "ignore")
            self.size += 2 + self.lencontext_description

    def tostring(self, options):
        text = "(ContextId: " + self.context_id

        if options == 4 or options == 6 or options == 7:
            text += "; Loglevel: " + str(self.loglevel)
        if options == 5 or options == 6 or options == 7:
            text += "; TraceStatus: " + str(self.tracestatus)
        if options == 7:
            text += "; Description: " + self.context_description

        text += ")"
        return text
