#ifndef EDIABASSHAREDDEF_HPP
#define EDIABASSHAREDDEF_HPP

#if defined(EDIABAS_DLL) && defined(_WIN32)
	#ifdef EDIABAS_DLL_EXPORT
		#define EDIABAS_EXPORT __declspec(dllexport)
	#else
		#define EDIABAS_EXPORT __declspec(dllimport)
	#endif
#else
	#define EDIABAS_EXPORT
#endif

#endif // EDIABASSHAREDDEF_HPP
