#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, random
from collections import defaultdict

class Task(object):
    typeTask = ("Ждет","Работает", "Выполнено","Очищен")
    tick = 1
    tickPercent = '100.0'

    def __init__(self, **kwargs):
        super().__init__()
        for key in kwargs:
            setattr(self, key, kwargs[key])
            setattr(self, key, kwargs[key])
        self.idTypeTask = 0
        self.doneTacts = 0
        self._max_tacts_doing = self.count_tact 

    def counter(self):
        if self.idTypeTask == 3:
            return '{}/0'.format(self.doneTacts)
        if self.idTypeTask == 1:
            self.doneTacts += 1
        if self.doneTacts >= self._max_tacts_doing:
            self.doneTacts = self._max_tacts_doing
            self.idTypeTask = 2
            return '{}/0'.format(self.doneTacts)
        
        return '{}/{}'.format(self.doneTacts, self._max_tacts_doing)
    
    def getProgress(self):
        return self.doneTacts * 100 / self._max_tacts_doing

    def editIdTypeTask(self):
        return self.doneTacts * 100 / self._max_tacts_doing

    def updateTypeTask(self, newId):
        self.idTypeTask = newId

    def getIdTypeTask(self):
        return self.idTypeTask

    def getTypeTask(self):
        return self.typeTask[self.idTypeTask]
    
    def getInfo(self):
        return str()

    def getTick(self):
        print(self._max_tacts_doing, 100, self.tick)
        return str(self.tick / self._max_tacts_doing *100 )

    def appendTick(self):
        if self.idTypeTask == 0:
            self.tick += 1
        else:
            self.tick = self._max_tacts_doing
