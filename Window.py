#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from collections import defaultdict
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self._update_secs = 30
        self.title = 'OS'
        self.left = 0
        self.top = 0
        self.width = 900
        self.height = 300
        self.speed = 0
        self.row = (
            (1,2,80,1),
            (2,200,20,0),
            (2,200,20,0),
            (2,200,20,0),
            (2,200,20,0),
            (2,200,20,0),
            (2,200,20,0),
            (2,200,20,0),
            (2,200,20,0),
            (2,200,20,0),
            (2,200,20,0),
        )
        self.typeRow = ("Работает", "Выполнено")
        self.workType = ("Start", "Finish")
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.layout = QGridLayout()
        self.setLayout(self.layout) 
        btnUp = QPushButton("+", self) 
        btnUp.clicked.connect(self.btnUpClicked)
        btnDown = QPushButton("-", self)
        btnDown.clicked.connect(self.btnDownClicked)
        btnSet = QPushButton(self.workType[0], self)
        btnSet.clicked.connect(self.btnSetClicked)

        self.createTable()

        self.layout.addWidget(QLabel("Speed: " + str(self.speed)), 1, 0)
        self.layout.addWidget(btnUp, 1, 1)
        self.layout.addWidget(btnDown, 1,2)
        self.layout.addWidget(btnSet, 1, 4) 
        self.layout.addWidget(QLabel(), 1, 0) 
        self.layout.addWidget(QLabel("CPU0: The task is't"),2, 0) 
        self.layout.addWidget(QLabel("History:"), 3, 0) 
        self.layout.addWidget(self.tableWidget, 4, 0, -1, -1) 

        self.show()
    
    def setTableWidth(self):
        height = self.tableWidget.verticalHeader().height()
        height += self.tableWidget.horizontalHeader().length()
        if self.tableWidget.verticalScrollBar().isVisible():
            height += self.tableWidget.verticalScrollBar().height()
        height += self.tableWidget.frameWidth() * 2

    def createProgressBar(self, count):
        progressBar = QProgressBar()
        progressBar.setMaximum(100)
        progressBar.setMinimum(0)
        progressBar.setValue(count)
        return progressBar

    def createTable(self):
        self.tableWidget = QTableView()
        self.tableWidget.verticalHeader().hide()
        
        sti = QStandardItemModel()
        sti.setColumnCount(4)
        sti.setHorizontalHeaderLabels(["ID", "Память", "Прогресс", "Состояние"])
        self.tableWidget.setModel(sti)

        index = 0
        for idRow, speed, progressBar, typeRow in self.row:
            sti.appendRow([QStandardItem("") for i in range(4)])
            self.tableWidget.setIndexWidget(sti.index(index, 0), QLabel(str(idRow)))
            self.tableWidget.setIndexWidget(sti.index(index, 1), QLabel(str(speed)))
            self.tableWidget.setIndexWidget(sti.index(index, 2), self.createProgressBar(progressBar))
            self.tableWidget.setIndexWidget(sti.index(index, 3), QLabel(self.typeRow[typeRow]))
            index += 1 

        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.tableWidget.setFixedHeight(300)

        self.tableWidget.doubleClicked.connect(self.on_click)

    def btnUpClicked(self):
        self.speed += 10
        print(self.speed)

    def btnDownClicked(self):
        self.speed -= 10
        print(self.speed)
    
    def btnSetClicked(self):
        print("set")
    
    @pyqtSlot()
    def on_click(self):
        sys.exit()
        