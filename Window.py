#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, random
from collections import defaultdict
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Task import Task
Task
TACT = 1 * 1000 * 0.1

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self._update_secs = 30
        self.title = 'OS'
        self.stop = 0
        self.stopB = 1
        self._next_id_task = 0
        self.speed = 100
        self.maxSpeed = 1000
        self.memory_all = 10000
        self.labelSpeed = QLabel()
        self.editSpeed(self.speed)
        self.labelMemory = QLabel()
        self.sti = QStandardItemModel()
        self.workType = ("Start", "Finish")
        self.tasks = []
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, 900, 300)
        self.layout = QGridLayout()
        self.setLayout(self.layout) 
        btnUp = QPushButton("+", self) 
        btnUp.clicked.connect(self.btnUpClicked)
        btnDown = QPushButton("-", self)
        btnDown.clicked.connect(self.btnDownClicked)
        self.btnSet = QPushButton(self.workType[0], self)
        self.btnSet.clicked.connect(self.btnSetClicked)
        btnNew = QPushButton("New", self) 
        btnNew.clicked.connect(self.btnNewClicked)
        self.createTable()
        self.layout.addWidget(self.labelSpeed, 1, 0)
        self.layout.addWidget(btnUp, 1, 1)
        self.layout.addWidget(btnDown, 1,2)
        self.layout.addWidget(self.btnSet, 1, 4) 
        self.layout.addWidget(QLabel(), 1, 0) 
        self.layout.addWidget(QLabel("CPU0: The task is't"),2, 0) 
        self.layout.addWidget(btnNew, 2, 1) 
        self.layout.addWidget(QLabel("History:"), 3, 0) 
        self.layout.addWidget(self.labelMemory, 4, 0) 
        self.layout.addWidget(self.tableWidget, 5, 0, -1, -1) 
        self.timer = QBasicTimer()
        self.timer.start(TACT * self.speed / 100, self)
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
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.sti.setColumnCount(5)
        self.sti.setHorizontalHeaderLabels(["ID", "Память", "Прогресс", "Состояние", "кол-во"])
        self.tableWidget.setModel(self.sti)
        self.addRow()
        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.tableWidget.setFixedHeight(300)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setSelectionBehavior(QTableView.SelectRows)

    def btnUpClicked(self):
        self.speed += 10
        if self.speed > self.maxSpeed:
            self.speed = self.maxSpeed
        self.editSpeed(self.speed)

    def btnDownClicked(self):
        self.speed -= 10
        if self.speed < 0:
            self.speed = 0
        self.editSpeed(self.speed)
    
    def btnSetClicked(self):
        self.stop, self.stopB = self.stopB, self.stop
        if self.stop == 1:
            self.btnSet.setText('Start')
        else:
            self.btnSet.setText('Stop')
        
    
    def btnNewClicked(self):
        self.addRow()

    def addRow(self):
        if self.memory_all < 1:
            return
        memory_size = random.randint(1, self.memory_all)
        priority = random.randint(0, 2)
        self.editMemory(memory_size)
        task = Task(
            id=self._next_id_task,
            priority=priority,
            memory_size=memory_size,
            count_tact=random.randint(1, self.memory_all)
        )
        
        self.sti.appendRow([QStandardItem("") for i in range(4)])
        self.tableWidget.setIndexWidget(
            self.sti.index(self._next_id_task, 0), QLabel(str(task.id)))
        self.tableWidget.setIndexWidget(
            self.sti.index(self._next_id_task, 1), QLabel('{}Мб'.format(task.memory_size)))
        self.tableWidget.setIndexWidget(
            self.sti.index(self._next_id_task, 2), self.createProgressBar(task.getProgress()))
        self.tableWidget.setIndexWidget(
            self.sti.index(self._next_id_task, 3), QLabel(task.getTypeTask()))
        self.tableWidget.setIndexWidget(
            self.sti.index(self._next_id_task, 4), QLabel(str(task.count_task)))
        self._next_id_task += 1
        self.tasks.append(task)

        
    def editSpeed(self, speed):
        self.labelSpeed.setText('Speed {}%'.format(self.speed))

    def editMemory(self, memory_size):
        self.memory_all = self.memory_all - memory_size
        self.labelMemory.setText('Память: {} свободно из 10 000'.format(self.memory_all))
    
    def renderTasks(self):
        if self.stop == 1:
            i = 0
            for task in self.tasks:
                self.tableWidget.setIndexWidget(self.sti.index(i, 4), QLabel(str(task.counter())))
                self.tableWidget.setIndexWidget(self.sti.index(i, 2), self.createProgressBar(task.getProgress()))
                self.tableWidget.setIndexWidget(self.sti.index(i, 3), QLabel(task.getTypeTask()))
                i += 1
    
    def timerEvent(self, *args, **kwargs):
        self.renderTasks()
        