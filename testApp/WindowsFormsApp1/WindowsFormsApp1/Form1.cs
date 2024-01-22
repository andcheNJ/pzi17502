using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Ediabas;
using System.Diagnostics;
using System.Threading;
using DiagnosticModule;
using System.IO;
using System.Configuration;
using System.Collections.Specialized;
using System.Xml;
using TestControl;
using PowerSupplyModule;
using System.Xml.Linq;
using DocumentFormat.OpenXml.Drawing;
using DocumentFormat.OpenXml.Drawing.Charts;


namespace WindowsFormsApp1
{
    public partial class Form1 : Form
    {
        private string _huSgbd ;
        //       private const string _huSgbd = "MGU_02_L";
        //        private const string _huSgbd = "HU_02_A";
       //             private const string _huSgbd = "NBTEVO";
        //        private const string _huSgbd = "ENAVEVO";
//        private const string _huSgbd = "RSE022CR";
        private const string JobSteuern = "steuern";
        const string genericJob = "steuern_cid_generisch";
//        const string genericJob = "steuern_display_generisch";    // PaDi
        private string brightness;
        private string testPic;
        private string val;
        private string val1;
        private string val2;
        private string newVal;
        private string ECU;
        private string ECU1;
        private string PWF_Job;
        private string supplier;
        private int wohnen;
        private int parken;
        private int PAD;
        private int osdStart;
        private int offset;
        private double volt = 12;
        private string xmlPath = @"E:\Scripts\testApp\WindowsFormsApp1\Config.xml";
        private string xmlPath1 = @"E:\Scripts\testApp\WindowsFormsApp1\DiagnoseJobs.xml";
        private string resultPath = @"E:\TestResults";
        string pythonEngine;
        string pythonArguements;
        private string filePath = string.Empty;



        EdiabasSingleton es = new EdiabasSingleton();
        XmlDocument doc = new XmlDocument();
        //Excel ex = new Excel(@"C:\Users\Andrew\imageMatching\excelFiles\Analysis.xlsx", 1);
        //Excel ex1 = new Excel(@"Analysis1.xlsx", 1);
       PowerSupply ps = PowerSupply.Instance;
       XElement elem = XElement.Parse("<xml><LOCATION><P>Value1</P></LOCATION><ACCEPTED_VARIANTES VALUE=\"Value2\"/><PERIOD_DAY>Value3</PERIOD_DAY><AWARD_CRITERIA_DETAIL><Value4/></AWARD_CRITERIA_DETAIL></xml>");


        Testrack_Control.Main tc = new Testrack_Control.Main();


        public Form1()
        {
            InitializeComponent();
            //Console.SetOut(new TextBoxStreamWriter(richTextBox5));
            Console.SetOut(new RichTextBoxWriter(richTextBox5));
        }

        private void button1_Click(object sender, EventArgs e)
        {

            //      Init();


            if (API.apiInit())    // API initialisieren

            {
                //               API.apiJobData("TMODE", "HOLE_INTERFACE_STATUS");
                es.Job(_huSgbd, genericJob, "00032E0101"); // turn on touch indicator 
                int millisec = 5000;
                Thread.Sleep(millisec);



                for (int i = 0; i < 101; i++)
                {
                    string st = "ARG;CID_BACKLIGHT;";
                    brightness = string.Concat(st, i);
                    es.Job(_huSgbd, JobSteuern, brightness);
                    int milliseconds = 2000;
                    Thread.Sleep(milliseconds);
                }
               es.Job(_huSgbd, genericJob, "00032E0100"); // turn off touch indicator
                API.apiEnd();           // API beenden

            }

        }

        private void button2_Click(object sender, EventArgs e)
        {
            if (API.apiInit())    // API initialisieren
              
            {

                for (int i = 1; i < 24; i++)
                {
                    string st = "arg;testbild_erweitert;";    //MGU
//                    string st = "arg;steuern_testbild_erweitert;";   //NBTEVO
                    string hexVal = i.ToString("X");
                    string s = "0x0";
                    string hexVal1 = string.Concat(s, hexVal);
                    testPic = string.Concat(st, hexVal1);
                    es.Job(_huSgbd, JobSteuern, testPic);
                    int milliseconds = 5000;
                    Thread.Sleep(milliseconds);
                }
                es.Job(_huSgbd, JobSteuern, "arg;steuern_testbild_erweitert;0x00");

                API.apiEnd();           // API beenden

            }
        }

