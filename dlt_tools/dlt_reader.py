""" by Friedrich Zimmer
  20.11.2019
Copyright ARRK Enineering 2019-2021
  Tool for reading .dlt files according to AUTOSAR standard
  can export to screen or into a csv file
"""

from argparse import ArgumentParser

from dltmodules import dlt_filter
from dltmodules.dlt_export import DltExport


# main funktionen
from dltmodules.dlt_filereader import DltFileReader


def main():

    """ for starting"""
    parser = ArgumentParser()
    parser.add_argument("source", type=str, help="File to read")
    parser.add_argument("-a", "-amount", type=int, help="Max Amount of Rows to read", default=0)
    parser.add_argument("-s", "-screen", help="Export to the console", action="store_true")
    parser.add_argument("-c", "-csv", type=str, help="Export to a csv-file. Needs the filename")
    parser.add_argument("-fecuid", type=str, help="Filters only a single ECU ID", default=None)
    parser.add_argument("-fapid", type=str, help="Filters only a single AppID", default=None)
    parser.add_argument("-fctid", type=str, help="Filters only a single ContextID", default=None)
    args = parser.parse_args()

    # ToDo: -c without a filename should take the filename from the dlt for the csv. Currently this only works with
    #  -c x.

    exporter = DltExport(args.source, args.s, args.c, amount=args.a)

    # amount 0 means, the tool is running until the end of the file
    # self.amount = args.a

    filter_object = dlt_filter.DltFilter(ecuid=args.fecuid, apid=args.fapid, ctid=args.fctid)

    filename = args.source

    dlt_reader_object = DltFileReader(filename, exporter, filter_object)
    dlt_reader_object.fromdltfile()
    print("DLT Filereader finished")


if __name__ == "__main__":
    main()
