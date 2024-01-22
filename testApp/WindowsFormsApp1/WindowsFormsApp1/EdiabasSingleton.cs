using Ediabas;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Threading;
using TestControl;
using WindowsFormsApp1;
using Word = Microsoft.Office.Interop.Word;
using System.Xml.Serialization;
using System.Xml.Linq;
using System.Linq;
using System.Xml;
using System.Windows.Forms;
using System.Threading.Tasks;

namespace DiagnosticModule
{
    /// <summary>
    /// Implements EDIABAS communication interface
    /// </summary>
    public class EdiabasSingleton
    {
        //max number of job executions before error set error state and break 
        private const int MaxCounter = 5;
        private const int lineSize = 33;
        private string path = @"C:\Example.txt";
        private string path1 = @"C:\Binary.txt";
        //Excel ex = new Excel(@"C:\Users\Andrew\imageMatching\excelFiles\Analysis.xlsx", 1);
        //        Excel ex1 = new Excel();
        int row = 0;
        int row1 = 0;
        int column = 1;
       //public string[,] str = new string[100000, 1000];
       //public string[,] str1 = new string[100000, 1000];
        private string date = DateTime.Now.ToString("yyMMdd_HHmm");
        private string date1 = DateTime.Now.ToString("yyMMdd_HHmmss");

        private string resultPath = @"E:\TestResults";




        Microsoft.Office.Interop.Excel.Application oXL;
        Microsoft.Office.Interop.Excel._Workbook oWB;
        Microsoft.Office.Interop.Excel._Worksheet oSheet;
        Microsoft.Office.Interop.Excel.Range oRng;
        object misvalue = System.Reflection.Missing.Value;

         //Form1 mc = new Form1();



        //possible EDIABAS module states



        public enum EdiabasState
        {
            Disconnected, Initialized, JobStoped, JobRunning, JobError
        }

        //current EDIABAS modul state
        public EdiabasState ModuleState { get; private set; }

        public static int StatusPollTime { get; set; }

        public string ResultDir { set; get; }

        public static EdiabasSingleton Instance
        {
            get
            {
                if (_ediabasModule == null)
                {
                    _ediabasModule = new EdiabasSingleton();
                }
                return _ediabasModule;
            }
        }
        private static EdiabasSingleton _ediabasModule;

        /// <summary>
        /// private singleton constructor
        /// </summary>
        public EdiabasSingleton()
        {
			ModuleState = EdiabasState.Disconnected;
			StatusPollTime = 500;
        }

        /// <summary>
        /// Initialise EDIABAS connection
        /// </summary>
        public void Init()
        {
            if (API.apiState() == API.APIREADY)
                return;

            bool result = false;
            if (ModuleState != EdiabasState.Initialized)
            {
                //result = API.enableServer(true); //NOTE: not needed
                result = API.apiInit(); //NOTE: The result is always true. 

                int apiState = WaitForExecution();
                int errorCode = API.apiErrorCode();

                if (apiState != API.APIREADY)
                {
                    Debug.WriteLine("apiState: {0}, errorcode {1}, errortext {2} ", apiState, errorCode, API.apiErrorText());
                    ModuleState = EdiabasState.JobError;
                    throw new EdiabasNotReadyException("Ediabas API is not ready.");
                }

                if (errorCode == API.EDIABAS_IFH_0029)
                {
                    Debug.WriteLine("Ediabas Init. ACCESS DENIED:  {1} . ", API.apiErrorText());
                    ModuleState = EdiabasState.JobError;
                    throw new EdiabasInitialiseFailedException();
                }

                if (result)//NOTE: In accordance with user manual, result should be APITRUE, but APITRUE is not implemented in API
                {
                    ModuleState = EdiabasState.Initialized;
                }
            }

        }



        /// <summary>
        /// Enables the multi threading.
        /// </summary>
        /// <param name="onOff">if set to <c>true</c> [on off].</param>
        /// <returns></returns>
        public static bool EnableMultiThreading(bool onOff)
        {
            return API.enableMultiThreading(onOff);
        }

        /// <summary>
        /// End  EDIABAS instance
        /// </summary>
        public void End()
        {
            API.apiEnd();
            ModuleState = EdiabasState.Disconnected;
        }

        /// <summary>
        /// Run single EDIABAS jobs with list of arguments
        /// </summary>
        /// <param name="sgbd">SGBD</param>
        /// <param name="jobName">job name</param>
        /// <param name="argListe">List of arguments as string list</param>
        public void Job(string sgbd, string jobName, List<string> argListe)
        {
            foreach (string argValue in argListe)
            {
                Job(sgbd, jobName, argValue);
            }
        }


