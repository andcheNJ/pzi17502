from ctypes import *
import os
import sys
from Binding.EdiabasTypes import (APIBool, APIState)


class Ediabas:

    initialization_count = 0

    def __init__(self, lib_path):
        try:
            self.ediabas = windll.LoadLibrary(os.path.abspath(lib_path))
            self.__loadFunctions()
            print("Successfully loaded ediabas library!\n")
            print("--------------------------------------------------------------------------\n")
        except TypeError:
            print("Ediabas library could not be loaded from path. Make sure the correct ediabas path is set in "
                  "\"config.yml\" and check your local PC directory. Program can not be executed...\n\n")
            input("Press enter to close the terminal window")
            sys.exit("\nProgram terminated because of missing ediabas path.")

    def __loadFunctions(self):
        """
        Load functions from C++ EdiabasExtended dll
        :return: /
        """

        # c++: APIBOOL InitEdiabas()
        self.ediabas_init = self.ediabas.InitEdiabas
        self.ediabas_init.argtypes = []
        self.ediabas_init.restypes = APIBool
        # returns apiInit()

        # c++: void CallEdiabasJob(const char * ecu, const char * job, const char * para, const char * result)
        self.call_ediabas_job = self.ediabas.CallEdiabasJob
        self.call_ediabas_job.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p]
        self.call_ediabas_job.restypes = None
        # returns nothing

        # c++: void EndEdiabas()
        self.end_ediabas = self.ediabas.EndEdiabas
        self.end_ediabas.argtypes = []
        self.end_ediabas.restypes = None
        # returns nothing

        # c++: int GetEdiabasState()
        self.get_ediabas_state = self.ediabas.GetEdiabasState
        self.get_ediabas_state.argtypes = []
        self.get_ediabas_state.restypes = c_int
        # returns apiState()

        # c++: int GetEdiabasErrorCode()
        self.get_error_code = self.ediabas.GetEdiabasErrorCode
        self.get_error_code.argtypes = []
        self.get_error_code.restypes = c_int
        # returns apiErrorCode()

        # c++: const char * GetEdiabasErrorText()
        self.get_error_text = self.ediabas.GetEdiabasErrorText
        self.get_error_text.argtypes = []
        self.get_error_text.restypes = c_char_p
        # returns apiErrorText()

        # c++: APIBOOL GetEdiabasResultReal(double * buf, const char * result, unsigned int set)
        self.get_result_real = self.ediabas.GetEdiabasResultReal
        self.get_result_real.argtypes = [POINTER(c_double), c_char_p, c_uint]
        self.get_result_real.restypes = APIBool
        # returns apiResultReal(buf, result, set)

        # c++: APIBOOL GetEdiabasResultInt(short * buf, const char * result, unsigned int set)
        self.get_result_int = self.ediabas.GetEdiabasResultInt
        self.get_result_int.argtypes = [POINTER(c_short), c_char_p, c_uint]
        self.get_result_int.restypes = APIBool
        # returns apiResultInt(buf, result, set)

        # c++: APIBOOL GetEdiabasResultText(char * buf, const char * result, unsigned int set, const char * format)
        self.get_result_text = self.ediabas.GetEdiabasResultText
        self.get_result_text.argtypes = [POINTER(c_char), c_char_p, c_uint, c_char_p]
        self.get_result_text.restypes = APIBool
        # returns apiResultText(buf, result, set, format)

        # c++: APIBOOL GetEdiabasConfig(const char * configName, char * configValue)
        self.get_ediabas_config = self.ediabas.GetEdiabasConfig
        self.get_ediabas_config.argtypes = [c_char_p, c_char_p]
        self.get_ediabas_config.restypes = APIBool
        # returns apiGetConfig(configName,configValue)

        # c++: APIBOOL SetEdiabasConfig(const char * configName, const char * configValue)
        self.set_ediabas_config = self.ediabas.SetEdiabasConfig
        self.set_ediabas_config.argtypes = [c_char_p, c_char_p]
        self.set_ediabas_config.restypes = APIBool
        # returns apiSetConfig(configName,configValue)

    def initEdiabas(self):
        result = self.ediabas_init()
        if(result != APIBool.APITRUE):
            return False
        # Call status job to boost --> dummy job
        self.callEdiabasJob("BDC_G05", "status_lesen", "ARG;AUSSENSPIEGEL_POSITION", "")
        # print("getEdiabasState(): " + str(self.getEdiabasState()))   # debug
        while (self.getEdiabasState() == APIState.APIBUSY):
            self.__printInitializationProgress()
        if(self.getEdiabasState() == APIState.APIERROR):
            print("APIState.APIERROR")  # debug
            return False
        print("\nFinished Initialization!")
        return True

    def endEdiabas(self):
        self.end_ediabas()

    def callEdiabasJob(self, prg_file: str, job_name: str, parameter: str, result: str):
        # apiJob("BCP_SP21","steuern","ARG;AUSSENSPIEGEL_POSITION;LEFT_MIRROR;100;100","")
        prg_file_input = prg_file.encode('utf-8')
        job_name_input = job_name.encode('utf-8')
        parameter_input = parameter.encode('utf-8')
        result_input = result.encode('utf-8')

        self.call_ediabas_job(prg_file_input, job_name_input, parameter_input, result_input)

    def getEdiabasState(self):
        return self.get_ediabas_state()

    def getEdiabasErrorCode(self):
        return self.get_error_code()

    def getEdiabasErrorText(self):
        return self.get_error_text()

    def getEdiabasResultDouble(self, value_descriptor):
        result = c_double()
        job_feedback = self.get_result_real(byref(result), value_descriptor.encode('utf-8'), 1)
        if(job_feedback == APIBool.APITRUE):
            return result.value
        return -1

    def getEdiabasResultInt(self, value_descriptor):
        result = c_short()
        job_feedback = self.get_result_int(byref(result), value_descriptor.encode('utf-8'), 1)
        if(job_feedback == APIBool.APITRUE):
            return result.value
        return -1

    def GetECUPath(self):
        result = c_char()
        argument = "ECUPATH"
        job_feedback = self.get_ediabas_config(argument.encode('utf-8'), byref(result))

    def SetECUPath(self, ecu_path: str):
        argument = "ECUPATH"
        job_feedback = self.set_ediabas_config(argument.encode('utf-8'), ecu_path.encode('utf-8'))

    def __printInitializationProgress(self):
        self.initialization_count += 1
        output = "\rInitialization Ediabas "
        for i in range(self.initialization_count):
            output = output + "."
        sys.stdout.write(output)
        sys.stdout.flush()
    # def getEdiabasResultText(self):
    #    result = c_char()
    #    job_feedback = self.get_result_real(byref(result),)
    #    if(job_feedback == APIBool.APITRUE):
    #        return result.value
    #    return ""
