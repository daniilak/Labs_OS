#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, random
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
        self.index = 0
        self.width = 900
        self.height = 300
        self.speed = 100
        self.maxSpeed = 1000
        self.memory = 4000
        self.labelSpeed = QLabel()
        self.editSpeed(self.speed)
        self.labelMemory = QLabel()
        self.sti = QStandardItemModel()
        self.row = []
        self.typeRow = ("Ждет","Работает", "Выполнено")
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


        btnNew = QPushButton("New", self) 
        btnNew.clicked.connect(self.btnNewClicked)

        self.createTable()
        
        self.layout.addWidget(self.labelSpeed, 1, 0)
        self.layout.addWidget(btnUp, 1, 1)
        self.layout.addWidget(btnDown, 1,2)
        self.layout.addWidget(btnSet, 1, 4) 
        self.layout.addWidget(QLabel(), 1, 0) 
        self.layout.addWidget(QLabel("CPU0: The task is't"),2, 0) 
        self.layout.addWidget(btnNew, 2, 1) 
        self.layout.addWidget(QLabel("History:"), 3, 0) 
        self.layout.addWidget(self.labelMemory, 4, 0) 
        self.layout.addWidget(self.tableWidget, 5, 0, -1, -1) 
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
        
        
        self.sti.setColumnCount(4)
        self.sti.setHorizontalHeaderLabels(["ID", "Память", "Прогресс", "Состояние"])
        self.tableWidget.setModel(self.sti)
        tmpCount = 1
        for i in range(4):
            allCount = random.randint(1,1000)
            doneCount = random.randint(1, allCount)
            res = (100 * doneCount) / allCount
            self.row.append((i + 1,random.randint(1,100),res,0,tmpCount,random.randint(1,tmpCount)))
        
        
        for idRow, memory, progressBar, typeRow, countProgress, countDone in self.row:
            self.addRow(memory,progressBar, typeRow)
        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.tableWidget.setFixedHeight(300)

    def btnUpClicked(self):
        self.speed += 10
        if (self.speed > self.maxSpeed):
            self.speed = self.maxSpeed
        self.editSpeed(self.speed)

    def btnDownClicked(self):
        self.speed -= 10
        if (self.speed < 0):
            self.speed = 0
        self.editSpeed(self.speed)
    
    def btnSetClicked(self):
        print("set")
    
    def btnNewClicked(self):
        self.row.append((self.index,0,0,0,0,0))
        self.addRow(0, 0, 0)
        print("new")

    def addRow(self, memory, progress, typeRow):
        self.sti.appendRow([QStandardItem("") for i in range(4)])
        self.memory = self.memory - memory
        self.editMemory(self.memory)
        self.tableWidget.setIndexWidget(self.sti.index(self.index, 0), QLabel(str(self.index)))
        self.tableWidget.setIndexWidget(self.sti.index(self.index, 1), QLabel(str(memory)+"Мб"))
        self.tableWidget.setIndexWidget(self.sti.index(self.index, 2), self.createProgressBar(progress))
        self.tableWidget.setIndexWidget(self.sti.index(self.index, 3), QLabel(self.typeRow[typeRow]))
        self.index = self.index + 1

    def editSpeed(self, speed):
        self.labelSpeed.setText("Speed: " + str(self.speed) + " %")

    def editMemory(self, memory):
        self.labelMemory.setText("Память: " + str(memory) + " свободно из 4000")
        