        /// <summary>
        /// Run single EDIABAS jobs with arguments concatinated to the string
        /// </summary>
        /// <param name="sgbd">SGBD</param>
        /// <param name="jobName">job name</param>
        /// <param name="arg">arguments as string</param>
        public void Job(string sgbd, string jobName, string arg)
        {
            //use counter to avoid endless circle
            int counter = 0;
            int apiState = API.APIREADY;
            int errorCode = API.EDIABAS_ERR_NONE;

            //check if sgbd includes file extension, then remove it
            if( sgbd.IndexOf(".prg") > 0)
            {
                sgbd = sgbd.Substring(0, sgbd.IndexOf(".prg"));
            }

            ModuleState = EdiabasState.JobRunning;
            while (ModuleState == EdiabasState.JobRunning)  //kann durch Aufruf von stopActualJob unterbrochen werden
            {
                counter++;
                Debug.WriteLine("EDIABAS INFO: job: " + sgbd + ", " + jobName + ", " + arg);
                Console.WriteLine("EDIABAS INFO: apiJob: " + sgbd + ", " + jobName + ", " + arg);
                API.apiJob(sgbd, jobName, arg, String.Empty);  // Result wird später berücksichtigt

                Thread.Sleep(StatusPollTime);
                apiState = WaitForExecution();
                errorCode = API.apiErrorCode();

                if (apiState != API.APIREADY)
                {
                    HandleException(string.Format("apiState: {0}, errorcode {1}, errortext {2} ", apiState, errorCode, API.apiErrorText()));
                    //Debug.WriteLine("apiState: {0}, errorcode {1}, errortext {2} ", apiState, errorCode, API.apiErrorText());
                    API.apiInit();

                    if (counter < MaxCounter)
                    {
                        Thread.Sleep(StatusPollTime);
                        continue;
                    }
                    else
                    {
                        ModuleState = EdiabasState.JobError;
                    }

                }

                if (errorCode == API.EDIABAS_SYS_0005)
                {
                    HandleException(string.Format("SGBD {0} with job {1} not found. ", sgbd, jobName));
                    //Debug.WriteLine("SGBD {0} with job {1} not found. ", sgbd, jobName);
                    ModuleState = EdiabasState.JobError;
                }
                else
                {
                    if (errorCode == API.EDIABAS_IFH_0010)  // DATATRANSMISSION TO CONTROLUNIT DISTURBED wird vom IFH gemeldet, wenn die Verbindung abgerissen ist
                    {
                        HandleException(string.Format("apiState: {0}, errorcode {1}, errortext {2} ", apiState, errorCode, API.apiErrorText()));
                        //Debug.WriteLine("apiState: {0}, errorcode {1}, errortext {2} ", apiState, errorCode, API.apiErrorText());
                        ModuleState = EdiabasState.JobError;
                    }
                    else if (errorCode == API.EDIABAS_IFH_0006)  // COMMAND NOT ACCEPTED wird vom IFH gemeldet, wenn das DVM das Kommando nicht akzeptiert
                    {
                        if (counter < MaxCounter)
                        {
                            Thread.Sleep(StatusPollTime);
                            continue;
                        }
                        else
                        {
                            ModuleState = EdiabasState.JobError;
                        }
                    }
                }
                break;
            }
            if (ModuleState == EdiabasState.JobRunning)
            {
                ModuleState = EdiabasState.JobStoped;
            }
            else if (ModuleState == EdiabasState.JobError)
            {
                throw new EdiabasNotReadyException(string.Format("apiState: {0}, errorcode {1}, errortext {2} ", apiState, errorCode, API.apiErrorText()));
            }

        }


        

        /// <summary>
        /// Stop job execution. It means: do not wait for job execution any more.
        /// </summary>
        public void stopActualJobExecution()
        {
            //apiBreak(); NOTE: As I realisede - we do not need to call it. But may be in future releases of EDIABAS it will be needed
            ModuleState = EdiabasState.JobStoped;
        }

        /// <summary>
        /// Wait for job execution
        /// </summary>
        private int WaitForExecution()
        {
            //use counter to avoid endless circle
            int counter = 0;
            int state = API.apiStateExt(StatusPollTime);
            while (state == API.APIBUSY && ModuleState == EdiabasState.JobRunning && counter++ < MaxCounter)
            {
                // Thread.Sleep(statusPollTime);
                state = API.apiStateExt(StatusPollTime);
            }
            return state;
        }

