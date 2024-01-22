using OxyPlot;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Diagnostics;
using System.IO;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Xml;

namespace PowerSupplyModule
{
    /// <summary>
    /// Implements power supply communication interface
    /// </summary>
    public class PowerSupply : IDisposable
    {

        //Power supply module states will be used by PowerSupplyViewModel
        //TestFinisched - Curve is completely finished in PowerSupply 

        public enum PowerSupplyState
        {
            Connected, Disconnected, TestRunning, TestFinished
        }

        public enum TestType
        {
            NoTest, ConstantVoltageTest, CurveTest
        }

        PowerSupplyCurrentProgress progress = new PowerSupplyCurrentProgress();
        

        public PowerSupplyState ModuleState { get; private set; }

        private TestType _currentTest;

        public List<double[]> waveForm_generated;

        public List<DataPoint> Points = new List<DataPoint>();
        private int CurrentPos = 0;

        public double MaxCurrent { get; set; }
        public double MaxVolt { get; set; }
        public TcpClient Tcpclnt { get; set; }
        public Stream Stm { get; set; }

        public static double Duration { get; set; } = 0;

        private bool StatusTrackingActive { get; set; } = false;
        private bool EthBusy { get; set; } = false;

        //Constants shold be filled in the future from Data base
        private const double minStep = 0.01;
        private const double maxStep = 10;
        private const int maxPoints = 1000;
        private const int chartStep = 5000;

        private readonly BackgroundWorker backgroundWorker1;
        private readonly BackgroundWorker backgroundWorker2;

        public static PowerSupply Instance
        {
            get
            {
                if (_powerSupply == null)
                {
                    _powerSupply = new PowerSupply();
                }
                return _powerSupply;
            }
        }

        //for constante voltage test only
        public double GlobalVoltage { get; private set; } = 0;

        private static PowerSupply _powerSupply;

        private PowerSupply()
        {
            // singleton constructor
			ModuleState = PowerSupplyState.Disconnected;
            
            backgroundWorker1 = new BackgroundWorker();
            this.backgroundWorker1.WorkerReportsProgress = true;
            this.backgroundWorker1.WorkerSupportsCancellation = true;

            backgroundWorker2 = new BackgroundWorker();
            this.backgroundWorker2.WorkerReportsProgress = true;
            this.backgroundWorker2.WorkerSupportsCancellation = true;

            InitializeBackgroundWorker();
        }

        /// <summary>
        /// Event handler for when a power supply finished procedure.
        /// A caller has to register on this event to receive finish test event.
        /// </summary>
        public event EventHandler<EventArgs> TestFinishedEvent;

        protected virtual void OnTestFinishedEvent(EventArgs e)
        {
            TestFinishedEvent?.Invoke(this, e);
           
        }

        public event EventHandler<PowerSupplyCurrentProgress> PowerSupplyUpdate;

        protected void OnPowerSupplyUpdate(PowerSupplyCurrentProgress progress)
        {
            PowerSupplyUpdate?.Invoke(this, progress);
        }

        public event EventHandler<PowerSupplySetedVoltage> PowerSupplySetVoltage;

        protected void OnPowerSupplySetVoltage(PowerSupplySetedVoltage settings)
        {
            PowerSupplySetVoltage?.Invoke(this, settings);
        }

        private void InitializeBackgroundWorker()
        {
            backgroundWorker1.DoWork += new DoWorkEventHandler(backgroundWorker1_DoWork);
            backgroundWorker1.RunWorkerCompleted += new RunWorkerCompletedEventHandler(backgroundWorker1_RunWorkerCompleted);

            backgroundWorker2.DoWork += new DoWorkEventHandler(backgroundWorker2_DoWork);
            backgroundWorker2.RunWorkerCompleted += new RunWorkerCompletedEventHandler(backgroundWorker2_RunWorkerCompleted);
        }

