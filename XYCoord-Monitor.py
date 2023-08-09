from re import I
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import logging
import numpy as np
import pyqtgraph as pg
import csv
from struct import *
import time 
import pandas as pd
import numpy as np
from numpy.linalg import inv
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon, QStandardItem, QStandardItemModel
from PyQt5.QtCore import *
from PyQt5 import QtCore 
from threading import *

# UI 파일과 Python 소스 코드 연결
form_class = uic.loadUiType("./pos.ui")[0]

# Log 출력 준비
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class QPlainTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super(QPlainTextEditLogger, self).__init__()

        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)

    def write(self, m):
        pass

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("Monitor UI")
        
        self.isConnected = False
        self.OperS = False
        self.Operation = 0
        self.lfStatus = "None"
        self.fError = "None"
        self.comStatus = 0
        self.isRecording = 0
        self.dataBuffer = None
        self.recording = False
        self.recordind = 0
        self.f = 0

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        self.pv = pg.PlotWidget(title="")
        self.pv.setRange(yRange = (0, 16.5), xRange = (0, 16.5), disableAutoRange=True)
        # self.pv.enableAutoRange(axis='xy', enable=True)
        self.scatter = pg.ScatterPlotItem(
            size=10, brush=pg.mkBrush(120, 218, 46, 255))
        self.scatterRef = pg.ScatterPlotItem(
            size=10, brush=pg.mkBrush(91, 155, 213, 255))
        self.x_data = [0]
        self.y_data = [0]
        self.scatter.addPoints(self.x_data,self.y_data)
        self.scatterRef.addPoints(self.x_data,self.y_data)
        self.pv.addItem(self.scatter)
        self.pv.addItem(self.scatterRef)
        self.graph_gridLayout.addWidget(self.pv)
        self.pv.showGrid(x=True, y=True)
        self.pv.addLegend(size=(100, 10))

        #Thread Control
        self.work = worker()
        self.work.finished.connect(self.update_s)

        #Disable buttons
        # self.disableB()

        # Set up logging to use your widget as a handler
        log_handler = QPlainTextEditLogger(self.widget)
        log_handler2 = QPlainTextEditLogger(self.widget_2)

        logging.getLogger().addHandler(log_handler)
        logging.getLogger().addHandler(log_handler2)
    #################------BUTTON Field-------#######################
        #버튼에 기능을 연결하는 코드
        self.pushButton.clicked.connect(self.button1Function)
        self.pushButton_2.clicked.connect(self.button2Function)
        self.pushButton_3.clicked.connect(self.button3Function)
        self.pushButton_4.clicked.connect(self.button4Function)        
        self.pushButton_5.clicked.connect(self.button5Function)
        self.pushButton_6.clicked.connect(self.button6Function)
        self.pushButton_7.clicked.connect(self.button7Function)
        self.pushButton_10.clicked.connect(self.button10Function)
        self.pushButton_11.clicked.connect(self.bCp)
        self.pushButton_12.clicked.connect(self.button12Function)
        


    #btn_1이 눌리면 작동할 함수
    def button1Function(self) :
        print("btn_1 Clicked")

    #btn_2가 눌리면 작동할 함수
    def button2Function(self) :
        print("btn_2 Clicked")

    #btn_3이 눌리면 작동할 함수
    def button3Function(self) :
        print("btn_3 Clicked")

    #btn_4가 눌리면 작동할 함수
    def button4Function(self) :
        print("btn_4 Clicked")   

    #btn_5이 눌리면 작동할 함수
    def button5Function(self) :
        print("btn_5 Clicked")

    #btn_6가 눌리면 작동할 함수
    def button6Function(self) :
        print("btn_6 Clicked")

    #btn_7이 눌리면 작동할 함수
    def button7Function(self) :
        print("btn_7 Clicked")
        logging.debug('logging debug123123123123213')
        logging.debug('logging deb12312312312312ug')
        logging.debug('logging debu321312321321g')
        logging.debug('logging debu312312312321g')
        logging.debug('logging debu321312312g')

    def button10Function(self) :
        self.work.start()

    def button11Function(self) :
        self.bCp()
                
    def button12Function(self) :
        self.work.stop()

    #Mouse Event 
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos() #Get the position of the mouse relative to the window
            event.accept()
    def mouseMoveEvent(self, QMouseEvent):
        if self.m_flag:  
            self.move(QMouseEvent.globalPos()-self.m_Position)#Change window position
            QMouseEvent.accept()
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False




    @pyqtSlot(list)
    def update_s(self, data):

        # self.op.setText(data[0])
        # self.nl.setText(data[1])
        # self.nlw.setText(data[3])
        # self.fe.setText(str(round(data[2][2],5)))
        
        #print([data[2][0]],[data[2][1]])
        #print(data[4][0],data[4][1])
        # print(data[5])

        self.scatter.addPoints([data[0]],[data[1]])
        self.scatterRef.addPoints([data[0]],[data[2]])


    # def clearLayout(graph_gridLayout):
    #     for i in reversed(range(graph_gridLayout.count())): 
    #         graph_gridLayout.itemAt(i).widget().setParent(None)



    def logoB(self):
        sys.exit()

    # def disableB(self):
    #     self.rs.setEnabled(False)
    #     self.rr.setEnabled(False)
    #     self.so.setEnabled(False)
    #     self.cp.setEnabled(False)
    #     self.plclear()
    #     self.stopR()
    #     self.op.setText("None")
    #     self.nl.setText("None")
    #     self.fe.setText("None")
    
    def startR(self):
        self.recording = True
        self.rr.setText("Stop Recording")
        self.f = open("Result.txt", mode= "w+")

    
    def stopR(self):
        self.recording = False
        self.rr.setText("Start Recording")
        if self.f:
            self.recordind = 0
            self.lcdN.display(str(self.recordind))
            self.f.close()
            self.f = 0

    def bRr(self):
        if not self.recording: #start operation
            try:
                self.startR()
            except:
                pass
        else:
            try:
                self.stopR()
            except:
                pass
        pass

    def bCp(self):
        try:
            self.plclear()
        except:
            pass

    def plclear(self):
        if self.pv:
                self.scatter.clear()
                self.scatterRef.clear()
                self.scatter.addPoints([0],[0])

    def dm(self, msg):
        print("DEBUG : ", msg)    

    #################------BUTTON Field-------#######################

class worker(QThread):
    finished = pyqtSignal(list)
    # isConnected = False
    cnt = 0
    # data_x = [0, 0, 0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0]
    # data_y = [0, 0, 0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0]

    def run(self):
        print("Start READING")
        while True:
#             if self.isConnected:
            
            df = pd.read_csv('./GUIdata.csv') 
            # print(df.shape)
            print(df.values[0,0], df.values[1,0], df.values[2,0])
            """ USER CODE BEGIN 1 """ 
            # anc1ID = anc1[0]
            x_coord = df.values[7,0]
            # anc2ID = anc2[0]
            y_coord = df.values[8,0]
            # anc3ID = anc3[0]
            x_filtered = df.values[9,0]
            y_filtered = df.values[10,0]

            self.cnt = self.cnt + 1

            # self.dataBuffer = self.scon.readline().decode("ascii")
            # self.dataBuffer = self.dataBuffer.split(',') 
                # self.dataBuffer = float(self.data_x[i], self.data_y[i]) 
            
            # Xe = 5
            time.sleep(0.5)
           
                # update_s(data[0])
            self.finished.emit([x_coord, y_coord, x_filtered, y_filtered])
            if (self.cnt == 10):
                break



if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 
    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 
    #프로그램 화면을 보여주는 코드
    myWindow.show()
    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()