        /// <summary>
        /// Exception handling
        /// <param name="description">Error description</param>
        /// <param name="ex">native exception</param>
        /// </summary>
        private static void HandleException(string description, Exception ex = null)
        {
            StackTrace stackTrace = new StackTrace();
            var MethodBase = stackTrace.GetFrame(1).GetMethod();
            var Class = MethodBase.ReflectedType;
            var Namespace = Class.Namespace;
            Debug.Indent();

            if (ex != null)
            {
                description += ". Exception: " + ex.Message;
            }
            Debug.WriteLine(@"{0}: in Funktion ""{1}"" Beschreibung: {2}", "EDIABAS ERROR", Namespace + "." + Class.Name + "." + MethodBase.Name, description);
            Debug.Unindent();
        }


        /// <summary>
        /// reads ediabas results.
        /// </summary>

        public void results()
        {

            ushort set, index;
            //               String[] data = new String[API.APIMAXNAME];
            row1 = row1 + 1;  
            row = row + 1;
            TextWriter tw = new StreamWriter(path, true);
            TextWriter tw1 = new StreamWriter(path1, true);
            //ex1.CreateNewFile();
            //ex1.CreateNewSheet();
            //ex1.SaveAs(@"Test");

            if (API.apiResultSets(out ushort s))
            {
                /* Fuer alle Ergebnissaetze */

                for (set = 0; (set <= s) && (API.apiErrorCode() == API.EDIABAS_ERR_NONE); set++)
                {


                                            tw.WriteLine("SET {0}:", set);
                  

                    /* Anzahl der Ergebnisse im aktuellen Ergebnissatz */

                    if (API.apiResultNumber(out ushort i, set))
                    {

                        /* Fuer alle Ergebnisse */

                        for (index = 1; (index <= i) && (API.apiErrorCode() == API.EDIABAS_ERR_NONE); index++)

                        {

                            /* Ergebnisnamen bestimmen */

                            if (API.apiResultName(out string data, index, set))
                            {

                                                                   tw.WriteLine(" {0}RESULT {1}:  ", (index == 1) ? "" : "         ", index);
                              
                                if (API.apiResultFormat(out int format, data, set))
                                {

                                    /* Ergebnisse nach Format auslesen und ausgeben */
//                                    Console.WriteLine("Format {0}", format);
                                    switch (format)
                                    {

                                        case API.APIFORMAT_INTEGER:
                                            API.apiResultInt(out short intG, data, set);
                                            Console.WriteLine("Integer Data: {0} = {1} ", data, intG);
                                                                                          tw.WriteLine("Integer Data: {0} = {1} ", data, intG);
                                          
                                            break;
                                        case API.APIFORMAT_TEXT:
                                            API.apiResultText(out string t, data, set, "");
                                            Console.WriteLine("Text Data: {0} = {1} {2} {3} ", data, '"', t, '"');
                                                                                           tw.WriteLine("Text Data: {0} = {1} {2} {3} ", data, '"', t, '"');
                                           
                                            break;

                                        case API.APIFORMAT_CHAR:
                                            API.apiResultChar(out char c, data, set);
                                            Console.WriteLine("Char Data: {0} = {1} ", data, c);
                                                                                          tw.WriteLine("Char Data: {0} = {1} ", data, c);
                                          
                                            break;
                                        case API.APIFORMAT_BYTE:
                                            API.apiResultByte(out byte b, data, set);
                                            Console.WriteLine("Byte Data: {0} = {1} ", data, b);
                                                                                            tw.WriteLine("Byte Data: {0} = {1} ", data, b);
                                       
                                            break;
                                        case API.APIFORMAT_WORD:
                                            API.apiResultWord(out ushort w, data, set);
                                            Console.WriteLine("Word Data: {0} = {1} ", data, w);
                                                                                           tw.WriteLine("Word Data: {0} = {1} ", data, w);
                                        
                                            break;
                                        case API.APIFORMAT_LONG:
                                            API.apiResultLong(out int l, data, set);
                                            Console.WriteLine("Long Data: {0} = {1} ", data, l);
                                                                                            tw.WriteLine("Long Data: {0} = {1} ", data, l);

                                            break;
                                        case API.APIFORMAT_DWORD:
                                            API.apiResultDWord(out uint dw, data, set);
                                            Console.WriteLine("Dword Data: {0} = {1} ", data, dw);
                                                                                            tw.WriteLine("Dword Data: {0} = {1} ", data, dw);

                                            break;
                                        case API.APIFORMAT_REAL:
                                            API.apiResultReal(out double r, data, set);
                                            Console.WriteLine("Real Data: {0} = {1} ", data, r);
                                                                                            tw.WriteLine("Real Data: {0} = {1} ", data, r);

                                            break;
                                        case API.APIFORMAT_BINARY:
                                            API.apiResultBinary(out byte[] yb, out ushort length, data, set);
                                            Console.WriteLine("Binary Data: {0} = {1} ", data, length);
                                                                                            tw.WriteLine("Binary Data: {0} = {1} ", data, length);
                                            
                                            for(int x = 0; x < length; x ++)
                                            {
                                                if (yb[x] < 16)
                                                {
                                                    string hexVal = yb[x].ToString("X");
                                                    string zero = "0";
                                                    string hexVal1 = string.Concat(zero, hexVal);
                                                    Console.Write(" {0} ", hexVal1);
                                                    tw.Write(" {0} ", hexVal1);
                                                    tw1.Write(" {0} ", hexVal1);
                                                    //str[row, x] = hexVal1;
                                                    //str1[row1, x] = hexVal1; 

//                                                    row++;
//                                                    ex.WriteToCell(row, x, hexVal1);
                               
                                                }
                                                else
                                                {
                                                    string hexVal = yb[x].ToString("X");
                                                    Console.Write(" {0} ", hexVal);
                                                    tw.Write(" {0} ", hexVal);
                                                    tw1.Write(" {0} ", hexVal);
                                                    //str[row, x] = hexVal;
                                                    //str1[row1, x] = hexVal;
                                                    //                                                    row++;
                                                    //                                                    ex.WriteToCell(row, x, hexVal)


                                                }

                                            }
//                                            ex.WriteRange(1, 1, 1000, 1, str);
                                            //                                            Console.Write("the row is {0} ", row);
                                            //                                            row++;

                                            //                                           printBinary(yb, length);
                                            break;


                                    }
                                 
                                }

                            }
                        }
                    }
                    
                }
                
            }

            tw.Close();
            tw1.Close();

        }