        public List<DataPoint> createChart(List<double[]> waveForm_generated)
        {
            Points.Clear();
            calculateWaveformDuration(waveForm_generated);
            double step = Duration / chartStep;
            double pos = 0;
            double stepPos = 0;


            int[] sinParameters = new int[] { 0, 0, 0 };
            for (int i = 0; i < waveForm_generated.Count; i++)
            {
                if (waveForm_generated[i].Length > 3) // Sinus
                {
                    sinParameters[0] = (int)waveForm_generated[i][3]; // loops
                    sinParameters[1] = (int)waveForm_generated[i][4]; // start
                    sinParameters[2] = (int)waveForm_generated[i][5]; // length
                }
            }

            for (int i = 0; i < sinParameters[1]; i++) // Werte von Block 0
            {
                pos += waveForm_generated[i][2];
                while (pos > stepPos)
                {
                  Points.Add(new DataPoint(stepPos, waveForm_generated[i][0]));
                    stepPos += step;
                }
            }
            for (int j = 0; j < sinParameters[0]; j++)// sinus
            {
                for (int i = sinParameters[1]; i < sinParameters[1] + sinParameters[2]; i++)
                {
                    pos += waveForm_generated[i][2];
                    while (pos > stepPos)
                    {
                        Points.Add(new DataPoint(stepPos, waveForm_generated[i][0]));
                        stepPos += step;
                    }
                }
            }
            for (int i = sinParameters[1] + sinParameters[2] + 1; i < waveForm_generated.Count; i++) // nach sinus
            {
                pos += waveForm_generated[i][2];
                while (pos > stepPos)
                {
                    Points.Add(new DataPoint(stepPos, waveForm_generated[i][0]));
                    stepPos += step;
                }
            }

            return Points;
        }

        static List<float[]> loadWaveForm(string filename)
        {
            var waveFormArray = new List<float[]>();
            XmlDocument xmlDoc = new XmlDocument();
            xmlDoc.Load(filename);
            foreach (XmlNode xn in xmlDoc.ChildNodes[1].ChildNodes[0].ChildNodes[0].ChildNodes[0].ChildNodes)
            {
                bool sine = false;
                if (xn.ChildNodes.Count > 0)
                {
                    if (xn.ChildNodes[0].Name == "sine") // Abfrage ob sine kann erst gemacht werden wenn auf child nodes geprüft wurde
                    {
                        sine = true;
                        waveFormArray.Add(new float[7]);
                    }
                    else
                    {
                        waveFormArray.Add(new float[3]);
                    }
                }
                else
                {
                    waveFormArray.Add(new float[3]);
                }
                waveFormArray[waveFormArray.Count - 1][0] = float.Parse(xn.Attributes.GetNamedItem("duration").Value, System.Globalization.CultureInfo.InvariantCulture);
                waveFormArray[waveFormArray.Count - 1][1] = float.Parse(xn.Attributes.GetNamedItem("start").Value, System.Globalization.CultureInfo.InvariantCulture);
                waveFormArray[waveFormArray.Count - 1][2] = float.Parse(xn.Attributes.GetNamedItem("end").Value, System.Globalization.CultureInfo.InvariantCulture);
                if (sine)
                {
                    waveFormArray[waveFormArray.Count - 1][3] = float.Parse(xn.ChildNodes[0].ChildNodes[0].Attributes.GetNamedItem("start").Value, System.Globalization.CultureInfo.InvariantCulture); //Amplitude
                    waveFormArray[waveFormArray.Count - 1][4] = float.Parse(xn.ChildNodes[0].ChildNodes[0].Attributes.GetNamedItem("end").Value, System.Globalization.CultureInfo.InvariantCulture);
                    waveFormArray[waveFormArray.Count - 1][5] = float.Parse(xn.ChildNodes[0].ChildNodes[1].Attributes.GetNamedItem("start").Value, System.Globalization.CultureInfo.InvariantCulture); // Frequenz
                    waveFormArray[waveFormArray.Count - 1][6] = float.Parse(xn.ChildNodes[0].ChildNodes[1].Attributes.GetNamedItem("end").Value, System.Globalization.CultureInfo.InvariantCulture);
                }
            }
            return waveFormArray;
        }

