#!/usr/bin/python

import sys
from PyQt4 import QtCore, QtGui, uic
import rinex_preprocess
import os
 
qtCreatorFile = "osgvGnssDataSubmit.ui" # Enter file here.
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
 
def file_open(self):
    filename = QtGui.QFileDialog.getOpenFileName(None, 'Open File', '/', "Trimble Data Files (*.T01 *.T02)")
    path = os.path.dirname(filename)
    
    print(os.path.basename(filename))
    print(os.path.dirname(filename))
    os.chdir(path)
    window.lineEdit_t0.setText(os.path.basename(filename))
    
def process(self):
    rinex_preprocess.get_smes(window.lineEdit_ninefig.text())
    rinex_preprocess.get_char4(window.lineEdit_ninefig.text())

    print(rinex_preprocess.get_smes.mark_name)
    print(rinex_preprocess.get_char4.char4)
    window.label_markname.setText(rinex_preprocess.get_smes.mark_name)
    window.label_lat.setText('{0:0.8f}'.format(rinex_preprocess.get_smes.mark_latitude))
    window.label_long.setText('{0:0.8f}'.format(rinex_preprocess.get_smes.mark_longitude))
    window.label_4char.setText(rinex_preprocess.get_char4.char4)
    arguments = ("-f \""+window.lineEdit_t0.text()+
    						"\" --ninefig "+window.lineEdit_ninefig.text()+
    						" -a "+window.lineEdit_slope_hgt.text()+
    						" -c "+window.lineEdit_antenna_serial.text()+
    						" -o "+window.lineEdit_observer.text())
    #print(arguments)
    #print(window.lineEdit_t0.text())
    input_st = os.path.basename(window.lineEdit_t0.text()).split('.')
    rinex_preprocess.t0_runpk(window.lineEdit_t0.text())
    rinex_preprocess.call_teqc(window.label_4char.text(), window.lineEdit_ninefig.text(), window.lineEdit_slope_hgt.text(),window.lineEdit_antenna_serial.text(), window.lineEdit_observer.text(),window.label_markname.text(), window.label_lat.text(), window.label_long.text(), input_st[0])
    
    #rinex_preprocess.main("--ninefig 356300460")

class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton_file.clicked.connect(file_open)
        self.pushButton_run.clicked.connect(process)
 
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())