        /// <summary>
        /// writes results to a specific folder and with specified name 
        /// </summary>
        /// <param name="directory"></param>
        /// <param name="saveName"></param>

        public void Results_1(string directory, string saveName)
        {
            ResultDir = directory;
            ushort set, index;
            //               String[] data = new String[API.APIMAXNAME];
            //            row1 = row1 + 1;
            //            row = row + 1;
            XmlSerializer xs = new XmlSerializer(typeof(string));
            string fileName = Path.Combine(ResultDir,  @saveName + "_"+ date + ".txt");
            //string fileName1 = Path.Combine(ResultDir, @saveName + "_1" + ".txt");



            //                TextWriter writer = new StreamWriter(filename);
            TextWriter tw = new StreamWriter(fileName, append: true);
            //StreamWriter file = new StreamWriter(fileName1, append: true);


            if (API.apiResultSets(out ushort s))
            {
                /* Fuer alle Ergebnissaetze */

                for (set = 0; (set <= s) && (API.apiErrorCode() == API.EDIABAS_ERR_NONE); set++)
                {


                    //tw.WriteLine("SET {0}:", set);


                    /* Anzahl der Ergebnisse im aktuellen Ergebnissatz */

                    if (API.apiResultNumber(out ushort i, set))
                    {

                        /* Fuer alle Ergebnisse */

                        for (index = 1; (index <= i) && (API.apiErrorCode() == API.EDIABAS_ERR_NONE); index++)

                        {

                            /* Ergebnisnamen bestimmen */

                            if (API.apiResultName(out string data, index, set))
                            {

                                //tw.WriteLine(" {0}RESULT {1}:  ", (index == 1) ? "" : "         ", index);

                                if (API.apiResultFormat(out int format, data, set))
                                {

                                    /* Ergebnisse nach Format auslesen und ausgeben */
                                    //                                    Console.WriteLine("Format {0}", format);
                                    switch (format)
                                    {

                                        case API.APIFORMAT_INTEGER:
                                            API.apiResultInt(out short intG, data, set);
                                            //    Console.WriteLine("Integer Data: {0} = {1} ", data, intG);
                                            //tw.WriteLine("Integer Data: {0} = {1} ", data, intG);

                                            break;
                                        case API.APIFORMAT_TEXT:
                                            API.apiResultText(out string t, data, set, "");
                                            //      Console.WriteLine("Text Data: {0} = {1} {2} {3} ", data, '"', t, '"');
                                            //tw.WriteLine("Text Data: {0} = {1} {2} {3} ", data, '"', t, '"');

                                            break;

                                        case API.APIFORMAT_CHAR:
                                            API.apiResultChar(out char c, data, set);
                                            //         Console.WriteLine("Char Data: {0} = {1} ", data, c);
                                            //tw.WriteLine("Char Data: {0} = {1} ", data, c);

                                            break;
                                        case API.APIFORMAT_BYTE:
                                            API.apiResultByte(out byte b, data, set);
                                            //           Console.WriteLine("Byte Data: {0} = {1} ", data, b);
                                            //tw.WriteLine("Byte Data: {0} = {1} ", data, b);

                                            break;
                                        case API.APIFORMAT_WORD:
                                            API.apiResultWord(out ushort w, data, set);
                                            //              Console.WriteLine("Word Data: {0} = {1} ", data, w);
                                            //tw.WriteLine("Word Data: {0} = {1} ", data, w);

                                            break;
                                        case API.APIFORMAT_LONG:
                                            API.apiResultLong(out int l, data, set);
                                            //                Console.WriteLine("Long Data: {0} = {1} ", data, l);
                                            //tw.WriteLine("Long Data: {0} = {1} ", data, l);

                                            break;
                                        case API.APIFORMAT_DWORD:
                                            API.apiResultDWord(out uint dw, data, set);
                                            //                 Console.WriteLine("Dword Data: {0} = {1} ", data, dw);
                                            //tw.WriteLine("Dword Data: {0} = {1} ", data, dw);

                                            break;
                                        case API.APIFORMAT_REAL:
                                            API.apiResultReal(out double r, data, set);
                                            //                   Console.WriteLine("Real Data: {0} = {1} ", data, r);
                                            //tw.WriteLine("Real Data: {0} = {1} ", data, r);

                                            break;
                                        case API.APIFORMAT_BINARY:
                                            API.apiResultBinary(out byte[] yb, out ushort length, data, set);
                                            Console.WriteLine("Binary Data: {0} = {1} ", data, length );
                                            tw.WriteLine("Binary Data: {0} = {1} ", data, length);

                                            for (int x = 0; x < length; x++)
                                            {
                                                if (yb[x] < 16)
                                                {
                                                    string hexVal = yb[x].ToString("X");
                                                    string zero = "0";
                                                    string hexVal1 = string.Concat(zero, hexVal);
                                                    Console.Write(" {0} ", hexVal1);
                                                    tw.Write(" {0} ", hexVal1);
                                                    //file.Write(hexVal1);
                                                    //str[row, x] = hexVal1;
                                                    //str1[row1, x] = hexVal1;
                                                    //                                                        tw1.Write(" {0} ", hexVal1);
                                                    //                                                    str[row, x] = hexVal1;
                                                    //
                                                    //                                                    row++;
                                                    //                                                    ex.WriteToCell(row, x, hexVal1);

                                                }
                                                else
                                                {
                                                    string hexVal = yb[x].ToString("X");
                                                    Console.Write(" {0} ", hexVal);
                                                    tw.Write(" {0} ", hexVal);
                                                    //file.Write(hexVal);
                                                    //str[row, x] = hexVal;
                                                    //str1[row1, x] = hexVal;
                                                    //                                                        tw1.Write(" {0} ", hexVal);
                                                    //                                                   str[row, x] = hexVal;
                                                    //                                                   str1[row1, x] = hexVal;
                                                    //                                                    row++;
                                                    //                                                    ex.WriteToCell(row, x, hexVal)


                                                }

                                            }
                                            //                                            ex.WriteRange(1, 1, 1000, 1, str);
                                                                                        Console.Write(Environment.NewLine);
                                            //                                            row++;

                                            //                                           printBinary(yb, length);
                                            break;


                                    }

                                }

                            }
                        }
                    }

                }


            }
            tw.Close();
            //            tw1.Close();



        }
/// <summary>
/// saves all the data to a file in a specific directory
/// </summary>
/// <param name="directory"></param>
/// <param name="saveName"></param>