        List<double[]> calculateWaveForm(List<float[]> waveForm_raw)
        {
            int rampCount = 0;
            int lastCount = 0;
            //double MaxCurrent = 20;
            var waveForm_generated_local = new List<double[]>();
            int localMaxRampPoints = 10;

            do
            {
                lastCount = waveForm_generated_local.Count;
                waveForm_generated_local.Clear();
                rampCount = 0;

                for (int i = 0; i < waveForm_raw.Count; i++)
                {
                    double val0 = (double)(decimal)waveForm_raw[i][0];
                    double val1 = (double)(decimal)waveForm_raw[i][1];
                    double val2 = (double)(decimal)waveForm_raw[i][2];

                    double timeRounded = (int)(val0 / minStep + 0.5) * minStep; // Zeit auf Step-Werte auf/ab runden
                    if (timeRounded == 0)
                        continue;

                    if (waveForm_raw[i].Length > 3) // Sinus
                    {
                        double val3 = (double)(decimal)waveForm_raw[i][3];
                        //   double val4 = (double)(decimal)waveForm_raw[i][4];
                        double val5 = (double)(decimal)waveForm_raw[i][5];

                        int valuesPerSin = (int)((1 / val5) / minStep);
                        int sinLoops = (int)Math.Ceiling(timeRounded * val5);
                        int sinStart = waveForm_generated_local.Count;
                        for (int k = 1; k <= valuesPerSin; k++) // Erstellt ein Sinus
                        {
                            waveForm_generated_local.Add(new double[6] { Math.Sin((double)k / valuesPerSin * Math.PI * 2) * val3 / 2 + val1, MaxCurrent, minStep, sinLoops, sinStart, valuesPerSin });
                        }
                    }
                    else if (val1 != val2) // Rampe
                    {
                        double rampStep = val0 / localMaxRampPoints;
                        rampStep = (int)(rampStep / minStep + 0.5) * minStep;
                        if (rampStep < minStep)
                            rampStep = minStep;
                        double voltStep = (val2 - val1) / (int)Math.Ceiling(timeRounded / rampStep);

                        if (timeRounded >= rampStep)
                        {
                            for (int j = 1; j <= (int)Math.Ceiling(timeRounded / rampStep); j++)
                            {
                                waveForm_generated_local.Add(new double[3] { val1 + voltStep * j, MaxCurrent, rampStep });
                            }
                        }
                        else
                        { // Rampe zu steil -> DWEL auf 0
                            waveForm_generated_local.Add(new double[3] { val2, MaxCurrent, 0.000 });
                        }
                        rampCount++;
                    }
                    else
                    {
                        while (timeRounded > maxStep)
                        {
                            waveForm_generated_local.Add(new double[3] { val1, MaxCurrent, maxStep });
                            timeRounded = timeRounded - maxStep;
                        }
                        if (timeRounded > 0)
                        {
                            waveForm_generated_local.Add(new double[3] { val1, MaxCurrent, timeRounded });
                        }
                    }
                }
                if ((waveForm_generated_local.Count < (maxPoints * 0.95)) && (rampCount > 0)) // Wenn Rampe vorhanden mindestens 95% der SpeicherPunkte (die das Netzteil bereitstellt) verwenden
                {
                    localMaxRampPoints += 2;
                }
            } while ((lastCount != waveForm_generated_local.Count) && (rampCount > 0)); // wenn Rampen vorhanden und erhöhung der Punkte nicht mehr Punkte liefert schleife beenden
            return waveForm_generated_local;
        }

        static double calculateWaveformDuration(List<double[]> waveForm_generated)
        {
            Duration = 0;

            int[] sinParameters = new int[] { 0, 0, 0 };
            for (int i = 0; i < waveForm_generated.Count; i++)
            {
                if (waveForm_generated[i].Length > 3) // Sinus
                {
                    sinParameters[0] = (int)waveForm_generated[i][3]; // loops
                    sinParameters[1] = (int)waveForm_generated[i][4]; // start
                    sinParameters[2] = (int)waveForm_generated[i][5]; // length
                }
            }

            for (int i = 0; i < sinParameters[1]; i++) // Werte von Block 0
                Duration += waveForm_generated[i][2];
            for (int i = 0; i < sinParameters[0]; i++)
            { // Werte der bisherigen repetitions
                for (int k = sinParameters[1]; k < sinParameters[1] + sinParameters[2]; k++)
                    Duration += waveForm_generated[k][2];
            }
            for (int i = sinParameters[1] + sinParameters[2]; i <= waveForm_generated.Count - 1; i++)
            { //aktueller Wert Block 2
                Duration += waveForm_generated[i][2];
            }

            return Duration;
        }


