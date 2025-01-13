"""
# by Friedrich Zimmer
# 8.11.2019
Copyright ARRK Enineering 2019-2021
# Executable funktion for reading the dlt messages from and to specified IP from the stream by using scapy
# inherits methods from DltListener in file pcapreader.py
"""
from argparse import ArgumentParser
from dltmodules.dlt_export import DltExport
from dltmodules.dlt_filter import DltFilter

from dltmodules.sniffer import DltSnifferThread


# DEFAULT_NETWORK = "Eth_MGW"


def main():
    """ main functions"""

    parser = ArgumentParser()

    parser.add_argument("network", type=str,help="Shows the network")
    parser.add_argument("-ip", type=str, help="IP adress", default="")
    parser.add_argument("-a", "-amount", type=int, help="Amount of rows to show", default=0)
    parser.add_argument("-s", "-screen", help="Shows on screen", action="store_true")
    parser.add_argument("-c", "-csv", type=str, help="Export to a csv-file. Requires the filename")
    parser.add_argument("-d", "-dlt", type=str, help="Export to a dlt-file. Requires the filename.")
    parser.add_argument("-all", help="Separates the read messages into separate files for each IP", action="store_true")
    parser.add_argument("-fecuid", type=str, help="Filters only a single ECU ID", default=None)
    parser.add_argument("-fapid", type=str, help="Filters only a single AppID", default=None)
    parser.add_argument("-fctid", type=str, help="Filters only a single ContextID", default=None)

    args = parser.parse_args()

    #filter and exporter objects
    filteroptions = DltFilter(ecuid=args.fecuid, apid=args.fapid, ctid=args.fctid)
    exportoptions = DltExport(None, args.s, args.c, args.d, amount=args.a, ipinfo=True, all=args.all)

    # Sniffer Objekt erstellen und Sniffen starten
    # Creating a Sniffer Thread Object
    c = DltSnifferThread(iface=args.network, ip=args.ip, exporter=exportoptions, dltfilter=filteroptions)

    c.start_sniffing()
    print("Press enter to stop reading")
    input()

    if args.a == 0:
        c.stop_sniffing()

    print("Exiting DLT Sniffer")


if __name__ == "__main__":
    main()
