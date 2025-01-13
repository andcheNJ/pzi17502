""" Friedrich Zimmer November 2019
Copyright ARRK Enineering 2019-2021
 classes for exporting to screen, csv files or dlt files
 no executable funktions
 needed by filereader, pcapreader sniffer and logreciever
"""

from datetime import datetime
from csv import writer

from scapy.layers.inet import IP

from dltmodules import dlt_message
from dltmodules import dlt_storageheader


class DltExport:
    """ for managing the export options"""

    def __init__(self, filename=None, screen=True, csvfilename=None, dltfilename=None, amount=0, ipinfo=False, all=False):
        """
            Defining the export
            Args:
                screen(bool): if message is shown on screen
                csvfilename(str): filename for exporting to csv
                dltfilename(str): filename for exporting to dlt
                ipinfo(bool): true if also connection info like IPs are exported
                all(bool): all the dlts in a trace should be exported into different files.
                    (only for sniffing and pcap reading)
        """

        # screen kann auch nachträglich aktiviert oder deaktiviert werden.
        # screen can also be activated or deactivated later
        self.screen = screen
        # if self.screen:
        #     print("Exporting to screen")

        # dlt oder csv sollte nicht unterbrochen werden.
        # DLT or CSV should not be interrupted.
        self.__csv = DltCsvExport(filename, csvfilename, ipinfo)
        # if dltfilename == "all":
        #     self.__dlt = DltDltMultiExport()
        # else:
        self.__dlt = DltDltExport(filename, dltfilename, all)
        self.counter = 0
        self.amount = amount

    def start_export(self):
        """creating the files"""
        self.__csv.start_writing()
        # self.__dlt.start_writing()

    def export_message(self, message, storageheader=None, pkt=None):
        """ for exporting a new message/row """
        """returns True if the amount is reached"""
        if self.screen:
            screenexport(self.counter, message, pkt)
        self.__csv.write_message(self.counter, message, storageheader, pkt)
        self.__dlt.write_message(message, pkt)
        self.counter += 1

        if self.amount != 0 and self.counter >= self.amount:
            return True

        return False

    def end_export(self):
        """closing the files"""
        self.__csv.end_writing()
        self.__dlt.end_writing()

    def interpreting_needed(self):
        """returns true if interpreting of the binary string is necessary for export"""
        if self.screen or self.__csv.aktiv:
            return True
        return False


def get_protocol_from_packet(pkt):
    if "UDP" in pkt:
        return "UDP"
    elif "TCP" in pkt:
        return "TCP"
    return ""


def screenexport(i, message, pkt):
    """ prints the message directly to the screen"""

    screenstring = str(i) + " "

    if pkt is not None:
        screenstring += pkt[IP].src + " " + pkt[IP].dst + " " + get_protocol_from_packet(pkt) + " "

    screenstring += str(message.header.tmsp) + " " + \
                    message.header.ecuid + " " + \
                    str(message.ext_header.apid) + " " + \
                    message.ext_header.ctid + " " + \
                    dlt_message.MESSAGETYPE[message.ext_header.mstp] + " " + \
                    dlt_message.MESSAGETYPEINFO[message.ext_header.mstp][message.ext_header.mtin] + " " + \
                    message.gettext()

    print(screenstring)