        static List<string[]> createScpiCommands(List<double[]> waveForm_generated)
        {
            var commandArray = new List<string[]>();

            int[] sinParameters = new int[] { 0, 0, 0 };

            string voltList = "";
            string currList = "";
            string dwelList = "";

            var culture = System.Globalization.CultureInfo.GetCultureInfo("en-GB");

            // INIT
            commandArray.Add(new string[1] { ";SYST:REM" });
            commandArray.Add(new string[1] { ";*CLS" });
            commandArray.Add(new string[1] { "SYST:LANG CIIL" });
            commandArray.Add(new string[1] { "LIST:SEQ:STAT OFF" });
            commandArray.Add(new string[1] { "LIST:SEQ:OPEN:MODE NORM" });
            commandArray.Add(new string[1] { "LIST:SEQ:TERM FIRS" });
            commandArray.Add(new string[1] { "CURR:LEV MAX" });
            commandArray.Add(new string[2] { "SYST:ERR?", "0,\"No error\"\r\n" });

            // Spannungskurve
            voltList = "LIST:VOLT 0";
            currList = "LIST:CURR 0";
            dwelList = "LIST:DWEL 0";
            for (int i = 0; i < waveForm_generated.Count; i++)
            {
                if (((i % 50) == 0) && (i > 0))
                {
                    commandArray.Add(new string[2] { voltList + ";*OPC?", "1\r\n" });
                    commandArray.Add(new string[2] { currList + ";*OPC?", "1\r\n" });
                    commandArray.Add(new string[2] { dwelList + ";*OPC?", "1\r\n" });
                    voltList = "LIST:VOLT " + i;
                    currList = "LIST:CURR " + i;
                    dwelList = "LIST:DWEL " + i;
                }
                voltList += "," + String.Format(culture, "{0:0.000}", waveForm_generated[i][0]);
                currList += "," + String.Format(culture, "{0:0.000}", waveForm_generated[i][1]);
                dwelList += "," + String.Format(culture, "{0:0.000}", waveForm_generated[i][2]);

                if (waveForm_generated[i].Length > 3) // Sinus
                {
                    sinParameters[0] = (int)waveForm_generated[i][3]; // loops
                    sinParameters[1] = (int)waveForm_generated[i][4]; // start
                    sinParameters[2] = (int)waveForm_generated[i][5]; // length
                }
            }
            commandArray.Add(new string[2] { voltList + ";*OPC?", "1\r\n" });
            commandArray.Add(new string[2] { currList + ";*OPC?", "1\r\n" });
            commandArray.Add(new string[2] { dwelList + ";*OPC?", "1\r\n" });

            if ((sinParameters[1] != 0) || (sinParameters[2] != 0)) // Sinus Block wiederholungen
            {
                commandArray.Add(new string[1] { "LIST:SEQ:BLOC 2" });
                commandArray.Add(new string[1] { "LIST:BLOC 0,0," + (sinParameters[1] - 1).ToString() + ",1" });
                commandArray.Add(new string[1] { "LIST:BLOC 1," + (sinParameters[1]).ToString() + "," + (sinParameters[1] + sinParameters[2] - 1).ToString() + "," + (sinParameters[0]).ToString() });
                commandArray.Add(new string[1] { "LIST:BLOC 2," + (sinParameters[1] + sinParameters[2]).ToString() + "," + (waveForm_generated.Count - 1).ToString() + ",1" });
            }
            else
            {
                commandArray.Add(new string[1] { "LIST:SEQ:BLOC 0" });
                commandArray.Add(new string[1] { "LIST:BLOC 0,0," + (waveForm_generated.Count - 1).ToString() + ",1" });
            }
            commandArray.Add(new string[2] { "SYST:ERR?", "0,\"No error\"\r\n" });


            return commandArray;
        }

        void statusTracking(List<double[]> waveForm_generated)
        {
            backgroundWorker1.RunWorkerAsync();//this invokes the DoWork event
        }

