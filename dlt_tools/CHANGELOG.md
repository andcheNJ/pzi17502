# Changelog

## 0.1 - 2020-01-24
- First Version for new repository

## 0.2 - 2020-01-24
- First release with all intended features including commander and sniffer

## 0.3 - 2020-02-03
- New Class dlt_Connector which also implements threading
- both logreciever and command Tools are using this new class
- old dlt_commander got removed
- Default IP
- executable files are now in main directory

## 0.4 - 2020-02-04
- Filtering added
- reworking, how commands interact with the Connector
- several new 4.0 commands
- dlt payload now also includes the header and was renamed to message

## 0.5 2020-02-06
- buffer in Dlt_Connector added
- Pressing the Key Enter interrupts logreciever
- logreciever can now also filter ecuid and ctid
- some more Autosar 4.0 commands were added

## 0.6 2020-02-14
- comments, variable names and messages in english
- the log payload has it's own class now

## 0.7 2020-03-10
-reworked exporting
-sniffer and pcap reader read from all IPs