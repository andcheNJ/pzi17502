# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 20:53:17 2022

@author: Andrew
"""

import sys

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import uic
import recordVid_1 as rv1

class AppDemo(QWidget):
    
    def __init__(self):
        super().__init__()
        uic.loadUi('recApp.ui', self)
        
        self.pushButton.clicked.connect(self.startVid)
        self.pushButton_2.clicked.connect(self.pauseVid)
        self.pushButton_3.clicked.connect(self.stopVid)
        
        
    def startVid(self):
        # print(self.lineEdit_Entry.text())
        rv1.recordVideo().start_vid()
        
    def pauseVid(self):
        
        rv1.recordVideo().pause_Recording()
        
    def stopVid(self):

        rv1.recordVideo().terminate()
        print('stopping')

         
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    
    demo = AppDemo()
    demo.show()
    
    try:
        sys.exit(app.exec_())
       
    except SystemExit:
        print('Closing window ...')
      