        List<string> communicate(List<string[]> commandArray)
        {
            var responseArray = new List<string>();
            byte[] receiveBuffer = new byte[100];

            while (EthBusy)
                Thread.Sleep(1);

            try
            {
                ASCIIEncoding asen = new ASCIIEncoding();
                EthBusy = true;
                for (int i = 0; i < commandArray.Count; i++)
                {
                    byte[] ba = asen.GetBytes(commandArray[i][0] + "\r\n");
                    Stm.Write(ba, 0, ba.Length); // WRITE COMMANDS 

                    if (commandArray[i].Length > 1)
                    {
                        int k = Stm.Read(receiveBuffer, 0, 100); // READ Response 
                        responseArray.Add(Encoding.ASCII.GetString(receiveBuffer, 0, k));
                    }
                }
                EthBusy = false;
            }

            catch (Exception e)
            {
                EthBusy = false;
                ModuleState = PowerSupplyState.Disconnected;
                Debug.WriteLine($"Power supply TCP Error.....Trace: { e.StackTrace}");

                throw new PowerSupplyNotReadyException($"Netzteil TCP Error..... " );

            }

            return responseArray;
        }

        public void Connect(string ip, int port)
        {
            if (ModuleState != PowerSupplyState.Disconnected)
            {
                throw new PowerSupplyNotReadyException(
                    $"Netzteil kann nicht connected werden. Aktuelle Status: {ModuleState}. Disconnect first.");
            }

            try
            {
                Tcpclnt = new TcpClient();
                Tcpclnt.Connect(ip, port);
                Stm = Tcpclnt.GetStream();
                Stm.ReadTimeout = 1000;
            }

            catch (Exception)
            {
               throw new PowerSupplyConnectionFailedException(
                    $"Netzteil TCP Error.....");
            }

            ModuleState = PowerSupplyState.Connected;
        }

        void disconnect()
        {
            while (EthBusy)
                Thread.Sleep(1);

            try
            {
                Stm.Close();
                Tcpclnt.Close();
            }

            catch (Exception)
            {
                throw new PowerSupplyConnectionFailedException(
                    $"Netzteil TCP Error.....");
            }
            ModuleState = PowerSupplyState.Disconnected;
        }

        void startSequence()
        {
            var commandArray = new List<string[]>();

            commandArray.Add(new string[1] { "TRIG:SOUR BUS" });
            commandArray.Add(new string[1] { "INIT:CONT OFF" });
            commandArray.Add(new string[1] { "LIST:SEQ:STAT ON" });
            commandArray.Add(new string[1] { "LIST:SEQ:CLE" });
            commandArray.Add(new string[1] { "INIT" });
            commandArray.Add(new string[1] { "OUTP ON" });
            commandArray.Add(new string[1] { "*TRG" });

            communicate(commandArray);
        }

        List<string> getInfo()
        {
            var commandArray = new List<string[]>();

            commandArray.Add(new string[1] { "LIST:SEQ:STAT OFF" });
            commandArray.Add(new string[2] { "*IDN?", "" });
            commandArray.Add(new string[2] { "CURR? MAX", "" });
            commandArray.Add(new string[2] { "VOLT? MAX", "" });
            commandArray.Add(new string[2] { "SYST:ERR?", "0,\"No error\"\r\n" });

            var responseArray = communicate(commandArray);

            return responseArray;
        }

        public List<string> getInfo_1()
        {
            var commandArray = new List<string[]>();

            commandArray.Add(new string[1] { "LIST:SEQ:STAT OFF" });
            commandArray.Add(new string[2] { "*IDN?", "" });
            commandArray.Add(new string[2] { "CURR? MAX", "" });
            commandArray.Add(new string[2] { "VOLT? MAX", "" });
            commandArray.Add(new string[2] { "SYST:ERR?", "0,\"No error\"\r\n" });

            var responseArray = communicate(commandArray);

            return responseArray;
        }

        /// <summary>
        /// Set constante voltage in power supply 
        /// </summary>
        /// <param name="voltage">voltage to be set in power supply</param>
        public void SetVoltage(double voltage)
        {
            PowerSupplySetedVoltage settings = new PowerSupplySetedVoltage();

            if (ModuleState != PowerSupplyState.Connected)
            {
                throw new PowerSupplyNotReadyException(
                    $"Netzteil ist inm Status: {ModuleState}. Connect first.", ModuleState);
            }

            var commandArray = new List<string[]>();
            var culture = System.Globalization.CultureInfo.GetCultureInfo("en-GB");

            commandArray.Add(new string[1] { "LIST:SEQ:STAT OFF" });
            commandArray.Add(new string[1] { "VOLT " + String.Format(culture, "{0:0.000}", voltage) });

            communicate(commandArray);

            settings.voltage = voltage;
            settings.duration = Duration;

            OnPowerSupplySetVoltage(settings);
        }