        public void Results_2(string directory, string saveName)
        {
            ResultDir = directory;
            ushort set, index;
            //               String[] data = new String[API.APIMAXNAME];
            //            row1 = row1 + 1;
            //            row = row + 1;
            XmlSerializer xs = new XmlSerializer(typeof(string));
            string fileName = Path.Combine(ResultDir, @saveName + "_" + date + ".txt");
            //string fileName1 = Path.Combine(ResultDir, @saveName + "_1" + ".txt");



            //                TextWriter writer = new StreamWriter(filename);
            TextWriter tw = new StreamWriter(fileName, append: true);
            //StreamWriter file = new StreamWriter(fileName1, append: true);


            if (API.apiResultSets(out ushort s))
            {
                /* Fuer alle Ergebnissaetze */

                for (set = 0; (set <= s) && (API.apiErrorCode() == API.EDIABAS_ERR_NONE); set++)
                {

                    tw.WriteLine("Date and Time  {0}:", date1);
                    tw.WriteLine("SET {0}:", set);
                    


                    /* Anzahl der Ergebnisse im aktuellen Ergebnissatz */

                    if (API.apiResultNumber(out ushort i, set))
                    {

                        /* Fuer alle Ergebnisse */

                        for (index = 1; (index <= i) && (API.apiErrorCode() == API.EDIABAS_ERR_NONE); index++)

                        {

                            /* Ergebnisnamen bestimmen */

                            if (API.apiResultName(out string data, index, set))
                            {

                                tw.WriteLine(" {0}RESULT {1}:  ", (index == 1) ? "" : "         ", index);

                                if (API.apiResultFormat(out int format, data, set))
                                {

                                    /* Ergebnisse nach Format auslesen und ausgeben */
                                    //                                    Console.WriteLine("Format {0}", format);
                                    switch (format)
                                    {

                                        case API.APIFORMAT_INTEGER:
                                            API.apiResultInt(out short intG, data, set);
                                                Console.WriteLine("Integer Data: {0} = {1} ", data, intG);
                                            tw.WriteLine("Integer Data: {0} = {1} ", data, intG);

                                            break;
                                        case API.APIFORMAT_TEXT:
                                            API.apiResultText(out string t, data, set, "");
                                                  Console.WriteLine("Text Data: {0} = {1} {2} {3} ", data, '"', t, '"');
                                            tw.WriteLine("Text Data: {0} = {1} {2} {3} ", data, '"', t, '"');

                                            break;

                                        case API.APIFORMAT_CHAR:
                                            API.apiResultChar(out char c, data, set);
                                                     Console.WriteLine("Char Data: {0} = {1} ", data, c);
                                            tw.WriteLine("Char Data: {0} = {1} ", data, c);

                                            break;
                                        case API.APIFORMAT_BYTE:
                                            API.apiResultByte(out byte b, data, set);
                                                      Console.WriteLine("Byte Data: {0} = {1} ", data, b);
                                            tw.WriteLine("Byte Data: {0} = {1} ", data, b);

                                            break;
                                        case API.APIFORMAT_WORD:
                                            API.apiResultWord(out ushort w, data, set);
                                                          Console.WriteLine("Word Data: {0} = {1} ", data, w);
                                            tw.WriteLine("Word Data: {0} = {1} ", data, w);

                                            break;
                                        case API.APIFORMAT_LONG:
                                            API.apiResultLong(out int l, data, set);
                                                            Console.WriteLine("Long Data: {0} = {1} ", data, l);
                                            tw.WriteLine("Long Data: {0} = {1} ", data, l);

                                            break;
                                        case API.APIFORMAT_DWORD:
                                            API.apiResultDWord(out uint dw, data, set);
                                                             Console.WriteLine("Dword Data: {0} = {1} ", data, dw);
                                            tw.WriteLine("Dword Data: {0} = {1} ", data, dw);

                                            break;
                                        case API.APIFORMAT_REAL:
                                            API.apiResultReal(out double r, data, set);
                                                               Console.WriteLine("Real Data: {0} = {1} ", data, r);
                                            tw.WriteLine("Real Data: {0} = {1} ", data, r);

                                            break;
                                        case API.APIFORMAT_BINARY:
                                            API.apiResultBinary(out byte[] yb, out ushort length, data, set);
                                            Console.WriteLine("Binary Data: {0} = {1} ", data, length);
                                            tw.WriteLine("Binary Data: {0} = {1} ", data, length);

                                            for (int x = 0; x < length; x++)
                                            {
                                                if (yb[x] < 16)
                                                {
                                                    string hexVal = yb[x].ToString("X");
                                                    string zero = "0";
                                                    string hexVal1 = string.Concat(zero, hexVal);
                                                    Console.Write(" {0} ", hexVal1);
                                                    tw.Write(" {0} ", hexVal1);
                                                    //file.Write(hexVal1);
                                                    //str[row, x] = hexVal1;
                                                    //tr1[row1, x] = hexVal1;
                                                    //                                                        tw1.Write(" {0} ", hexVal1);
                                                    //                                                    str[row, x] = hexVal1;
                                                    //
                                                    //                                                    row++;
                                                    //                                                    ex.WriteToCell(row, x, hexVal1);

                                                }
                                                else
                                                {
                                                    string hexVal = yb[x].ToString("X");
                                                    Console.Write(" {0} ", hexVal);
                                                    tw.Write(" {0} ", hexVal);
                                                    //file.Write(hexVal);
                                                    //str[row, x] = hexVal;
                                                    //str1[row1, x] = hexVal;
                                                    //                                                        tw1.Write(" {0} ", hexVal);
                                                    //                                                   str[row, x] = hexVal;
                                                    //                                                   str1[row1, x] = hexVal;
                                                    //                                                    row++;
                                                    //                                                    ex.WriteToCell(row, x, hexVal)


                                                }

                                            }
                                            //                                            ex.WriteRange(1, 1, 1000, 1, str);
                                            Console.Write(Environment.NewLine);
                                            //                                            row++;

                                            //                                           printBinary(yb, length);
                                            break;


                                    }

                                }

                            }
                        }
                    }

                }


            }
            tw.Close();
            //            tw1.Close();



        }





