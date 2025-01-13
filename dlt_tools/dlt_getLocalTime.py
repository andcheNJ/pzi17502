# Friedrich Zimmer
# Januar 2020
# Function for sending DLT commands
# Get Local Time sollte nur in 4.0 funktioniern aber nicht in 4.3

from argparse import ArgumentParser
import dlt_logger
from dltmodules import dlt_filter
from dltmodules import dlt_readcontrolpayload, dlt_createcontrolrequest
from dltmodules.dlt_export import DltExport


class DltGetLocalTime:

    def __init__(self):
        parser = ArgumentParser()
        # exclude if fixed IP
        parser.add_argument("-ip", type=str, help="IP adress", default=dlt_logger.DEFAULT_IP)
        parser.add_argument("-s", "-screen", help="Shows on screen", action="store_true")
        parser.add_argument("-c", "-csv", type=str, help="Export to a csv-file. Needs the filename")
        parser.add_argument("-d", "-dlt", type=str, help="Export to a dlt-file. Needs the filename")
        args = parser.parse_args()

        # nur das Kommando und die Anwort anzeigen#
        # show only the command and the answer
        f = dlt_filter.DltFilter(dltcommand=dlt_readcontrolpayload.GET_LOCALTIME)
        exportoptions = DltExport(args.s, args.c, args.d, amount=2)

        # verbindung aufbauen und logging starten
        # Establish a connection and start logging
        connector = dlt_logger.DltConnector(ip=args.ip, exp=exportoptions, dltfilter=f)

        # Control message senden
        messagestring = dlt_createcontrolrequest.payload_getlocaltime()
        connector.start_reading()
        connector.send_message(messagestring)


# main funktionen
def main():
    DltGetLocalTime()


if __name__ == "__main__":
    main()
