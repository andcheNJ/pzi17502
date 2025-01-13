#include "EdiabasExtended.h"

void CallEdiabasJob(const char *ecu,const char *job,const char *para,const char *result)
{
    apiJob(ecu,job,para, result);
}

APIBOOL InitEdiabas(void)
{
    return apiInit();
}

void EndEdiabas(void)
{
    apiEnd();
}
int GetEdiabasState(void)
{
    return apiState();
}

int GetEdiabasErrorCode(void)
{
    return apiErrorCode();
}

const char * GetEdiabasErrorText(void)
{
    return apiErrorText();
}


APIBOOL GetEdiabasResultReal(double * buf, const char * result, unsigned int set)
{
    return apiResultReal(buf, result, set);
}

APIBOOL GetEdiabasResultInt(short * buf, const char * result, unsigned int set)
{
    return apiResultInt(buf, result, set);
}

APIBOOL GetEdiabasResultText(char * buf, const char * result, unsigned int set, const char * format)
{
    return apiResultText(buf, result, set, format);
}

APIBOOL SetEdiabasConfig(const char *configName, const char *configValue)
{
    return apiSetConfig(configName,configValue);
}

APIBOOL GetEdiabasConfig(const char *configName, char *configValue)
{
    return apiGetConfig(configName,configValue);
}