        /// <summary>
        /// Modify an XML to give it a new value. not tested
        /// </summary>
        public void AdjustXmlFile()
        {
            var doc = XDocument.Load("diagnosisParameters.xml");

            //select all leaf elements having value equals "john"
            var elementsToUpdate = doc.Descendants()
                                      .Where(o => o.Value == "john" && !o.HasElements);

            //update elements value
            foreach (XElement element in elementsToUpdate)
            {
                element.Value = "danny";
            }

            //save the XML back as file
            doc.Save("diagnosisParameters.xml");
        }

        // Modify an XML to give it a new value. currently used
        /// <summary>
        /// 
        /// </summary>
        /// <param name="tag"></param>
        /// <param name="position"></param>
        /// <param name="newValue"></param>
        /// /// <param name="doc"></param>
        public void ModifyXmlFile(string doc , string tag, string position,  string newValue )
        {

            //Here is the variable with which you assign a new value to the attribute
  
    

            XmlDocument xmlDoc = new XmlDocument();

            xmlDoc.Load(doc);


            XmlNodeList elemList = xmlDoc.GetElementsByTagName(tag);
            //for (int i = 0; i < elemList.Count; i++)
            //{
            Debug.WriteLine(elemList[1].InnerXml);
            int position1 = Int32.Parse(position);
            elemList[position1].InnerXml = newValue;

            xmlDoc.Save(doc);


        }

