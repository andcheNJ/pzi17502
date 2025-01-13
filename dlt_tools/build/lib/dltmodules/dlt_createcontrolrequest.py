""" these functions create binary strings for sending control messages
by Friedrich Zimmer
Copyright ARRK Enineering 2019-2021
"""

import time

from dltmodules.dlt_readcontrolpayload import *


def headerstring(counter, packetlength, ecuid="", seid=0):
    """generate header for control message request
    Args:
        counter(int): message counter in the header
        ecuid(str): ID of the ECU
        seid(int): Session ID
        packetlength(int): Total packet lenght of dlt standard header and extended header
    Returns:
        header argumets"""

    # the Bits of htyp are always defined as follows:
    # Bit 0: UEH (Use Extended Header) = true
    # Bit 1: MSBF (Most Significant Byte First) = wahr; -> always big endian
    # Bit 2: WEID (With ECU ID) = true
    # Bit 3: WSID (With Session ID) = true
    # Bit 4: WTMS (With Timestamp) = true
    # Bit 5-7: VERS (Version Number) = 1
    htyp = (0b00111111).to_bytes(1, byteorder='big')
    mcnt = counter.to_bytes(1, byteorder='big')
    packet_length = packetlength.to_bytes(2, byteorder='big')
    # ecuid need to exactly length 4
    while len(ecuid) < 4:
        ecuid += " "
    ecu = ecuid.encode('ascii')
    session_id = seid.to_bytes(4, byteorder='big')
    tmsp = int(time.time()).to_bytes(4, byteorder='big')
    return htyp + mcnt + packet_length + ecu + session_id + tmsp


def sendrequest(payload, counter=0, ecuid="", seid=0, apid="APP ", ctid="CON "):
    """  combining header, extended header and payload

    Args:
        payload(bytearray) : the payload of the message that has to be send
        counter(int): message counter in the header
        ecuid(str): ID of the ECU
        seid(int): Session ID
        apid(str): Application ID of the application that sends the message
        ctid(str): Context ID

    Returns:
         the message as binary string that can be sent by TCP """

    # applicationID, contextID
    extended_header = extheader(apid, ctid)
    # ecuid und session ID can also be optional according to the standard
    header = headerstring(counter, 26 + len(payload), ecuid, seid)

    return header + extended_header + payload


def extheader(apid="    ", ctid="    "):
    """ generate ext header for control messages """
    # for htyp: mtin = Request (message Type 3; Non Verbose
    msin = (0b00010110).to_bytes(1, byteorder='big')
    # Anzahl der Argumente wird nicht benötigt
    # No number of arguments needed
    nobin = b'\x00'
    apidbin = apid.encode('ascii')
    ctidbin = ctid.encode('ascii')
    return msin + nobin + apidbin + ctidbin


# generate payloads for the various control payloads
def payload_setloglevel(applicationid, contextid, newloglevel):
    binst = SET_LOGLEVEL.to_bytes(4, byteorder='big')
    binst += applicationid.encode('ascii')
    binst += contextid.encode('ascii')
    binst += newloglevel.to_bytes(1, byteorder='big', signed=True)
    binst += b"\x00\x00\x00\x00"
    return binst


def payload_settracestatus(applicationid, contextid, newtracestatus):
    binst = SET_TRACESTATUS.to_bytes(4, byteorder='big')
    binst += applicationid.encode('ascii')
    binst += contextid.encode('ascii')
    binst += newtracestatus.to_bytes(1, byteorder='big', signed=True)
    binst += b"\x00\x00\x00\x00"
    return binst


def payload_getloginfo(options, applicationid, contextid):
    binst = GET_LOGINFO.to_bytes(4, byteorder='big')
    binst += options.to_bytes(1, byteorder='big')
    if applicationid is None:
        binst += b"\x00\x00\x00\x00"
    else:
        binst += applicationid.encode('ascii')
    if contextid is None:
        binst += b"\x00\x00\x00\x00"
    else:
        binst += contextid.encode('ascii')
    # in Version 4.0 this is the com_interface
    binst += b"\x00\x00\x00\x00"
    return binst


def payload_getdefaultloglevel():
    return GET_DEFAULTLOGLEVEL.to_bytes(4, byteorder='big')


def payload_storconfiguration():
    return STORE_CONFIGURATION.to_bytes(4, byteorder='big')


def payload_resettofactorydefault():
    return RESET_TOFACTORYDEFAULT.to_bytes(4, byteorder='big')


def payload_setmessagefiltering(newstatus):
    binst = SET_MESSAGEFILTERING.to_bytes(4, byteorder='big')
    binst += newstatus.to_bytes(1, byteorder='big')
    return binst


# nur 4.0
def payload_getlocaltime():
    binst = GET_LOCALTIME.to_bytes(4, byteorder='big')
    return binst


def payload_setdefaultloglevel(newloglevel):
    binst = SET_DEFAULTLOGLEVEL.to_bytes(4, byteorder='big')
    binst += newloglevel.to_bytes(1, byteorder='big', signed=True)
    binst += b"\x00\x00\x00\x00"
    return binst


def payload_setdefaulttracestatus(newtracestatus):
    binst = SET_DEFAULTTRACESTATUS.to_bytes(4, byteorder='big')
    binst += newtracestatus.to_bytes(1, byteorder='big', signed=True)
    binst += b"\x00\x00\x00\x00"
    return binst


def payload_getsoftwareversion():
    return GET_SOFTWAREVERSION.to_bytes(4, byteorder='big')


def payload_getdefaulttracestatus():
    return GET_DEFAULT_TRACESTATUS.to_bytes(4, byteorder='big')


def payload_getlogchannelnames():
    return GET_LOGCHANNELNAMES.to_bytes(4, byteorder='big')


def payload_gettracestatus(applicationid, contextid):
    binst = GET_TRACESTATUS.to_bytes(4, byteorder='big')
    binst += applicationid.encode('ascii')
    binst += contextid.encode('ascii')
    return binst


def payload_setlogchannelassignment(applicationid, contextid, logchannelname, addremoveop):
    binst = SET_LOGCHANNELASSIGNMENT.to_bytes(4, byteorder='big')
    binst += applicationid.encode('ascii')
    binst += contextid.encode('ascii')
    binst += logchannelname.to_bytes(4, byteorder='big')
    binst += addremoveop.to_bytes(1, byteorder='big')
    return binst


def payload_setlogchannelthreshold(logchannelname, logchannelthreshold, tracestatus):
    binst = SET_LOGCHANNELTHRESHOLD.to_bytes(4, 'big')
    binst += logchannelname.to_bytes(4, 'big')
    binst += logchannelthreshold.to_bytes(1, 'big')
    binst += tracestatus.to_bytes(1, 'big')
    return binst


def payload_getlogchannelthreshold(logchannelname):
    binst = GET_LOGCHANNELTHRESHOLD.to_bytes(4, 'big')
    binst += logchannelname.to_bytes(4, 'big')
    return binst


def payload_bufferoverflownotification():
    return BUFFER_OVERFLOWNOTIFICATION.to_bytes(4, 'big')

# ToDo: control messages for Autosar 4.0
