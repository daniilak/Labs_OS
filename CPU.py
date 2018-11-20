#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, random
from collections import defaultdict

class CPU(object):

    states = ("запущен","Пауза", "Остановлен")
    typeState = 2
    idCurrentTask = 0
    task = 0

    def __init__(self, **kwargs):
        super().__init__()
        for key in kwargs:
            setattr(self, key, kwargs[key])
            setattr(self, key, kwargs[key])
    
    def getCurrentTask(self):
        return self.idCurrentTask

    def setCurrentTask(self, id):
        self.idCurrentTask = id   
        return

    def setSpeed(self, speed):
        self.speed = speed

    def getSpeed(self):
        return self.speed

    def getTypeState(self):
        return states[self.typeState]

    def setTypeState(self, typeState):
        self.typeState = typeState