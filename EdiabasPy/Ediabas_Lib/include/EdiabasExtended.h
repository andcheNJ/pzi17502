#ifndef EDIABASEXTENDED_HPP
#define EDIABASEXTENDED_HPP

#include <Api.h>
#include <EdiabasSharedDef.h>

#ifdef __cplusplus
extern "C"
{
#endif

EDIABAS_EXPORT void CallEdiabasJob(const char *ecu,const char *job,const char *para,const char *result);
EDIABAS_EXPORT APIBOOL InitEdiabas(void);
EDIABAS_EXPORT void EndEdiabas(void);
EDIABAS_EXPORT int GetEdiabasState(void);
EDIABAS_EXPORT int GetEdiabasErrorCode(void);
EDIABAS_EXPORT const char * GetEdiabasErrorText(void);
EDIABAS_EXPORT APIBOOL GetEdiabasResultReal(double * buf, const char * result, unsigned int set);
EDIABAS_EXPORT APIBOOL GetEdiabasResultInt(short * buf, const char * result, unsigned int set);
EDIABAS_EXPORT APIBOOL GetEdiabasResultText(char * buf, const char * result, unsigned int set, const char * format);
EDIABAS_EXPORT APIBOOL SetEdiabasConfig(const char *configName, const char *configValue);
EDIABAS_EXPORT APIBOOL GetEdiabasConfig(const char *configName, char *configValue);


#ifdef __cplusplus
}
#endif
#endif // EDIABASEXTENDED_HPP
