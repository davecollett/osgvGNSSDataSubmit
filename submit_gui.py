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
    
def check_smes(self):
    rinex_preprocess.get_smes(window.lineEdit_ninefig.text())
    window.label_markname.setText(rinex_preprocess.get_smes.mark_name)
    window.label_lat.setText(str(rinex_preprocess.get_smes.mark_latitude))
    window.label_long.setText(str(rinex_preprocess.get_smes.mark_longitude))
    
    indexMp = window.comboBoxMp.findText(rinex_preprocess.get_smes.markPostExists)
    if indexMp >= 0: 
       window.comboBoxMp.setCurrentIndex(indexMp)
       
    indexCvr = window.comboBoxMp.findText(rinex_preprocess.get_smes.coverExists)
    if indexCvr >= 0: 
       window.comboBoxCvr.setCurrentIndex(indexCvr)
       
    indexMt = window.comboBoxMt.findText(rinex_preprocess.get_smes.markType)
    if indexMt >= 0: 
       window.comboBoxMp.setCurrentIndex(indexMt)
       
    indexGn = window.comboBoxGnss.findText(rinex_preprocess.get_smes.gnssSuitability)
    if indexGn >= 0: 
       window.comboBoxMp.setCurrentIndex(indexGn)

    window.fieldGroundLevel.setText(str(rinex_preprocess.get_smes.groundToMarkOffset))
    
    
def check_char4(self):
    rinex_preprocess.get_char4(window.lineEdit_ninefig.text())
    print(rinex_preprocess.get_char4.char4)
    window.label_4char.setText(rinex_preprocess.get_char4.char4)
    
    
def process(self):
    input_st = os.path.basename(window.lineEdit_t0.text()).split('.')
    rinex_preprocess.t0_runpk(window.lineEdit_t0.text())
    rinex_preprocess.call_teqc(window.label_4char.text(), window.lineEdit_ninefig.text(), window.lineEdit_slope_hgt.text(),window.lineEdit_antenna_serial.text(), window.lineEdit_observer.text(),window.label_markname.text(), window.label_lat.text(), window.label_long.text(), input_st[0])
    
def smes_connect(self):
    server = window.comboBoxServer.currentText()
    username = window.smesUsername.text()
    password = window.smesPassword.text()
    nine_fig = window.lineEdit_ninefig.text()
    coverExists = window.comboBoxCvr.currentText()
    smesComment = window.smesComment.toPlainText()
    rinex_preprocess.smes_connect(server, username, password,nine_fig, coverExists,smesComment)

def smes_update(self):
    sessionKey = smes_connect.sessionKey
    nine_fig = window.lineEdit_ninefig.text()
    coverExists = window.comboBoxCvr.currentText()
    smesComment = window.smesComment.toPlainText()
    rinex_preprocess.smes_update(sessionKey, nine_fig, coverExists,smesComment)



class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.comboBoxMp.addItems(["","Yes","No"])
        self.comboBoxCvr.addItems(["","Yes","No"])
        self.comboBoxMt.addItems(["","Plaque","Deep Driven Rod","Cross Head Nail","Star Picket","Pipe", "Rivet", "Other"])
        self.comboBoxGnss.addItems(["","Good","Moderate","Poor"])
        self.comboBoxServer.addItems(["PROD","UAT","SYSTEST"])
        self.pushButton_file.clicked.connect(file_open)
        self.pushSMES.clicked.connect(check_smes)
        self.push4Char.clicked.connect(check_char4)
        self.pushButton_run.clicked.connect(process)
        self.pushButtonUpdateSmes.clicked.connect(smes_connect)
    
 
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())