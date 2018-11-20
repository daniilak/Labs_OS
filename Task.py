#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, random
from collections import defaultdict

class Task(object):
    typeTask = ("Ждет","Работает", "Выполнено","Очищен")

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
        if self.doneTacts >= self._max_tacts_doing:
            self.doneTacts = self._max_tacts_doing
            self.idTypeTask = 2
            return '{}/0'.format(self.doneTacts)
        self.doneTacts += 1
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