class DltCsvExport:
    """ for exporting the data into csv files """

    def __init__(self, filename, csv_filename, ipinfo):
        if csv_filename is None:
            # No CSV Export
            self.aktiv = False
            return
        elif csv_filename == "x":
            # CSV Name aus pcap filename
            # CSV name from pcap filename
            csv_filename = filename[:filename.rfind(".p")]
            print("Exported into serval csv files")
        else:
            print("Exported into csv file: " + csv_filename)
        self.aktiv = True

        if len(csv_filename) < 4 or csv_filename[-4:] != ".csv":
            self.filename = csv_filename + ".csv"
        else:
            self.filename = csv_filename

        self.csvfile = None
        self.csvwriter = None
        self.ipinfo = ipinfo

    def start_writing(self):
        """creating the csv file and the writer object"""
        if not self.aktiv:
            return

        try:
            self.csvfile = open(self.filename, "w", newline="")
            self.csvwriter = writer(self.csvfile, delimiter=";", escapechar='_')
            # Überschrift:
            if self.ipinfo is False:
                self.csvwriter.writerow(
                    ["Index", "Time", "Timestamp", "Count", "ECU-Id", "Apid", "Ctid", "Sessionid", "Type", "Typeinfo",
                     "Mode", "#Args", "Arg1", "Arg2", "Arg3", "Arg4", "Arg5", "Arg6", "Arg7", "Arg8", "Arg9"])
            else:
                self.csvwriter.writerow(
                    ["Src-IP", "Dst-IP", "Protocol", "Index", "Time", "Timestamp", "Count", "ECU-Id", "Apid", "Ctid",
                     "Sessionid", "Type", "Typeinfo",
                     "Mode", "#Args", "Arg1", "Arg2", "Arg3", "Arg4", "Arg5", "Arg6", "Arg7", "Arg8", "Arg9"])
            print("CSV-Datei " + self.filename + " wird erstellt...")
        except FileNotFoundError:
            print("ERROR: CSV Datei konnte nicht erstellt werden.")
            self.aktiv = False

    def write_message(self, counter, message, storageheader=None, pkt=None):
        """ adding a new row to the csv file"""
        if not self.aktiv:
            return

        # Falls kein Storageheader übergeben wird, wird der aktuelle Zeitpunkt verwendet.
        # If no storage header is passed, the current time is used.
        # ToDo: Bei pcap auslesen Timestamp des Frames verwenden.
        if storageheader:
            timestring = storageheader.timestring()
        else:
            timestring = datetime.now().isoformat()

        if self.ipinfo:
            self.csvwriter.writerow([pkt[IP].src, pkt[IP].dst, get_protocol_from_packet(pkt),
                                     str(counter), timestring, str(message.header.tmsp), message.header.mcnt,
                                     message.header.ecuid,
                                     str(message.ext_header.apid), message.ext_header.ctid, message.header.seid,
                                     dlt_message.MESSAGETYPE[message.ext_header.mstp],
                                     dlt_message.MESSAGETYPEINFO[message.ext_header.mstp][message.ext_header.mtin],
                                     message.getverboseasstring(), message.ext_header.noar,
                                     message.getargtext(0), message.getargtext(1), message.getargtext(2),
                                     message.getargtext(3), message.getargtext(4), message.getargtext(5),
                                     message.getargtext(6), message.getargtext(7), message.getargtext(8)])

        else:
            self.csvwriter.writerow([str(counter), timestring, str(message.header.tmsp), message.header.mcnt,
                                     message.header.ecuid,
                                     str(message.ext_header.apid), message.ext_header.ctid, message.header.seid,
                                     dlt_message.MESSAGETYPE[message.ext_header.mstp],
                                     dlt_message.MESSAGETYPEINFO[message.ext_header.mstp][message.ext_header.mtin],
                                     message.getverboseasstring(), message.ext_header.noar,
                                     message.getargtext(0), message.getargtext(1), message.getargtext(2),
                                     message.getargtext(3), message.getargtext(4), message.getargtext(5),
                                     message.getargtext(6), message.getargtext(7), message.getargtext(8)])

    def end_writing(self):
        if self.aktiv:
            self.csvfile.close()

class DltDltExport:
    """ for exporting the data as dlt file """

    def __init__(self, filename, dlt_filename, all=False):
        """init the dlt file object and checking the filename"""

        if dlt_filename is None:
            # No DLT Export
            self.active = False
            return
        elif dlt_filename == "x":
            # DLT Name aus pcap filename
            # DLT name from pcap filename
            dlt_filename = filename[:filename.rfind(".p")]
        self.active = True
        self.export_all = all

        # Liste der Exportfiles
        # List of export files
        self.dltfile = []

        # dlt anhängen falls einzelexport und dlt nicht schon da ist.
        # Attach DLT if single export and DLT are not already there.
        if self.export_all:
            self.filename = dlt_filename
            print("The DLT data is packaged into separate files for each ECU.")
        else:
            if (len(dlt_filename) < 5 or dlt_filename[-4:] != ".dlt"):
                self.filename = dlt_filename + ".dlt"
            else:
                self.filename = dlt_filename

            print("The DLT data is packaged into a single file.")
            self.start_writing(self.filename)

    def start_writing(self, filename=None):
        """creating the dlt file"""

        if self.active is False:
            return

        try:
            new_dltfile = open(filename, "wb")
            self.dltfile.append(new_dltfile)
            print("DLT-File " + filename + " is being created....")
        except FileNotFoundError:
            new_dltfile = None
            print("ERROR: Failed to create DLT file.")
            self.active = False

        return new_dltfile

    def write_message(self, message, pkt):
        """ adding a new row """
        if self.active is False:
            return

        # Generate DLT Storage Header:
        if (pkt):
            storageheader = dlt_storageheader.DltStorageHeader(ecu=message.header.ecuid,
                                                               s=int(pkt[0].time), ms=int(str(pkt[0].time).split('.')[1]))
            dlt_file = self.get_dlt_file(pkt[IP].src)
        else:
            storageheader = dlt_storageheader.DltStorageHeader(ecu=message.header.ecuid,
                                                               s=int(datetime.now().timestamp()), ms=0)
            # ToDo: also get milliseconds
            dlt_file = self.dltfile[0]

        # print("SH:" + str(len(storageheader.binst)) + " " + str(storageheader.binst))
        # print("MH:" + str(len(message.header.binst)) + " " + str(message.header.binst))
        # print("M:" + str(len(message.binst)) + " " + str(message.binst))

        dlt_file.write(storageheader.binst + message.header.binst + message.binst)

    def end_writing(self):
        """closing the dlt file"""
        if self.active:
            for file in self.dltfile:
                file.close()

    def get_dlt_file(self, src):
        """provides the target dlt file for writing a new dlt row. If file doesn't exist it gets created"""

        if self.export_all:
            filename = self.filename + "_DLT_" + str(src) + ".dlt"
        else:
            return self.dltfile[0]

        # search if file already exists
        for file in self.dltfile:
            if filename == file.name:
                return file

        # start writing a new file
        return self.start_writing(filename)