        /// <summary>
        /// SME: Set Current.
        /// </summary>
        /// <param name="obj"></param>
        public void SetCurrent(double current)
        {
            if (ModuleState != PowerSupplyState.Connected)
            {
                throw new PowerSupplyNotReadyException(
                    $"Netzteil ist im Status {ModuleState}. Connect first.", ModuleState);
            }

            var commandArray = new List<string[]>();
            var culture = System.Globalization.CultureInfo.GetCultureInfo("en-GB");

            commandArray.Add(new string[1] { "LIST:SEQ:STAT OFF" });
            commandArray.Add(new string[1] { "CURR " + String.Format(culture, "{0:0.000}", current) });

            communicate(commandArray);
        }

        public void setOutput(bool status)
        {
            if (ModuleState != PowerSupplyState.Connected)
            {
                throw new PowerSupplyNotReadyException(
                    $"Netzteil ist im Status { ModuleState}. Connect first.", ModuleState);
            }

            var commandArray = new List<string[]>();

            commandArray.Add(new string[1] { "LIST:SEQ:STAT OFF" });
            if (status == true)
            {
                commandArray.Add(new string[1] { "OUTP ON" });
                ModuleState = PowerSupplyState.Connected;
            }                
            else
            {
                commandArray.Add(new string[1] { "OUTP OFF" });
                ModuleState = PowerSupplyState.Connected;
            }

            communicate(commandArray);

            
        }

        private void backgroundWorker1_DoWork(object sender, DoWorkEventArgs e)
        {

            if (StatusTrackingActive)
            {
                var commandArray = new List<string[]>();
                commandArray.Add(new string[2] { "STAT:OPER:COND?", "" });
                commandArray.Add(new string[2] { "LIST:SEQ?", "" });
                commandArray.Add(new string[2] { "MEAS:VOLT?", "" });
                commandArray.Add(new string[2] { "MEAS:CURR?", "" });
                List<string> responseArray = communicate(commandArray);
                e.Result = responseArray;
            }
            // string str = "0.01"; // textBox8.Text;
            //int delay = (int)(Convert.ToDouble(str.Replace(".", ",")) * 1000);
            int delay = 10;
            Thread.Sleep(delay);

        }

