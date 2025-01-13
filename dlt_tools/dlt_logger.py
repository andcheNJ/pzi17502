""" Friedrich Zimmer
Copyright ARRK Enineering 2020-2021
function for starting a dlt connection, recieving log files and sending DLT commands
"""

from argparse import ArgumentParser
from dltmodules.dlt_export import DltExport
from dltmodules import connector
from dltmodules import dlt_filter

# IC Box über Mediagateway: 160.48.199.96
# IC Box über OBD2: 169.254.199.42
# MGU im U06 laut Ediabas: 169.254.27.154
DEFAULT_IP = "169.254.1.99"  # See from EDIABUS If using ARRK test setup


# main functions
def dlt_logreciever():
    """ for connecting to the ECU via DLT with a command line"""

    parser = ArgumentParser()
    parser.add_argument("-ip", type=str, help="IP adress", default=DEFAULT_IP)
    parser.add_argument("-a", "-amount", type=int, help="Amount of TCP Pakets to read", default=0)
    parser.add_argument("-s", "-screen", help="Shows on screen", action="store_true")
    parser.add_argument("-c", "-csv", type=str, help="Export to a csv-file. Needs the filename")
    parser.add_argument("-d", "-dlt", type=str, help="Export to a dlt-file. Needs the filename")
    parser.add_argument("-fecuid", type=str, help="Filters only a single ECU ID", default=None)
    parser.add_argument("-fapid", type=str, help="Filters only a single AppID", default=None)
    parser.add_argument("-fctid", type=str, help="Filters only a single ContextID", default=None)
    args = parser.parse_args()

    filteroptions = dlt_filter.DltFilter(ecuid=args.fecuid, apid=args.fapid, ctid=args.fctid)
    exportoptions = DltExport(None, args.s, args.c, args.d, amount=args.a)

    c = connector.DltConnectorThread(ip=args.ip, exp=exportoptions, dltfilter=filteroptions, buffering=False)
    c.start_reading()

    print("Press enter to stop reading")
    input()
    c.stop_reading()


# execute only if this file has been directly started by python
if __name__ == "__main__":
    dlt_logreciever()
