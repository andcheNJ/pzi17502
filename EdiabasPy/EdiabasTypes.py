from ctypes import *


class APIBool(c_int):
    APIFALSE = 0
    APITRUE = 1


class APIState(c_int):
    APIBUSY = 0
    APIREADY = 1
    APIBREAK = 2
    APIERROR = 3