        private void backgroundWorker1_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
        {
            if (e.Error != null)// First, handle the case where an exception was thrown.
            {
                throw new PowerSupplyBackgroundWorkerException(e.Error.Message);
            }
            else if (e.Cancelled) // Next, handle the case where the user canceled the operation.
            {// Note that due to a race condition in the DoWork event handler, the Cancelled flag may not have been set, even though CancelAsync was called.
                throw new PowerSupplyBackgroundWorkerException("Operation canceled by user"); //MessageBox.Show("Canceled");
            }
            else // Finally, handle the case where the operation succeeded.
            {
                List<string> responseArray = e.Result as List<string>;

                if (e.Result == null)
                    return;
                else if (responseArray.Count == 0)
                    return;

                var culture = System.Globalization.CultureInfo.GetCultureInfo("en-GB");

                int[] sinParameters = new int[] { 0, 0, 0 };
                for (int i = 0; i < waveForm_generated.Count; i++)
                {
                    if (waveForm_generated[i].Length > 3) // Sinus
                    {
                        sinParameters[0] = (int)waveForm_generated[i][3]; // loops
                        sinParameters[1] = (int)waveForm_generated[i][4]; // start
                        sinParameters[2] = (int)waveForm_generated[i][5]; // length
                    }
                }

                if (responseArray[0] != "00008\r\n")
                { 
                    StatusTrackingActive = false;
                    Debug.WriteLine("backgroundWorker1_RunWorkerCompleted ModuleState: " + ModuleState);
                    ModuleState = PowerSupplyState.Connected;
                    OnTestFinishedEvent(new EventArgs());
                }
                else if (responseArray.Count < 2)
                    return;
                else if (responseArray.Count > 1)
                {
                    String[] elements = responseArray[1].Split(','); // Response:  2,067,00001 = Block, Position, Block Loop
                    int block = Convert.ToInt32(elements[0]);
                    int position = Convert.ToInt32(elements[1]);
                    int blockLoop = Convert.ToInt32(elements[2]);

                    double currentTime = 0;

                  //  Debug.WriteLine("backgroundWorker1_RunWorkerCompleted currentTime: " + currentTime);
                    if (block == 0)
                    { // Block 0 = vor einer Sinuskurve
                        for (int i = 0; i < position; i++)
                            currentTime += waveForm_generated[i][2];
 //                       Debug.WriteLine("backgroundWorker1_RunWorkerCompleted currentTime: " + currentTime + " block:" + block);
                    }
                    else if (block == 1)
                    {
                   //     Debug.WriteLine("backgroundWorker1_RunWorkerCompleted currentTime: " + currentTime + " block:" + block);
                        // Block 1 = Sinuskurve die mehrfach durchlaufen wird
                        for (int i = 0; i < sinParameters[1]; i++) // Werte von Block 0
                            currentTime += waveForm_generated[i][2];
                        for (int i = 0; i < blockLoop - 1; i++)
                        { // Werte der bisherigen repetitions
                            for (int k = sinParameters[1]; k < sinParameters[1] + sinParameters[2]; k++)
                                currentTime += waveForm_generated[k][2];
                        }
                        for (int k = sinParameters[1]; k < position; k++)
                        { //Wert der aktuellen repetition
                            currentTime += waveForm_generated[k][2];
                        }
                    }
                    else if (block == 2)
                    {
                //        Debug.WriteLine("backgroundWorker1_RunWorkerCompleted currentTime: " + currentTime + " block:" + block);
                        // Block 2 = nach einer Sinuskurve
                        for (int i = 0; i < sinParameters[1]; i++) // Werte von Block 0
                            currentTime += waveForm_generated[i][2];
                        for (int i = 0; i < sinParameters[0]; i++)
                        { // Sinus
                            for (int k = sinParameters[1]; k < sinParameters[1] + sinParameters[2]; k++)
                                currentTime += waveForm_generated[k][2];
                        }
                        for (int i = sinParameters[1] + sinParameters[2]; i <= position; i++)
                        { //aktueller Wert Block 2
                            currentTime += waveForm_generated[i][2];
                        }
                    }

                    int pos = (int)(currentTime / Duration * Points.Count);
                    //setMarkerPosition(pos);

                    double voltageResponse = 0.0;
                    double currentResponse = 0.0;
                    if(responseArray.Count > 3)
                    {
                        bool success;

                        success = Double.TryParse(responseArray[2], out voltageResponse);
                        success &= Double.TryParse(responseArray[3], out currentResponse);

                        if(!success)
                        {
                            Debug.WriteLine($"Warning: Could not get voltage or current!");
                        }
                    }

                    // send update event
                    // OnPowerSupplyUpdate(pos);
                    progress.pos = pos;
                    progress.time = currentTime;
                    progress.voltage = voltageResponse/100;
                    progress.current = currentResponse/1000;

                    OnPowerSupplyUpdate(progress);
                }
            }
            if (StatusTrackingActive == true)
                backgroundWorker1.RunWorkerAsync();
            else
                backgroundWorker1.CancelAsync();
        }


        private void backgroundWorker2_DoWork(object sender, DoWorkEventArgs e)
        {           
            int delay = 1000;
            Thread.Sleep(delay);
        }

        private void backgroundWorker2_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
        {
            if (e.Error != null)// First, handle the case where an exception was thrown.
            {
                throw new PowerSupplyBackgroundWorkerException(e.Error.Message);
            }
            else if (e.Cancelled) // Next, handle the case where the user canceled the operation.
            {// Note that due to a race condition in the DoWork event handler, the Cancelled flag may not have been set, even though CancelAsync was called.
                throw new PowerSupplyBackgroundWorkerException("Operation canceled by user"); 
            }
            else // Finally, handle the case where the operation succeeded.
            {

                CurrentPos++;
                progress.pos = CurrentPos;
                progress.time = CurrentPos;
                progress.voltage = GlobalVoltage;
                OnPowerSupplyUpdate(progress);

            }

            if (StatusTrackingActive == true)
                backgroundWorker2.RunWorkerAsync();
            else
                backgroundWorker2.CancelAsync();
        }