        private void button3_Click(object sender, EventArgs e)
        {
            //          tc.Open_Com_port("COM4");
            //                tc.Send_cmd(1, 8, 15);
            //          tc.Toggle_Klemmen();
         //
         //
//         ps.Connect("10.64.71.99", 5025);

            if (API.apiInit())    // API initialisieren

            {
//                for (int i = 1; i < 6; i++)
 //               {
//                                    es.Job(_huSgbd, "fs_lesen", "");
//
                  es.Job(_huSgbd, "sensoren_ident_lesen", "");
//                es.Job(_huSgbd, "status_lesen", "ARG;DISPLAY_DETAIL_INFORMATION_EXTENDED");


                //               ConradRelaycard.Send_cmd(Address_Byte, Command_Byte, Data_byte);
                //                                 tc.Open_Com_port("COM4");
                //                                 tc.Toggle_Klemmen();      //toggle on and off
                //                  int milliseconds = 20000;                // delay
                //                 Thread.Sleep(milliseconds);

                //                                   tc.Send_cmd_1(1, 8, 15);


               es.results();
   //             es.WriteExcel();
   //             }

                API.apiEnd();           // API beenden

            }

        }

        private void button4_Click(object sender, EventArgs e)
        {

            //           Console.Write("Enter arguement: ");
            val = richTextBox1.Text;

            if (API.apiInit())    // API initialisieren

            {



                es.Job(_huSgbd, genericJob, val);
                es.results();


                API.apiEnd();           // API beenden

            }

        }



        private void richTextBox1_TextChanged(object sender, EventArgs e)
        {

        }







        private void button5_Click(object sender, EventArgs e)
        {





//                        int osdStart = 0x017F4360;              // OSD Digits Start Address MLC
//                          int osdStart = 0x017F7AB0; // LGE 
                        int osdStart = 0x017D7000;  //Conti
          //              int osdStart = 0x017D9A10;   //INX
 //           int osdStart = 0x017D6EB0;     // LG AZVGE Mid
//            int offset = 16;
            int offset = 28; //Conti
            if (API.apiInit())    // API initialisieren

                es.Job(_huSgbd, genericJob, "000b2e020002c00002017CA000");      // OSD Config Start Address
            int milliseconds = 5000;
            Thread.Sleep(milliseconds);

            for (int i = 1; i < 77; i++)
                {
                    string st = "000b2e020002c000020";
                   
                    string hexVal = osdStart.ToString("X");

                    string genVal = string.Concat(st, hexVal);


                    es.Job(_huSgbd, genericJob, genVal);

//                    int milliseconds = 5000;
                    Thread.Sleep(milliseconds);
                    osdStart += offset;
                }

            API.apiEnd();           // API beenden

        }

        private void button6_Click(object sender, EventArgs e)
        {

//          int ramStart = 0x00200000;                // nbt and mgu18
          int ramStart = 0x00300000;              // new mgu21

            int offset = 4;
            if (API.apiInit())    // API initialisieren

//                es.str = null;

            {
                for (int i = 1; i < 25; i++)
                {
                    string st = "0007220200";
//                    string st = "06220200";                    // PaDi
                    string two = "02";
                    
                    string hexVal = ramStart.ToString("X");
                    string oneVal = string.Concat(st, hexVal);
                    string flashVal = string.Concat(oneVal, two);
                    
                    es.Job(_huSgbd, genericJob, flashVal);
                    es.results();

                    int milliseconds = 10000;
                    Thread.Sleep(milliseconds);
                    ramStart += offset;

                }
                //ex.WriteRange(1, 1, 1000, 1000, es.str);

                //ex.SaveAs(@"test4.xlsx");
                //ex.Close();
                API.apiEnd();           // API beenden

            }

        }

