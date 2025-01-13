from dltmodules import dlt_readheader, dlt_message
from dltmodules import dlt_storageheader


class DltFileReader:
    """
    For reading of dlt files created by dlt-tools or Dlt_Viewer
    See also chapter 5.4 of theDiagnostic, Log and Trace Protocol Specification
    """

    def __init__(self, filename, exporter, filter_object):
        """ initiating the reading from the command

           Args:


        """

        self.exporter = exporter

        # amount 0 means, the tool is running until the end of the file
        # self.amount = args.a

        self.filter = filter_object

        self.filename = filename

        if len(self.filename) < 5:
            print("Filename " + self.filename + " too short!")
            exit(-1)

    def fromdltfile(self):
        """ reads the messages from the .dlt file"""
        try:
            with open(self.filename, "rb") as file:
                print("Reading from file: " + str(self.filename))
                pos = 0
                fstr = file.read()

                # Start of csv export if desired
                self.exporter.start_export()
                # csvexport = dlt_export.DltCsvExport(self.csv)

                # for i in range(0, self.amount):
                while True:

                    # Checking if the file starts correctly
                    start = fstr[pos:pos + 4]
                    if start != dlt_storageheader.DLTSTORAGESTART:
                        print("Error: Data has to start with ""DLT"" and not with " + str(start))
                        # Search for next position
                        pos = fstr.find(dlt_storageheader.DLTSTORAGESTART, pos)
                        if pos == -1:
                            print("Error: No DLT-Pattern found")
                            exit(-3)

                    storageheader = dlt_storageheader.DltStorageHeader(binst=fstr[pos:pos + 16])

                    # header
                    header = dlt_readheader.DltHeader(fstr[pos + 16:pos + 32])

                    # If there is no ECU-ID in the dlt-message heeader, the ECU_ID of the storage header is used instead
                    if header.ecuid == "":
                        header.ecuid = storageheader.ecu

                    # complete DLT message including header and extended header
                    message = dlt_message.DltMessage(
                        binst=fstr[pos + 16 + header.headerlength():pos + 16 + header.packetlength], header=header)

                    if self.filter.ok(message):
                        # export returns true, if the maximum of lines is reached
                        if self.exporter.export_message(message=message, storageheader=storageheader):
                            break

                    pos = pos + 16 + header.packetlength
                    if pos > len(fstr) - 4:
                        print("End of file has been reached")
                        break

                self.exporter.end_export()
                # csvexport.end()

                print(str(self.exporter.counter) + " Rows were exported")
        except FileNotFoundError:
            print("ERROR: File " + self.filename + " was not found.")
