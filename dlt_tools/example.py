import time

import dlt_logger
from dltmodules import dlt_filter
from dltmodules import dlt_createcontrolrequest


def example():
    # filter nur auf control messages
    # Filter only on Control Messages
    # f = dlt_filter.DltFilter(apid="PAGY")

    f = dlt_filter.DltFilter(mstp=3)

    conn = dlt_logger.DltConnector(ip="169.254.199.42", dltfilter=f, screen=True)

    conn.send_message(dlt_createcontrolrequest.payload_getsoftwareversion())
    print("Line: " + str(conn.rownumber) + " from " + str(conn.allrownumber))

    time.sleep(1)
    conn.send_message(dlt_createcontrolrequest.payload_setloglevel(applicationid="AUDP", contextid="HADT",
                                                                   newloglevel=-1))
    print("Line: " + str(conn.rownumber) + " from " + str(conn.allrownumber))

    time.sleep(1)
    conn.send_message(dlt_createcontrolrequest.payload_settracestatus(applicationid="AUDP", contextid="HADT",
                                                                      newtracestatus=-1))
    print("Line: " + str(conn.rownumber) + " from " + str(conn.allrownumber))

    time.sleep(1)
    conn.send_message(dlt_createcontrolrequest.payload_getloginfo(options=6, applicationid="AUDP", contextid="HADT"))
    print("Line: " + str(conn.rownumber) + " from " + str(conn.allrownumber))
    time.sleep(1)

    conn.stop_reading()
    print("End")


example()