        private void button7_Click(object sender, EventArgs e)
        {
 //           int flashStart = 0x017F4000;
            int flashStart = 0x017F7000;    // PaDi
            int offset = 4;
            if (API.apiInit())    // API initialisieren

            {
                for (int i = 1; i < 10; i++)
                {
 //                   string st = "0008220300010";
                    string st = "0622020";                    // PaDi
                    string two = "02";                          //PaDi


//                    string hexVal = flashStart.ToString("X");                    
//                    string flashVal = string.Concat(st, hexVal);

                    string hexVal = flashStart.ToString("X");
                    string oneVal = string.Concat(st, hexVal);
                    string flashVal = string.Concat(oneVal, two);


                    es.Job(_huSgbd, genericJob, flashVal);
                    es.results();

                    int milliseconds = 10000;
                    Thread.Sleep(milliseconds);
                    flashStart += offset;
                }

                API.apiEnd();           // API beenden

            }

            //ex.WriteRange(1, 1, 1000, 1000, es.str1);

            //ex.SaveAs(@"test5.xlsx");
            //ex.Close();
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void button8_Click(object sender, EventArgs e)
        {
            doc.Load("diagnosisParameters.xml");
            val = textBox1.Text;
            int number = 0;


            if (API.apiInit())    // API initialisieren

            {

               foreach(XmlNode node in doc.DocumentElement)
                {
                    string name = node.Attributes[0].InnerText;

              
                        if (val != null && val.Length >= 3)
                        {
                            if (val == name)
                            {
                                number = node.ChildNodes.Count;
                                Console.WriteLine("number is : {0}", number);

                                if (number < 4)
                                {
                                    es.Job(_huSgbd, node.ChildNodes[0].InnerText, node.ChildNodes[1].InnerText);
                                    es.results();
                                }
                                else
                                {
                                    for (int i = 2; i < number; i++)
                                    {
                                        es.Job(_huSgbd, node.ChildNodes[0].InnerText, node.ChildNodes[1].InnerText + ";" + node.ChildNodes[i].InnerText);
                                        //               es.results();
                                        int milliseconds = 5000;
                                        Thread.Sleep(milliseconds);
                                    }
                                }

                            }
                            else
                            {
                                Console.Write("Job not found.");
                            }
                        }
                        else
                        {

                            MessageBox.Show("Invalid Input");
                            break;
                        }
                    
                }

               

                API.apiEnd();           // API beenden

            }
        }

        private void button9_Click(object sender, EventArgs e)
        {
            //char ch;
            //int Tchar = 0;
            //int row = 0;
            //int x = 1;
            //string[] s = new string[100000];
            ////            object[,] arr = new object[1000, 1];
            //string[,] str = new string[100000, 1];
            //StreamReader reader;
            //reader = new StreamReader(@"C:\Binary.txt");

//            ps.Connect("10.64.71.99", 5025);
            ps.SetVoltage(volt + 0.1);
            volt = volt + 0.1;
            textBox3.Text = (volt + "V");
            //            do
            //            {
            //                ch = (char)reader.Read();
            ////                Console.WriteLine(ch);
            //                if (Convert.ToInt32(ch) != 32)
            //                {
            //                    Console.Write(ch);
            //                    str[row, 0] = ch.ToString();
            //                    //                    row ++;
            //                }
            // //                              str[row, 0] = ch.ToString();


            //                Tchar++;
            //                row++;
            //                x++;
            //                s[row] = ch.ToString();
            //            } while (!reader.EndOfStream);

            //            ex.WriteRange(1,1,1000,1 ,str);
            //            reader.Close();
            //            reader.Dispose();
            //            Console.WriteLine(" ");
            //            Console.WriteLine(Tchar.ToString() + " characters");
            //            Console.ReadLine();
            ////            ex.Save();
            //            ex.SaveAs(@"C:\Tst.xlsx");
            //            ex.Close();
        }

        private void button10_Click(object sender, EventArgs e)
        {
            doc.Load("diagnosisParameters.xml");
            //string diagJob;
            int number = 0;
                        string st = "4.2.";         //MGU
          //              string st = "4.2a.";     //entryEvo

            for (int i = 1; i < 15; i++)
            {

            val = string.Concat(st, i.ToString());

                if (API.apiInit())    // API initialisieren

                {

                    foreach (XmlNode node in doc.DocumentElement)
                    {
                        string name = node.Attributes[0].InnerText;


                        if (val != null && val.Length >= 3)
                        {
                            if (val == name)
                            {
                                number = node.ChildNodes.Count;
                                Console.WriteLine("number is : {0}", number);

                                if (number < 4)
                                {
                                    es.Job(_huSgbd, node.ChildNodes[0].InnerText, node.ChildNodes[1].InnerText);
                                    es.results();
                                    int milliseconds = 5000;
                                    Thread.Sleep(milliseconds);
                                }
                                else
                                {
                                    for (int j = 2; j < number; j++)
                                    {
                                        es.Job(_huSgbd, node.ChildNodes[0].InnerText, node.ChildNodes[1].InnerText + ";" + node.ChildNodes[j].InnerText);
                                        //               es.results();
                                        int milliseconds = 5000;
                                        Thread.Sleep(milliseconds);
                                    }
                                }

                            }
                            //else
                            //{
                            //    Console.Write("Job not found.");
                            //}
                        }
                        else
                        {

                            MessageBox.Show("Invalid Input");
                            break;
                        }

                    }


            

                    API.apiEnd();           // API beenden

                }
            }

            //ex.WriteRange(1, 1, 1000, 1000, es.str1);

            //ex.SaveAs(@"test3.xlsx");
            //ex.Close();

        }

        private void textBox3_TextChanged(object sender, EventArgs e)
        {

        }

        private void button11_Click(object sender, EventArgs e)
        {
 //             ps.Connect("10.64.71.99", 5025 );
              ps.SetVoltage(volt - 0.1);
              volt = volt - 0.1;
              textBox3.Text = (volt + "V");
        }

        private void button12_Click(object sender, EventArgs e)
        {

            val = richTextBox2.Text;
            val1 = richTextBox3.Text;
            val2 = richTextBox4.Text;


            es.ModifyXmlFile(xmlPath, val1,val2, val);
            label1.Text = es.getXmlVal(xmlPath, val1, Int32.Parse(val2));

        }

        private void label1_Click(object sender, EventArgs e)
        {
           
        }

        private void richTextBox2_TextChanged(object sender, EventArgs e)
        {

        }

        private void richTextBox3_TextChanged(object sender, EventArgs e)
        {

        }

        private void button13_Click(object sender, EventArgs e)
        {
            val1 = richTextBox3.Text;
            val2 = richTextBox4.Text;

            label1.Text = es.getXmlVal(xmlPath, val1, Int32.Parse(val2));

        }

        private void button14_Click(object sender, EventArgs e)
        {
            string s = @"C:\Users\njuguna.PZI15922\Documents\scripts\search2.py";
            string r = @"search2.add(2,3)";
            Debug.WriteLine(es.Run_cmd(s, r));
            MessageBox.Show(es.Run_cmd(s, r) + "Done");      

        }

        private void richTextBox4_TextChanged(object sender, EventArgs e)
        {

        }

        private void tabPage1_Click(object sender, EventArgs e)
        {

        }

        private void button14_Click_1(object sender, EventArgs e)
        {
            ECU = comboBox1.Text;

            switch (ECU)
            {
                case "MGU18":
                    wohnen = 33;
                    parken = 21;
                    PAD = 35;
                    
                    break;
                case "MGU21":
                    wohnen = 24;
                    parken = 22;
                    PAD = 26;

                    break;
                case "MGU22":
                    wohnen = 42;
                    parken = 23;
                    PAD = 44;

                    break;
                case "IDC23":
                    wohnen = 30;
                    parken = 24;
                    PAD = 32;

                    break;
                case "ICBox":
                    wohnen = 27;
                    parken = 27;
                    PAD = 29;

                    break;
                case "NBTEvo":
                    wohnen = 36;
                    parken = 25;
                    PAD = 38;

                    break;
                case "EntryEvo":
                    wohnen = 39;
                    parken = 26;
                    PAD = 41;

                    break;
            }
            
            string phrase = es.getXmlVal(xmlPath1, "string", wohnen);
            string[] words = phrase.Split(';');
            int displayVal = Int32.Parse(words[1])/1000;
            label6.Text = displayVal.ToString() + " Seconds";
            int displayVal2 = Int32.Parse(es.getXmlVal(xmlPath, "Value", parken))/1000;
            label7.Text = displayVal2.ToString() + " Seconds";
            string phrase1 = es.getXmlVal(xmlPath1, "string", PAD);
            string[] words1 = phrase1.Split(';');
            int displayVal1 = Int32.Parse(words1[1]) / 1000;
            label8.Text  = displayVal1.ToString() + " Seconds";



        }
        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void label3_Click(object sender, EventArgs e)
        {

        }

        private void label8_Click(object sender, EventArgs e)
        {

        }

        private void label1_Click_1(object sender, EventArgs e)
        {

        }

        private void button13_Click_1(object sender, EventArgs e)
        {
            val1 = richTextBox3.Text;
            val2 = richTextBox4.Text;
            Debug.Write(val1);
            Debug.Write(val2);

            label1.Text = es.getXmlVal(xmlPath1, val1, Int32.Parse(val2));
        }

        private void richTextBox3_TextChanged_1(object sender, EventArgs e)
        {

        }

        private void richTextBox4_TextChanged_1(object sender, EventArgs e)
        {

        }

        private void richTextBox2_TextChanged_1(object sender, EventArgs e)
        {

        }

        private void button12_Click_1(object sender, EventArgs e)
        {

            val = richTextBox2.Text;
            val1 = richTextBox3.Text;
            val2 = richTextBox4.Text;
            Debug.Write(val);
            Debug.Write(val1);
            Debug.Write(val2);  

            es.ModifyXmlFile(xmlPath, val1,val2, val);
            label1.Text = es.getXmlVal(xmlPath, val1, Int32.Parse(val2));

        }

        private void button1_Click_1(object sender, EventArgs e)
        {
            //      Init();


            if (API.apiInit())    // API initialisieren

            {
                //               API.apiJobData("TMODE", "HOLE_INTERFACE_STATUS");
                es.Job(_huSgbd, genericJob, "00032E0101"); // turn on touch indicator 
                int millisec = 5000;
                Thread.Sleep(millisec);



                for (int i = 0; i < 101; i++)
                {
                    string st = "ARG;CID_BACKLIGHT;";
                    brightness = string.Concat(st, i);
                    es.Job(_huSgbd, JobSteuern, brightness);
                    int milliseconds = 2000;
                    Thread.Sleep(milliseconds);
                }
                es.Job(_huSgbd, genericJob, "00032E0100"); // turn off touch indicator
                API.apiEnd();           // API beenden

            }
        }

        private void button8_Click_1(object sender, EventArgs e)
        {
            doc.Load("diagnosisParameters.xml");
            val = textBox1.Text;
            int number = 0;


            if (API.apiInit())    // API initialisieren

            {

                foreach (XmlNode node in doc.DocumentElement)
                {
                    string name = node.Attributes[0].InnerText;


                    if (val != null && val.Length >= 3)
                    {
                        if (val == name)
                        {
                            number = node.ChildNodes.Count;
                            Console.WriteLine("number is : {0}", number);

                            if (number < 4)
                            {
                                es.Job(_huSgbd, node.ChildNodes[0].InnerText, node.ChildNodes[1].InnerText);
                                es.results();
                            }
                            else
                            {
                                for (int i = 2; i < number; i++)
                                {
                                    es.Job(_huSgbd, node.ChildNodes[0].InnerText, node.ChildNodes[1].InnerText + ";" + node.ChildNodes[i].InnerText);
                                    //               es.results();
                                    int milliseconds = 5000;
                                    Thread.Sleep(milliseconds);
                                }
                            }

                        }
                        else
                        {
                            Console.Write("Job not found.");
                        }
                    }
                    else
                    {

                        MessageBox.Show("Invalid Input");
                        break;
                    }

                }



                API.apiEnd();           // API beenden

            }
        }

        private void button2_Click_1(object sender, EventArgs e)
        {
            string st;
            ECU1 = comboBox2.Text;
            if (API.apiInit())    // API initialisieren

            {

                for (int i = 1; i < 24; i++)
                {
;
                    if (ECU1 == "NBTEvo" | ECU1 == "MGU18")
                    {
                        st = "arg;steuern_testbild_erweitert;";   //NBTEVO
                    }
                    else
                    {
                        st = "arg;testbild_erweitert;";    //MGU              // new mgu21
                    }

                    
                                                              //                    
                    string hexVal = i.ToString("X");
                    string s = "0x0";
                    string hexVal1 = string.Concat(s, hexVal);
                    testPic = string.Concat(st, hexVal1);
                    es.Job(_huSgbd, JobSteuern, testPic);
                    int milliseconds = 5000;
                    Thread.Sleep(milliseconds);
                }
                es.Job(_huSgbd, JobSteuern, "arg;steuern_testbild_erweitert;0x00");

                API.apiEnd();           // API beenden

            }
        }

        private void textBox1_TextChanged_1(object sender, EventArgs e)
        {

        }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {

        }

        private void label6_Click(object sender, EventArgs e)
        {

        }

        private void label7_Click(object sender, EventArgs e)
        {

        }

        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        private void label9_Click(object sender, EventArgs e)
        {

        }

        private void label10_Click(object sender, EventArgs e)
        {

        }

        private void button15_Click(object sender, EventArgs e)
        {
            PWF_Job = comboBox2.Text;
            string inVal = textBox2.Text;
            newVal = (Int32.Parse(inVal) * 1000).ToString();
            string searchTag = "string";
            string searchTag1 = "Value";

            switch (PWF_Job)
            {
                case "Wohnen":
                    
                    string phrase = es.getXmlVal(xmlPath1, searchTag, wohnen);
                    string[] words = phrase.Split(';');
                    string valSet = words[0] + ";" + newVal + ";" + words[2];
                    es.ModifyXmlFile(xmlPath1, searchTag, wohnen.ToString(), valSet);
                    phrase = es.getXmlVal(xmlPath1, searchTag, wohnen);
                    words = phrase.Split(';');
                    int displayVal = Int32.Parse(words[1]) / 1000;
                    label6.Text = displayVal.ToString() + " Seconds";

                    break;
                case "Parken_BN_IO":

                    es.ModifyXmlFile(xmlPath, searchTag1, parken.ToString(), newVal);
                    int displayVal2 = Int32.Parse(es.getXmlVal(xmlPath, searchTag1, parken)) / 1000;
                    label7.Text = displayVal2.ToString() + " Seconds";

                    break;

                case "PrüfenAnalyseDiagnose":

                    string phrase1 = es.getXmlVal(xmlPath1, searchTag, PAD);
                    string[] words1 = phrase1.Split(';');
                    string valSet1 = words1[0] + ";" + newVal + ";" + words1[2];
                    es.ModifyXmlFile(xmlPath1, searchTag, PAD.ToString(), valSet1);
                    phrase1 = es.getXmlVal(xmlPath1, searchTag, PAD);
                    words1 = phrase1.Split(';');
                    int displayVal1 = Int32.Parse(words1[1]) / 1000;
                    label8.Text = displayVal1.ToString() + " Seconds";

                    break;


        }
        }

        private void comboBox2_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        private void textBox2_TextChanged_1(object sender, EventArgs e)
        {

        }

        private void button3_Click_1(object sender, EventArgs e)
        {
            //          tc.Open_Com_port("COM4");
            //                tc.Send_cmd(1, 8, 15);
            //          tc.Toggle_Klemmen();
            //
            //
            //         ps.Connect("10.64.71.99", 5025);

            if (API.apiInit())    // API initialisieren

            {
                //                for (int i = 1; i < 6; i++)
                //               {
                                                    es.Job(_huSgbd, "fs_lesen", "");
                //
                //es.Job(_huSgbd, "sensoren_ident_lesen", "");
                //                es.Job(_huSgbd, "status_lesen", "ARG;DISPLAY_DETAIL_INFORMATION_EXTENDED");


                //               ConradRelaycard.Send_cmd(Address_Byte, Command_Byte, Data_byte);
                //                                 tc.Open_Com_port("COM4");
                //                                 tc.Toggle_Klemmen();      //toggle on and off
                //                  int milliseconds = 20000;                // delay
                //                 Thread.Sleep(milliseconds);

                //                                   tc.Send_cmd_1(1, 8, 15);


                es.results();
                //             es.WriteExcel();
                //             }

                API.apiEnd();           // API beenden

            }
        }

        private void button5_Click_1(object sender, EventArgs e)
        {
            supplier = comboBox4.Text;


            if (supplier == "Melco")
            {
                osdStart = 0x017F4360;
                offset = 16;
            }
            else if (supplier == "LGE_CID")
            {
                osdStart = 0x017F7AB0;
                offset = 16;
            }
            else if (supplier == "LGE_AZV")
            {
                osdStart = 0x017D6EB0;
                offset = 16;
            }
            else if (supplier == "Conti")
            {
                osdStart = 0x017D7000;
                offset = 28;

            }
            else if (supplier == "Innolux")
            {
                osdStart = 0x017D9A10;
                offset = 16;

            }
    
      
            

            //                        int osdStart = 0x017F4360;              // OSD Digits Start Address MLC
            //                          int osdStart = 0x017F7AB0; // LGE 
            //int osdStart = 0x017D7000;  //Conti
                                        //              int osdStart = 0x017D9A10;   //INX
                                        //           int osdStart = 0x017D6EB0;     // LG AZVGE Mid
                                        //            int offset = 16;
            //int offset = 28; //Conti
            if (API.apiInit())    // API initialisieren

                es.Job(_huSgbd, genericJob, "000b2e020002c00002017CA000");      // OSD Config Start Address
            int milliseconds = 5000;
            Thread.Sleep(milliseconds);

            for (int i = 1; i < 77; i++)
            {
                string st = "000b2e020002c000020";

                string hexVal = osdStart.ToString("X");

                string genVal = string.Concat(st, hexVal);


                es.Job(_huSgbd, genericJob, genVal);

                //                    int milliseconds = 5000;
                Thread.Sleep(milliseconds);
                osdStart += offset;
            }

            API.apiEnd();           // API beenden
        }

        private void button6_Click_1(object sender, EventArgs e)
        {
            int ramStart;
            ECU1 = comboBox2.Text;
            if (ECU1 == "NBTEvo" | ECU1 == "MGU18")
            {
              ramStart = 0x00200000;                // nbt and mgu18
            }
            else
            {
              ramStart = 0x00300000;              // new mgu21
            }
            

            int offset = 4;
            if (API.apiInit())    // API initialisieren

            //                es.str = null;

            {
                for (int i = 1; i < 25; i++)
                {
                    string st = "0007220200";
                    //                    string st = "06220200";                    // PaDi
                    string two = "02";

                    string hexVal = ramStart.ToString("X");
                    string oneVal = string.Concat(st, hexVal);
                    string flashVal = string.Concat(oneVal, two);

                    es.Job(_huSgbd, genericJob, flashVal);
                    //es.results();
                    es.Results_1(resultPath,"RAM");

                    int milliseconds = 10000;
                    Thread.Sleep(milliseconds);
                    ramStart += offset;

                }
                //string fileName = Path.Combine(es.ResultDir, "RAM_1" + ".txt");
                //ex.WriteRange(1, 1, 1000, 1000, es.str);

                //ex.SaveAs(@"test4.xlsx");
                //ex.Close();
                API.apiEnd();           // API beenden
                MessageBox.Show("Done");

            }

        }

        private void button4_Click_1(object sender, EventArgs e)
        {
            //           Console.Write("Enter arguement: ");
            val = richTextBox1.Text;

            if (API.apiInit())    // API initialisieren

            {



                es.Job(_huSgbd, genericJob, val);
                es.results();


                API.apiEnd();           // API beenden

            }

        }

        private void richTextBox1_TextChanged_1(object sender, EventArgs e)
        {

        }

        private void button11_Click_1(object sender, EventArgs e)
        {
            //             ps.Connect("10.64.71.99", 5025 );
            ps.SetVoltage(volt - 0.1);
            volt = volt - 0.1;
            textBox3.Text = (volt + "V");
        }

        private void button9_Click_1(object sender, EventArgs e)
        {
            //            ps.Connect("10.64.71.99", 5025);
            ps.SetVoltage(volt + 0.1);
            volt = volt + 0.1;
            textBox3.Text = (volt + "V");
        }

        private void button10_Click_1(object sender, EventArgs e)
        {
            doc.Load("diagnosisParameters.xml");
            //string diagJob;
            int number = 0;
            string st = "4.2.";         //MGU
                                        //              string st = "4.2a.";     //entryEvo

            for (int i = 1; i < 15; i++)
            {

                val = string.Concat(st, i.ToString());

                if (API.apiInit())    // API initialisieren

                {

                    foreach (XmlNode node in doc.DocumentElement)
                    {
                        string name = node.Attributes[0].InnerText;


                        if (val != null && val.Length >= 3)
                        {
                            if (val == name)
                            {
                                number = node.ChildNodes.Count;
                                Console.WriteLine("number is : {0}", number);

                                if (number < 4)
                                {
                                    es.Job(_huSgbd, node.ChildNodes[0].InnerText, node.ChildNodes[1].InnerText);
                                    //es.results();
                                    es.Results_1(resultPath, "Diagnosis");
                                    int milliseconds = 5000;
                                    Thread.Sleep(milliseconds);
                                }
                                else
                                {
                                    for (int j = 2; j < number; j++)
                                    {
                                        es.Job(_huSgbd, node.ChildNodes[0].InnerText, node.ChildNodes[1].InnerText + ";" + node.ChildNodes[j].InnerText);
                                        //               es.results();
                                        es.Results_1(resultPath, "Diagnosis");
                                        int milliseconds = 5000;
                                        Thread.Sleep(milliseconds);
                                    }
                                }

                            }
                            //else
                            //{
                            //    Console.Write("Job not found.");
                            //}
                        }
                        else
                        {

                            MessageBox.Show("Invalid Input");
                            break;
                        }

                    }




                    API.apiEnd();           // API beenden

                }
            }

            //ex.WriteRange(1, 1, 1000, 1000, es.str1);

            //ex.SaveAs(@"test3.xlsx");
            //ex.Close();

        }

        private void button7_Click_1(object sender, EventArgs e)
        {
            //           int flashStart = 0x017F4000;
            int flashStart = 0x017F7000;    // PaDi
            int offset = 4;
            if (API.apiInit())    // API initialisieren

            {
                for (int i = 1; i < 10; i++)
                {
                    //                   string st = "0008220300010";
                    string st = "0622020";                    // PaDi
                    string two = "02";                          //PaDi


                    //                    string hexVal = flashStart.ToString("X");                    
                    //                    string flashVal = string.Concat(st, hexVal);

                    string hexVal = flashStart.ToString("X");
                    string oneVal = string.Concat(st, hexVal);
                    string flashVal = string.Concat(oneVal, two);


                    es.Job(_huSgbd, genericJob, flashVal);
                    es.results();

                    int milliseconds = 10000;
                    Thread.Sleep(milliseconds);
                    flashStart += offset;
                }

                API.apiEnd();           // API beenden

            }

            //ex.WriteRange(1, 1, 1000, 1000, es.str1);

            //ex.SaveAs(@"test5.xlsx");
            //ex.Close();
        }

        private void comboBox3_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        private void button16_Click(object sender, EventArgs e)
        {
            ps.Connect("10.64.71.99", 5025 );


        }

        private void button17_Click(object sender, EventArgs e)
        {
            ECU1 = comboBox3.Text;

            switch (ECU1)
            {
                case "MGU18":
                    _huSgbd = "HU_MGU";

                    break;
                case "MGU21":
                    _huSgbd = "HU_MGU";

                    break;
                case "MGU22":
                    _huSgbd = "MGU_02_L";

                    break;
                case "IDC23":
                    _huSgbd = "MGU_02_A";

                    break;
                case "ICBox":
                    _huSgbd = "Kombi21";

                    break;
                case "NBTEvo":
                    _huSgbd = "NBTEVO";

                    break;
                case "EntryEvo":
                    _huSgbd = "ENAVEVO";

                    break;
            }
        }

        private void comboBox4_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        private void richTextBox5_TextChanged(object sender, EventArgs e)
        {
            richTextBox5.SelectionStart = richTextBox5.Text.Length;
            richTextBox5.ScrollToCaret();
        }

        public void Display(string output)
        {
            SynchronizationContext _syncContext;
            _syncContext = SynchronizationContext.Current;
            _syncContext.Post(_ => richTextBox5.AppendText(output), null);
        }

        private void openFileDialog1_FileOk(object sender, CancelEventArgs e)
        {

        }

        private void button18_Click(object sender, EventArgs e)
        {
            //var fileContent = string.Empty;
            //var filePath = string.Empty;
            //openFileDialog1.ShowDialog();
            openFileDialog1.InitialDirectory = "c:\\";
            //openFileDialog1.Filter = "txt files (*.txt)|*.txt|All files (*.*)|*.*";
            openFileDialog1.Filter = "Excel files (*.xlsx)|*.xlsx|All files (*.*)|*.*";
            openFileDialog1.FilterIndex = 2;
            openFileDialog1.RestoreDirectory = true;

            if (openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                //Get the path of specified file
                filePath = openFileDialog1.FileName;


            }

            //MessageBox.Show(fileContent, "File Content at path: " + filePath, MessageBoxButtons.OK);
        }

        private void button19_Click(object sender, EventArgs e)
        {
            RunPythonScript();
            HandleRadioButtonSelection();
        }

        private void RunPythonScript()
        {
            pythonEngine = "C:\\Users\\testhouse\\anaconda3\\envs\\analysis\\python.exe";
            pythonArguements = "import os ; os.chdir('E:\\Scripts\\excelWorkbooks') ; import runJob ; runJob.runJob_1( '" + filePath + "')";
            es.Run_cmd3(pythonEngine, pythonArguements);
            //HandleRadioButtonSelection();
        }

        private void HandleRadioButtonSelection()
        {
            if (radioButton1.Checked == true)
            {
                es.Results_2(resultPath, "Custom_Job ");
            }
            // Add more conditions for other radio buttons if needed
        }

        private void radioButton1_CheckedChanged(object sender, EventArgs e)
        {

        }
    }

}