        /// <summary>
        /// get the value of a variable from xml file
        /// </summary>
        /// <param name="tag"></param>
        /// <param name="doc"></param>
        /// <param name="position"></param>
        /// <returns></returns>
        public string getXmlVal(string doc, string tag, int position)
        {

            XmlDocument xmlDoc = new XmlDocument();

            //xmlDoc.Load("diagnosisParameters.xml");
            xmlDoc.Load(doc);

            XmlNodeList elemList = xmlDoc.GetElementsByTagName(tag);
            return elemList[position].InnerXml;

        }
        
        /// <summary>
        /// no tested 
        /// </summary>
        /// <param name="cmd"></param>
        /// <param name="args"></param>
        /// <returns></returns>
        public string Run_cmd(string cmd, string args)
        {
            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = @"C:\ProgramData\Anaconda3\envs\compVision10\python.exe"; ;
            start.Arguments = string.Format("\"{0}\" \"{1}\"", cmd, args);
            start.UseShellExecute = false;// Do not use OS shell
            start.CreateNoWindow = true; // We don't need new window
            start.RedirectStandardOutput = true;// Any output, generated by application will be redirected back
            start.RedirectStandardError = true; // Any error in standard output will be redirected back (for example exceptions)
            using (Process process = Process.Start(start))
            {
                using (StreamReader reader = process.StandardOutput)
                {
                    string stderr = process.StandardError.ReadToEnd(); // Here are the exceptions from our Python script
                    string result = reader.ReadToEnd(); // Here is the result of StdOut(for example: print "test")
                    
                    Debug.WriteLine(result);
                    return result;
                }
            }
        }
        /// <summary>
        /// function is not used ... yet
        /// </summary>
        /// <param name="reader"></param>
        /// <param name="progress"></param>
        /// <returns></returns>
        public static async Task ReadTextReaderAsync(TextReader reader, IProgress<string> progress)
        {
            char[] buffer = new char[1024];
            for (; ; )
            {
                int count = await reader.ReadAsync(buffer, 0, buffer.Length).ConfigureAwait(false);
                if (count == 0)
                {
                    break;
                }
                progress.Report(new string(buffer, 0, count));
            }
        }


