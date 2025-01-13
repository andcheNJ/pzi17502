"""
 by Friedrich Zimmer
Copyright ARRK Enineering 2019-2021
8.11.2019
Executable function for reading pcapng files
can export to screen, dlt files and csv files
"""

from argparse import ArgumentParser

from dltmodules.pcap_reading import DltPcapReader

from dltmodules.dlt_export import DltExport
from dltmodules.dlt_filter import DltFilter

# def main():
parser = ArgumentParser()
parser.add_argument("file", type=str, help="Filepath and name of the pcap data source")
parser.add_argument("-ip", type=str, help="IP adress send&recieve filter", default="")
parser.add_argument("-a", "-amount", type=int, help="Amount of rows to show", default=0)
parser.add_argument("-s", "-screen", help="Shows on screen", action="store_true")
parser.add_argument("-c", "-csv", type=str, help="Export to a csv-file. Requires the filename")
parser.add_argument("-d", "-dlt", type=str, help="Export to a dlt-file. Requires the filename.")
parser.add_argument("-all", help="Separates the read messages into separate files for each IP", action="store_true")
parser.add_argument("-fecuid", type=str, help="Filters only a single ECU ID", default=None)
parser.add_argument("-fapid", type=str, help="Filters only a single AppID", default=None)
parser.add_argument("-fctid", type=str, help="Filters only a single ContextID", default=None)
args = parser.parse_args()

# ToDo: -d without a filename should take the filename from the pcap for dlt. Currently this only works with -d x.
#  Same with -c

filter_options = DltFilter(ecuid=args.fecuid, apid=args.fapid, ctid=args.fctid)
export_options = DltExport(args.file, args.s, args.c, args.d, amount=args.a, ipinfo=True, all=args.all)

DltPcapReader(filename=args.file, ip=args.ip, exporter=export_options, dltfilter=filter_options)

print("DLT PCAP Reader finished")

# if __name__ == "__main__":

# main()
