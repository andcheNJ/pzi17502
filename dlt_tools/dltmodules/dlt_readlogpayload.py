""" class for reading the dlt payload in verbose and non verbose mode
creating log payloads is only done on ecu. So its not implemented in ARRK DLT-Tools
by Friedrich Zimmer
Copyright ARRK Enineering 2019-2021
"""


class DltReadVerbose:

    def __init__(self, binst, endian, noar, header):
        """interpreting the dlt payload of verbose dlt messages
            Args:
                binst(bytearray): the remaining binary string from the message
                endian(str): Endian for reading int
                noar(int): number of arguments
        """

        self._endian = endian

        # size of these lists is according to number of arguments (noar)
        self.typeinfo = []  # 4 Byte header of the argument
        self.variable = []  # Variable name and unit as string. remains "" if there is no variable
        self.argument = []  # Arguments Data as String
        i = 0
        pos = 0
        self.error = False

        # self.text = "
        while i < noar:
            # In current version, every argument is saved as a string
            # Log Payload always starts with 4 Byte Type Info.
            # This is need to translate all following data into it's arguments

            # Adding one typeinfo, variable datapayload per argument
            self.typeinfo.append(binst[pos:pos + 4])
            self.variable.append("")
            self.argument.append("")

            if pos > len(binst) - 4:
                print("Error: Size of payload is bigger the the remaining bin string")
                self.argument[0] = "Error: Size of payload is bigger the the remaining bin string"
                # self.eh.noar = 1
                self.error = True
                break

            # typlänge wird nur bei bool sint, uint und float benötigt und bezeichnet die Byteanzahl
            # type length is only needed for bool sint, uint, and float and denotes the number of bytes
            self.__tyle = int(self.typeinfo[i][0] & 0b00001111)

            # calculating the bits as bool variables
            tbool = bool(self.typeinfo[i][0] & 0b00010000)
            tsint = bool(self.typeinfo[i][0] & 0b00100000)
            tuint = bool(self.typeinfo[i][0] & 0b01000000)
            tfloa = bool(self.typeinfo[i][0] & 0b10000000)
            taray = bool(self.typeinfo[i][1] & 0b00000001)
            tstrg = bool(self.typeinfo[i][1] & 0b00000010)
            trawd = bool(self.typeinfo[i][1] & 0b00000100)
            tvari = bool(self.typeinfo[i][1] & 0b00001000)
            tfixp = bool(self.typeinfo[i][1] & 0b00010000)
            ttrai = bool(self.typeinfo[i][1] & 0b00100000)
            tstru = bool(self.typeinfo[i][1] & 0b01000000)
            tscod = bool(self.typeinfo[i][1] & 0b10000000)
            pos += 4

            if self.__tyle > 5 or self.__tyle < 0 or (self.__tyle == 0 and (tsint or tuint or tfloa)):
                self.argument[0] = "Error: Typelength " + str(
                    self.__tyle) + "is invalid. Must be between 1(=8bit) and 5(=128bit)"
                print(self.argument[0])
                # self.eh.noar = 1
                self.error = True
                break

            # Bei array kommen die dimensionen vor vari/fixedpoint
            # In the case of array, the dimensions come before vari/fixedpoint
            if taray:
                numdim = int.from_bytes(binst[pos:pos + 2], endian, signed=False)
                pos += 2
                if numdim > 2:
                    self.argument[i] += "ARRK DLT Tools Info: n>2-dimensional ARRAY is not supported"
                    continue
                entriesdimension = []
                for j in range(0, numdim):
                    entriesdimension.append(int.from_bytes(binst[pos:pos + 2], endian, signed=False))
                    pos += 2
            else:
                numdim = 0
                entriesdimension = 0

            # variable ist optional bei allen Daten ausser Trace
            # variable is optional for all data except trace

            if tvari:
                if not ttrai:
                    # Länge des Variablenamens
                    # Variable Name Length
                    lname = int.from_bytes(binst[pos:pos + 2], endian)
                    pos += 2
                    # Bei sint und uint wird auch immer die Einheit mit angegeben
                    # In the case of sint and uint, the unit is always included
                    lunit = 0
                    if tsint or tuint:
                        # Länge des Einheitennamens
                        # Length of unit name
                        lunit = int.from_bytes(binst[pos:pos + 2], endian)
                        pos += 2
                        # name der Einheit
                        # Name of the unit
                        unit = binst[pos + lname:pos + lname + lunit].decode("ascii", "ignore") + ": "
                        self.variable[i] += unit
                    # Name als String (laut spec immer asdii)
                    # Name as string (according to spec always asdii)
                    name = binst[pos:pos + lname].decode("ascii", "ignore") + ": "
                    self.variable[i] += name + "= "
                    # print("Variablenname:" + name)
                    pos += lname + lunit

            # wird nur optional bei sint, uint und array verwendet
            # Used only optionally with Sint, UINT and Array
            if tfixp:
                self.quantization = bytetofloat(binst[pos:pos + 4])  # not yet tested, as there is no test data
                # print("Quant:" + str(self.quantization))
                pos += 4
                if self.__tyle == 1 or self.__tyle == 2 or self.__tyle == 3:
                    self.offset = int.from_bytes(binst[pos:pos + 4], "little", signed=True)
                    pos += 4
                elif self.__tyle == 4:
                    self.offset = int.from_bytes(binst[pos:pos + 8], "little", signed=True)
                    pos += 8
                elif self.__tyle == 5:
                    self.offset = int.from_bytes(binst[pos:pos + 8], "little", signed=True)
                    pos += 16
                else:
                    print("Error in packet " + str(header.ecuid) + " " + str(header.seid) +
                          ": If fixed point, type length is required")
            else:
                self.quantization = 1
                self.offset = 0

            self.__tyle = 2 ** (self.__tyle - 1)  # Type length in bytes

            # actually the string code (scod) also includes the firt two bits of Byte 2
            # in current autosar version not needed, yet because 0x02 - 0x07 reserved for future use
            # see (SRS_Dlt_00044, SRS_Dlt_00025)

            # tscod is only used as mandatory information with string and trace
            if tscod:
                stringcode = "utf_8"
            else:
                stringcode = "ascii"

            if pos >= len(binst):
                self.error = True
                print("Error in packet " + str(header.ecuid) + " " + str(header.seid) +
                      ": Position greater than binary string length")
                break

            if tbool:
                pos += self._tbool_calc(i, binst[pos])
            elif tsint:
                pos += self._tsint_calc(i, binst[pos:pos + self.__tyle])
            elif tuint:
                pos += self._tuint_calc(i, binst[pos:pos + self.__tyle])
            elif tfloa:
                pos += self._tfloa_calc(i, binst[pos:pos + self.__tyle])
            elif tstrg:
                # Stringlänge nochmal extra als 16 bit integer
                # String length extra as 16 bit integer
                strglen = int.from_bytes(binst[pos:pos + 2], self._endian)
                pos = pos + 2
                arg = binst[pos:pos + strglen].decode(stringcode, "ignore")
                # Remove line break
                arg = arg.replace("\n", " ")
                self.argument[i] += arg
                pos += strglen
            elif taray:
                # tyle = 2 ** (self.tyle - 1)  # Type length in bytes
                # Import data:
                if tbool:
                    for j in range(0, int(entriesdimension[0])):
                        if numdim == 1:
                            pos += self._tbool_calc(i, binst[pos])
                        else:
                            for k in range(0, int(entriesdimension[1])):
                                pos += self._tbool_calc(i, binst[pos])
                elif tsint:
                    for j in range(0, int(entriesdimension[0])):
                        if numdim == 1:
                            pos += self._tsint_calc(i, binst[pos:pos + self.__tyle])
                        else:
                            for k in range(0, int(entriesdimension[1])):
                                pos += self._tsint_calc(i, binst[pos:pos + self.__tyle])
                elif tuint:
                    for j in range(0, int(entriesdimension[0])):
                        if numdim == 1:
                            pos += self._tuint_calc(i, binst[pos:pos + self.__tyle])
                        else:
                            for k in range(0, int(entriesdimension[1])):
                                pos += self._tuint_calc(i, binst[pos:pos + self.__tyle])
                elif tfloa:
                    for j in range(0, int(entriesdimension[0])):
                        if numdim == 1:
                            pos += self._tfloa_calc(i, binst[pos:pos + self.__tyle])
                        else:
                            for k in range(0, int(entriesdimension[1])):
                                pos += self._tfloa_calc(i, binst[pos:pos + self.__tyle])
            elif tstru:
                # ToDo: implement structure files.
                # showing as binary not possible because length is not known
                self.argument[i] += "ARRK DLT-Tools Info: STRUCTURE is not supported by DLT_Tools"
            elif trawd:
                # print("Raw Data")
                strglen = int.from_bytes(binst[pos:pos + 2], self._endian, signed=False)
                pos = pos + 2
                arg = binst[pos:pos + strglen]
                self.argument[i] += str(arg)
                pos += strglen
            elif ttrai:
                # print("Trace")
                strglen = int.from_bytes(binst[pos:pos + 2], self._endian, signed=False)
                pos = pos + 2
                arg = binst[pos:pos + strglen]
                self.argument[i] += str(arg)
                pos += strglen
            else:
                print("Error in packet " + str(header.ecuid) + " " + str(header.seid)
                      + ": No Data Type in Payload")
            i += 1

    def _tbool_calc(self, i, binst):
        if self.__tyle != 1:
            print("Warning: Type Length at bool must be 1. Current Type length: " + str(self.__tyle))
        self.argument[i] += str(bool(binst))
        return 1

    def _tsint_calc(self, i, binst):
        phy_v = int.from_bytes(binst, self._endian, signed=True)
        log_v = phy_v * self.quantization + self.offset
        self.argument[i] += str(log_v)
        return self.__tyle

    def _tuint_calc(self, i, binst):
        phy_v = int.from_bytes(binst, self._endian, signed=False)
        log_v = phy_v * self.quantization + self.offset
        self.argument[i] += str(log_v)
        return self.__tyle

    def _tfloa_calc(self, i, binst):
        self.argument[i] += str(bytetofloat(binst))
        return self.__tyle


class DltReadNonVerbose:
    """class for log messages in non verbose mode"""

    def __init__(self, binst, endian):
        # ToDo: implement non verbose and Fibex
        self.msgid = int.from_bytes(binst[:4], endian)


def bytetofloat(binst):
    """converts byte to float"""
    int4 = int.from_bytes(binst, "little", signed=False)
    sign = (1, -1)[int4 >> 31 & 1]  # edit: & 1 added
    exp = int4 >> 23 & 255
    if exp >= 128:
        exp = -((exp ^ 255) + 1)  # edit: -(...) added
    mant = int4 & 8388607  # 2 ** 23 - 1
    if mant == 0:
        print("Error in byte to float conversion")
        return 0.0
    float32 = sign * mant ** exp
    return float32
