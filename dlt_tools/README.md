# DLT Tools

Management of Autosar Diagnostic Log and Trace Messages

by Friedrich Zimmer of ARRK Engineering Division
Project started in November 2019

According to Diagnostic, Log and Trace Protocol Specification 1.0.0 from 2016-11-30 ( DLT 4.3)
Some Control Messages of DLT 4.0 that are deprecated in 4.3 are still readable

Contains the following tools:
## dlt_filrereader:
Reads .dlt files and can show them on the screen or convert them to .csv

Arguments:

"source", type=str, help="Datei zum auslesen":
Mandatory, as this is the file you want to read from

"-a", "-amount", type=int, help="Anzahl der Auslesevorgänge", default=0:
optional, if you want to read until a certain amount of rows has been read. 0 means, the program will read until the 
end of the file

"-s", "-screen", help="Show Messages on Screen", action="store_true":
optional, if you want to show the messages directly on the screen

"-c", "-csv", type=str, help="Export to a csv-file. Needs the filename":
optional if you want to store the messages in a csv file. you need to tell the new filename

"-fecuid", type=str, help="Filters only a single ECU ID", default=None:
optional if you only want to see the messages from a certain ECU ID

"-fapid", type=str, help="Filters only a single AppID", default=None:
optional if you only want to see the messages from a certain Application ID

"-fctid", type=str, help="Filters only a single ContextID", default=None:
optional if you only want to see the messages from a certain Context ID

Example:

python dlt_filereader.py C:\Users\zimmerf\PycharmProjects\DLT_Tools\examples\dlt_trace.dlt -s -c C:\Temp\test99 -a 10000

This reads the file dlt_trace.dlt and shows it on the screen exports it to csv file C:\Temp\test99.csv up to 10000 rows

## dlt_pcapreader:
Reads pcap files (for example from wireshark), filters out the dlt packets and can show them on the 
screen or convert them to .dlt and .csv

Arguments:
for -a, -s and -c see above

"-ip", type=str, help="IP adress", default=DEFAULT_IP:
optional if you want to see only the messages from and to a certain IP. Otherwise it will read all IPs (port filter 3470 is always in effect to determine dlt)

"-d", "-dlt", type=str, help="Export to a dlt-file. Needs the filename":
optional argument if you want to store the messages in a dlt file. You need to tell the new filename.
Please notice that the messages from all ecus are written into the same .dlt file

"-all" this separates the dlts into separate files. Only for sniffer and pcapreader.

Example:

python dlt_pcapreader.py C:\temp\test3.pcapng -ip 169.254.199.42 -s -d C:\temp\test4.dlt
python dlt_pcapreader.py D:\ENS_Stresstests\KW32.5\pcap_traces_dlt\0251_2021-08-14_08-28-43.pcap -d D:\ENS_Stresstests\KW32.5\0251_2021-08-14_08-28-43 -all

This reads the pcap file test3.pcapng and shows all DLT Pakets sent to and from IP 169.254.199.42 and shows up to 100000 
rows on the screen and also stores them in test4.dlt

## dlt_sniffer:
Reads dlt packets from network stream, filters out the DLT Messages and shows them on the screen exports them as .dlt or .csv
Please notice, that this doesn't run smoothly because of occasional packet losses

Same Arguments like pcapreader

Examples:

python dlt_sniffer.py -s -a 100
python dlt_sniffer.py -a 100000 -d C:\Temp\DLT_Temp -all

This reads the ip stream and shows up to 100 DLT-Messages on the screen

## dlt_logreciever:
Connects to the ip and records all incoming dlt messages. This file also contains the class DltConnector, which creates 
a connector Object that can be used in other projects

Example: dlt_logreciever -s

Connects to the Default IP 169.254.199.42 and shows all messages on the screen

for the other Arguments see above
"-a", "-amount", type=int, help="Anzahl der Auslesevorgänge", default=0:
optional, if you want to read until a certain amount of rows has been read. Pressing enter also interrupts the reading

The logciever does not have the option -d all, as only the connection to a single ecu has been established.

 
## Commands
several tools that generates a certain dlt control message, sends them into the network via tcp/ip and recieves and show the reply.
Recieved Log messages or other controlmessages are ignored. For the Details what the different requests are asking, please read the specs

Example:

python dlt_getSoftwareVersion -ip 169.254.199.42 -s

This requests and shows the Software Version of the target ip

python dlt_getLogInfo.py -s -options 7

This requests the log Info from default IP (169.254.199.42) including description (=options 7) for all AppIDs and ContextIDs 