        /// <summary>
        /// tested and working 
        /// </summary>
        /// <param name="exeORpy"></param>
        /// <param name="args"></param>
        /// <param name="output"></param>
        public void Run_cmd2(string exeORpy, string args)
        {

            var outputStream = new StreamWriter("E:\\TestResults\\testOut.txt");
            // create a process with the name procided by the 'exe' variable 
            Process cmd = new Process();
            cmd.StartInfo.FileName = exeORpy;
            //define you preference on the window and input/output 
            cmd.StartInfo.RedirectStandardInput = true;
            cmd.StartInfo.RedirectStandardOutput = true;
            cmd.StartInfo.CreateNoWindow = true;
            cmd.StartInfo.UseShellExecute = false;
            // write the output to file created 

            cmd.OutputDataReceived += new DataReceivedEventHandler((sender, e) =>
            {
                if (!String.IsNullOrEmpty(e.Data))
                {
                    outputStream.WriteLine(e.Data);
                    //Debug.WriteLine(e.Data);



                }
            });


            //cmd.OutputDataReceived += (sender, e) => Form1.Display(e.Data);
            //cmd.ErrorDataReceived += (sender, e) => Form1.Display(e.Data);
            cmd.Start();

            //cmd.StandardInput.WriteLine("python3 -c 'import os ; os.chdir('C:\\Users\\Andrew\\imageMatching\\excelFiles') ; import search3 ; print(search3.readListDTCs('ICBox'))'");
            // write to the console you opened. In this case for example the python console 
            cmd.StandardInput.WriteLine(args);
            //Read the output and close everything. make sure you wait till the end of the process 
            cmd.BeginOutputReadLine();


            cmd.StandardInput.Flush();
            cmd.StandardInput.Close();

            //Progress<string> writeToConsole = new Progress<string>(Console.Write);

            //Task stdout = ReadTextReaderAsync(cmd.StandardOutput, writeToConsole);
            //Task stderr = ReadTextReaderAsync(cmd.StandardError, writeToConsole);
            cmd.WaitForExit();
    


            //close the process. writing to debug helps when coding
            outputStream.Close();
            //cmd.StandardOutput.ReadToEnd(); 
            cmd.Close();
            Debug.WriteLine("\n\n script finished.");
            Console.ReadLine();

        }
        /// <summary>
        /// run process and call EDIABAS jobs
        /// </summary>
        /// <param name="exeORpy"></param>
        /// <param name="args"></param>
        public void Run_cmd3(string exeORpy, string args)
        {

            //var outputStream = new StreamWriter(output);
            // create a process with the name procided by the 'exe' variable 
            System.Diagnostics.Process cmd = new System.Diagnostics.Process();
            cmd.StartInfo.FileName = exeORpy;
            //define you preference on the window and input/output 
            cmd.StartInfo.RedirectStandardInput = true;
            cmd.StartInfo.RedirectStandardOutput = true;
            cmd.StartInfo.CreateNoWindow = true;
            cmd.StartInfo.UseShellExecute = false;
            // write the output to file created 
            cmd.OutputDataReceived += new DataReceivedEventHandler((sender, e) =>
            {
                if (!String.IsNullOrEmpty(e.Data))
                {
                    //outputStream.WriteLine(e.Data);
                    //string data = e.Data;
                    string[] words = e.Data.Split('$');
                    //Console.WriteLine(e.Data + Environment.NewLine);
                    //Console.WriteLine(words[0] + Environment.NewLine);
                    //int Ln = words.Length;
                    //Job(words[0], words[1], words[2]);
                    // Check the length of the words array
                    if (words.Length >= 3)
                    {
                        Job(words[0], words[1], words[2]);
                        //mc.HandleRadioButtonSelection();
                        Results_2(resultPath, "Custom_Job ");
                    }
                    else if (words.Length == 2)
                    {
                        // Handle the case when there are 2 words
                        Job(words[0], words[1], "");
                        Results_2(resultPath, "Custom_Job ");
                    }

                }
            });
            cmd.Start();

            //cmd.StandardInput.WriteLine("python3 -c 'import os ; os.chdir('C:\\Users\\Andrew\\imageMatching\\excelFiles') ; import search3 ; print(search3.readListDTCs('ICBox'))'");
            // write to the console you opened. In this case for example the python console 
            cmd.StandardInput.WriteLine(args);
            //Read the output and close everything. make sure you wait till the end of the process 
            cmd.BeginOutputReadLine();
            cmd.StandardInput.Flush();
            cmd.StandardInput.Close();
            //cmd.WaitForExit();
            while (!cmd.HasExited)
            {
                Application.DoEvents(); // This keeps your form responsive by processing events
            }

            //close the process. writing to debug helps when coding
            //outputStream.Close();
            //Console.WriteLine(cmd.StandardOutput.ReadToEnd()); 
            cmd.Close();
            Debug.WriteLine("\n\nDTC analysis done.");
            //Console.ReadLine();

        }




    }
}
