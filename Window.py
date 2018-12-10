#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, random
from collections import defaultdict
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Task import Task
from CPU import CPU
CPU
Task
TACT = 1 * 1000 # * 0.1

class Window(QWidget):

    maxCPU = 3
    stop = 0
    allTakts = 0
    _update_secs = 30
    _next_id_task = 1
    speed = 100
    maxSpeed = 1000
    memory_all = 10000
    workType = ("Start", "Finish")
    tasks = []
    CPUs = []

    def __init__(self):
        super().__init__()
        self.labelSpeed = QLabel()
        self.editSpeed()
        self.labelMemory = QLabel()
        self.labelDescCPU = QLabel()
        self.sti = QStandardItemModel()
        self.play = QtGui.QIcon()
        self.pause = QtGui.QIcon()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('OS')
        self.setGeometry(0, 0, 900, 300)
        layout = QHBoxLayout()
        
        plus = QtGui.QIcon()
        plus.addPixmap(QtGui.QPixmap("icons/plus.png"))
        minus = QtGui.QIcon()
        minus.addPixmap(QtGui.QPixmap("icons/minus.png"))
        
        self.play.addPixmap(QtGui.QPixmap("icons/play.png"))
        self.pause.addPixmap(QtGui.QPixmap("icons/pause.png"))
        
        btnUp = QPushButton(self) 
        btnUp.setFixedSize(30, 30)
        btnUp.setIcon(plus)
        btnUp.clicked.connect(self.btnUpClicked)

        btnDown = QPushButton(self)
        btnDown.setFixedSize(30, 30)
        btnDown.setIcon(minus)
        btnDown.clicked.connect(self.btnDownClicked)

        self.btnSet = QPushButton()
        self.btnSet.setIcon(self.pause)
        #self.btnSet.setFixedSize(30, 30)
        self.btnSet.clicked.connect(self.btnSetClicked)
        btnNew = QPushButton("New", self)
        btnNew.setFixedSize(100, 30)

        btnNew.clicked.connect(self.btnNewClicked)
        self.createTable()
        layout.addWidget(self.labelSpeed)
        layout.addWidget(btnUp)
        layout.addWidget(btnDown)
        layout.addStretch(1)
        layout.addWidget(btnNew)
        
        layout.addWidget(self.labelDescCPU) 
        layout.addWidget(self.labelMemory) 
        vbox = QVBoxLayout()
        vbox.addLayout(layout)
        vbox.addWidget(self.table)
        vbox.addWidget(self.btnSet) 
        
        self.setLayout(vbox)
        self.timer = QBasicTimer()
        for i in range(self.maxCPU):
            cpu = CPU(
                id=i,
                speed=self.speed
            )
            self.CPUs.append(cpu)
        self.timer.start(TACT * self.speed / 100, self)
        self.editMemory(0)
        self.show()
    
    def setTableWidth(self):
        height = self.table.verticalHeader().height()
        height += self.table.horizontalHeader().length()
        if self.table.verticalScrollBar().isVisible():
            height += self.table.verticalScrollBar().height()
        height += self.table.frameWidth() * 2

    def createProgressBar(self, count):
        progressBar = QProgressBar()
        progressBar.setMaximum(100)
        progressBar.setMinimum(0)
        progressBar.setValue(count)
        return progressBar

    def createTable(self):
        self.table = QTableView()
        self.table.verticalHeader().hide() 
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.sti.setColumnCount(5)
        self.sti.setHorizontalHeaderLabels(["ID", "Memory", "Progress", "State", "Tacts"])
        self.table.setModel(self.sti)
        header = self.table.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table.resizeColumnsToContents()
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.context)

    def btnUpClicked(self):
        self.speed += 50
        if self.speed > self.maxSpeed:
            self.speed = self.maxSpeed
        for CPU in self.CPUs:
            CPU.setSpeed(self.speed)
        self.timer.start(TACT / self.speed * 100, self)
        self.editSpeed()

    def btnDownClicked(self):
        self.speed -= 50
        if self.speed < 0:
            self.speed = 0
        for CPU in self.CPUs:
            CPU.setSpeed(self.speed)
        self.timer.start(TACT / self.speed * 100, self)
        self.editSpeed()
    
    def btnSetClicked(self):
        self.btnSet.setIcon(QIcon())
        if self.stop == 1:
            self.btnSet.setIcon(self.pause)
            self.stop = 0
        else:
            self.stop = 1
            self.btnSet.setIcon(self.play)
    
    def btnNewClicked(self):
        self.addTask()
    
    def redrawTable(self):
        self.sti = QStandardItemModel()
        self.sti.setColumnCount(6)
        self.sti.setHorizontalHeaderLabels(["ID", "Memory", "Progress", "State", "Tacts", "E"])
        self.table.setModel(self.sti)
        index = 0
        tmpTasks = []
        for task in self.tasks:
            if task.getIdTypeTask() == 0 or task.getIdTypeTask() == 1:
                self.sti.appendRow([QStandardItem("") for i in range(4)])
                self.table.setIndexWidget(
                    self.sti.index(index, 0), QLabel(str(task.id)))
                self.table.setIndexWidget(
                    self.sti.index(index, 1), QLabel('{}Мб'.format(task.memory_size)))
                self.table.setIndexWidget(
                    self.sti.index(index, 2), self.createProgressBar(task.getProgress()))
                self.table.setIndexWidget(
                    self.sti.index(index, 3), QLabel(task.getTypeTask()))
                self.table.setIndexWidget(
                    self.sti.index(index, 4), QLabel(task.counter()))
                self.table.setIndexWidget(
                    self.sti.index(index, 5), QLabel(task.getTick()))
                index += 1
                tmpTasks.append(task) 
        self.task = tmpTasks

            
    def addTask(self):
        if self.memory_all < 1:
            return
        memory_size = random.randint(1, self.memory_all)
        self.editMemory(memory_size)
        task = Task(
            id=self._next_id_task,
            memory_size=memory_size,
            count_tact=random.randint(1, 50) #self.memory_all)
        )
        self._next_id_task += 1
        self.tasks.append(task)
        self.redrawTable()
        
    def editSpeed(self):
        self.labelSpeed.setText('Speed: {}%'.format(self.speed))

    def editMemory(self, memory_size, typeEdit = 'erase'):
        if typeEdit == 'erase':
            self.memory_all = self.memory_all - memory_size
        if typeEdit == 'add':
            self.memory_all = self.memory_all + memory_size
        self.labelMemory.setText('Takts: {} \n M Free: {}\nM Total: 10 000  \n'.format(self.allTakts, self.memory_all))
    
    def context(self, point, *args, **kwargs):
        menu = QMenu()
        edit_row = self.table.selectionModel().selectedRows()
        if edit_row:
            edit_row = edit_row[0].row()
            edit_question = QAction('Edit task', menu)
            edit_question.triggered.connect(self.contextEvent)
            menu.addAction(edit_question)
            menu.exec(self.table.mapToGlobal(point))

    def contextEvent(self, *args, **kwargs):
        selected_rows = self.table.selectionModel().selectedRows()
        selected_row = selected_rows[0] if selected_rows else None
        if selected_row:
            index = selected_row.row()
            edit_task = self.tasks[index]

    def renderTasks(self):
        allCPU = ''
        if self.stop == 0:
            index = 0
            for cp in self.CPUs:
                allCPU = str(allCPU) + "CPU " + str(index) + ": X\n"
                index += 1
            self.labelDescCPU.setText(allCPU)
            return
        index = 0
        for cp in self.CPUs:
            allCPU = str(allCPU) + "CPU " + str(index) + ": " + str(cp.getCurrentTask()) + '\n'  
            index += 1
            if cp.getCurrentTask() == 0:
                minIdTask = 0
                for task in self.tasks:
                    if task.getIdTypeTask() == 0:
                        minIdTask = task.id
                        task.updateTypeTask(1)
                        break
                cp.setCurrentTask(minIdTask)
            if cp.getCurrentTask() == 0:
                self.addTask()
                continue
            id = cp.getCurrentTask() - 1
            self.allTakts = self.allTakts + 1
            if self.tasks[id].doneTacts == self.tasks[id]._max_tacts_doing:
                cp.setCurrentTask(0)
                self.tasks[id].updateTypeTask(3)
                if self.tasks[id].idTypeTask == 2:
                   self.tasks[id].updateTypeTask(3)
                   self.tasks[id].idTypeTask = 3
                   cp.setCurrentTask(0)
                self.editMemory(self.tasks[id].memory_size, 'add')
        for task in self.tasks:
            task.appendTick()
        self.redrawTable()
        self.labelDescCPU.setText(allCPU)

    
    def timerEvent(self, *args, **kwargs):
        self.renderTasks()
