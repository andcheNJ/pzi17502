# Friedrich Zimmer
# Januar 2020
# Function for sending DLT commands
# is not yet included in 4.0

from argparse import ArgumentParser
import dlt_logger
from dltmodules import dlt_filter
from dltmodules import dlt_readcontrolpayload, dlt_createcontrolrequest
from dltmodules.dlt_export import DltExport


class DltGetTraceStatus:

    def __init__(self):
        parser = ArgumentParser()
        parser.add_argument("-ip", type=str, help="IP adress", default=dlt_logger.DEFAULT_IP)
        parser.add_argument("applicationid", type=str, help="Application ID")
        parser.add_argument("contextid", type=str, help="Context ID")
        parser.add_argument("-s", "-screen", help="Shows on screen", action="store_true")
        parser.add_argument("-c", "-csv", type=str, help="Export to a csv-file. Needs the filename")
        parser.add_argument("-d", "-dlt", type=str, help="Export to a dlt-file. Needs the filename")

        args = parser.parse_args()

        # payload = dlt_createcontrolrequest.payload_getloginfo(args.options, args.applicationid, args.contextid)
        # dlt_logreciever.DltConnector(args.ip, 2, args.s, args.c, args.d, payload)

        # Filter um nur das Kommando und die Anwort anzeigen
        # Filter to show only the command and the response
        f = dlt_filter.DltFilter(dltcommand=dlt_readcontrolpayload.GET_TRACESTATUS)
        exportoptions = DltExport(args.s, args.c, args.d, amount=2)

        # verbindung aufbauen und logging starten
        # Establish a connection and start logging
        connector = dlt_logger.DltConnector(ip=args.ip, exp=exportoptions, dltfilter=f)

        # Control message senden. Header und ExtHeader werden erst im connector hinzugefügt
        # Control message. Header and ExtHeader are only added in the connector
        payloadstring = dlt_createcontrolrequest.payload_gettracestatus(args.applicationid, args.contextid)
        connector.start_reading()
        connector.send_message(payloadstring)


# main funktionen
def main():
    DltGetTraceStatus()


if __name__ == "__main__":
    main()
