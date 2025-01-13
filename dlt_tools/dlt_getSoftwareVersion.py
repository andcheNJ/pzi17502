# Friedrich Zimmer
# Januar 2020
# Funktion zum senden von DLT Befehlen
# Function for sending DLT commands

from argparse import ArgumentParser
import dlt_logger
from dltmodules import dlt_createcontrolrequest
from dltmodules import dlt_filter
from dltmodules.connector import DltConnectorThread
from dltmodules.dlt_export import DltExport
from dltmodules.dlt_readcontrolpayload import GET_SOFTWAREVERSION


class DltGetSoftwareVersion:

    def __init__(self):
        parser = ArgumentParser()
        parser.add_argument("-ip", type=str, help="IP adress", default=dlt_logger.DEFAULT_IP)
        parser.add_argument("-s", "-screen", help="Shows on screen", action="store_true")
        parser.add_argument("-c", "-csv", type=str, help="Export to a csv-file. Needs the filename")
        parser.add_argument("-d", "-dlt", type=str, help="Export to a dlt-file. Needs the filename")
        args = parser.parse_args()

        # um nur das Kommando und die Anwort anzeigen wird Filter gesetzt
        # to show only the command and the answer, filters are set
        f = dlt_filter.DltFilter(dltcommand=GET_SOFTWAREVERSION)
        exportoptions = DltExport(args.s, args.c, args.d, amount=2)

        # verbindung aufbauen und logging starten
        # Establish a connection and start logging
        connector = DltConnectorThread(ip=args.ip, exp=exportoptions, dltfilter=f)

        # Control message wird gesendet
        # Sending Control message
        messagestring = dlt_createcontrolrequest.payload_getsoftwareversion()
        connector.start_reading()
        connector.send_message(messagestring)


# main functions
def main():
    DltGetSoftwareVersion()


if __name__ == "__main__":
    main()
