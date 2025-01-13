# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 15:40:00 2024

@author: testhouse
"""

from argparse import ArgumentParser
from dltmodules.pcap_reading import DltPcapReader
from dltmodules.dlt_export import DltExport
from dltmodules.dlt_filter import DltFilter

def convert_pcap_to_dlt(pcap_path, dlt_output_path):
    # Define the arguments manually
    args = {
        "file": pcap_path,
        "ip": "",
        "a": 0,
        "s": False,
        "c": None,
        "d": dlt_output_path,
        "all": False,
        "fecuid": None,
        "fapid": None,
        "fctid": None
    }

    filter_options = DltFilter(ecuid=args['fecuid'], apid=args['fapid'], ctid=args['fctid'])
    export_options = DltExport(args['file'], args['s'], args['c'], args['d'], amount=args['a'], ipinfo=True, all=args['all'])

    DltPcapReader(filename=args['file'], ip=args['ip'], exporter=export_options, dltfilter=filter_options)

    print("DLT PCAP Reader finished")

# Example usage
pcap_file_path = r"E:\DLT_Traces\IDCevo_Pcap\pcap_trace_20240620_151823.pcap"
dlt_file_path = r"E:\DLT_Traces\IDCevo_Pcap\pcap_trace_20240620_151823.dlt"
convert_pcap_to_dlt(pcap_file_path, dlt_file_path)
