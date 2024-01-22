using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using DocumentFormat.OpenXml.Drawing.Diagrams;

using Microsoft.Office.Interop.Excel;
using _Excel = Microsoft.Office.Interop.Excel;
using Word = Microsoft.Office.Interop.Word;

namespace TestControl
{
    class Excel
    {
        string path = "";
        _Application excel = new _Excel.Application(); 
        Workbook wb;
        Worksheet ws;

        public Excel()
        {

        }

        public Excel(string path, int Sheet)
        {
            this.path = path;
            wb = excel.Workbooks.Open(path);
            ws = wb.Worksheets[Sheet];
        }

        public void CreateNewFile()
        {
            this.wb = excel.Workbooks.Add(XlWBATemplate.xlWBATWorksheet);
            this.ws = wb.Worksheets[1];
        }

        public void CreateNewSheet()
        {
            Worksheet temptsheet = wb.Worksheets.Add(After: ws);
        }
        public string ReadCell(int i, int j)
        {
            i++;
            j++;
            if(ws.Cells[i,j].Value2 != null){
                return ws.Cells[i, j].Value2;
            }
            else
            {
                return "";
            }
                  
        }

        public string [,] ReadRange( int starti , int starty, int endi, int endy)
        {
            Range range = (Range)ws.Range[ws.Cells[starti, starty], ws.Cells[endi, endy]];
            object[,] holder = range.Value2;
            string[,] returnstring = new string[endi = starti, endy = starty];
            for(int p= 1; p <= endi - starti; p++)
            {
                for (int q = 1; q <= endy - starty; p++)
                {
                    returnstring[p - 1, q - 1] = holder[p, q].ToString();
                }
            }
            return returnstring;
        }

        public void WriteToCell(int i, int j, string s)
        {
            //i++;
            //j++;
            ws.Cells[i, j].Value2 = s;
        }

        public void WriteRange(int starti, int starty, int endi, int endy, string[,] writestring)
        {
                Range range = (Range)ws.Range[ws.Cells[starti, starty], ws.Cells[endi, endy]];
            range.Value2 = writestring;
        }

        public void Save()
        {
            wb.Save();
        }

        public void SaveAs(string path)
        {
            wb.SaveAs(path);
        }

        public void SelectWorksheet(int SheetNumber)
        {
           this.ws =  wb.Worksheets[SheetNumber];
        }

        public void DeleteWorksheet(int SheetNumber)
        {
            wb.Worksheets[SheetNumber].Delete();
        }

        public void Close()
        {
            wb.Close();
        }
    }
}