        /// <summary>
        /// SelectFile Power Select file.
        /// </summary>
        /// <param name="obj"></param>
        public List<DataPoint> SelectFile(string filename)
        {
            MaxCurrent = 20;
            MaxVolt = 32;
            List<float[]> waveFormArray = loadWaveForm(filename);

            waveForm_generated = calculateWaveForm(waveFormArray);
            // int maxPoints = Convert.ToInt32(textBox9.Text.Replace(".", ","));

            //if (waveForm_generated.Count > maxPoints)
            //    MessageBox.Show("ERROR - zu viele Punkte");

        //    ModuleState = PowerSupplyState.FileSelected;
            return createChart(waveForm_generated);
        }

        /// <summary>
        /// Upload curve to power supply.
        /// </summary>
        /// <param name="obj"></param>
        public void Upload()
        {
            
            if (waveForm_generated == null || waveForm_generated.Count == 0)
            {
                throw new PowerSupplyNotReadyException("Spannungskurve Datei existiert nicht oder ist beschädigt");
            }

            var responseArray = getInfo();

            if (responseArray.Count == 0)
            {
                throw new PowerSupplyNotReadyException("Netzteil antwortet nicht.");
            }

            if (MaxCurrent == 0)
            {
                throw new PowerSupplyNotReadyException("Max current ist 0.");
            }
            else
            {
                var commandArray = createScpiCommands(waveForm_generated);
                communicate(commandArray);
            }

        }


        /// <summary>
        /// Start voltage curve test
        /// </summary>
        public void StartCurveTest()
        {
            if (StatusTrackingActive)
                return;

            startSequence();
            StatusTrackingActive = true;
            statusTracking(waveForm_generated);

            _currentTest = TestType.CurveTest;
            ModuleState = PowerSupplyState.TestRunning;
        }

        /// <summary>
        /// SME: Spannungscurventest starten.
        /// </summary>
        /// <param name="obj"></param>
        public void StartConstantTest(double voltage, double duration)
        {
            if (StatusTrackingActive)
                return;

            StatusTrackingActive = true;

            Duration = duration;
            CurrentPos = 0;

            Points.Clear();

            for(int i = 0; i< duration; i++)
            {
                Points.Add(new DataPoint(i,voltage));
            }

            SetVoltage(voltage);
            GlobalVoltage = voltage;
            backgroundWorker2.RunWorkerAsync();//this invokes the DoWork event

            _currentTest = TestType.ConstantVoltageTest;
            ModuleState = PowerSupplyState.TestRunning;
        }

        /// <summary>
        /// SME: Disconnect Power Select file.
        /// </summary>
        /// <param name="obj"></param>
        public void Disconnect()
        {
            if (StatusTrackingActive)
            {
                StatusTrackingActive = false;
                backgroundWorker1.CancelAsync();
                backgroundWorker2.CancelAsync();
                var commandArray = new List<string[]>();
                commandArray.Add(new string[1] { "LIST:SEQ:STAT OFF" });
                communicate(commandArray);
            }

            disconnect();

        }

        public void FinishTest()
        {
            if (ModuleState != PowerSupplyState.TestRunning )
            {
                return;
            }

            StatusTrackingActive = false;

            if (_currentTest == TestType.ConstantVoltageTest )
            {
                Duration = 0;                
                backgroundWorker2.CancelAsync();

            }
            else if(_currentTest == TestType.CurveTest)
            {
                backgroundWorker1.CancelAsync();
                backgroundWorker2.CancelAsync();
                var commandArray = new List<string[]>();
                commandArray.Add(new string[1] { "LIST:SEQ:STAT OFF" });
                communicate(commandArray);
            }

            _currentTest = TestType.NoTest;
            ModuleState = PowerSupplyState.Connected;
            OnTestFinishedEvent(new EventArgs());
        }

        public void Dispose()
        {
            backgroundWorker1.Dispose();
            backgroundWorker2.Dispose();
        }

        public class PowerSupplyCurrentProgress
        {
            public int pos { get; set; }
            public double time { get; set; }
            public double voltage { get; set; }
            public double current { get; set; }

        }

        public class PowerSupplySetedVoltage
        {
            public double voltage { get; set; }
            public double duration { get; set; }

        }
    }
}