#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, random
from collections import defaultdict
TACT = 1 * 1000 * 0.1

class Task(object):
    typeTask = ("Ждет","Работает", "Выполнено")
    hight = 'Hight'
    medium = 'Medium'
    low = 'Low'
    prioritiesIndexes = {
        hight: 0,
        medium: 1,
        low: 2,
    }
    priorities = {
        hight: 'Высокий',
        medium: 'Средний',
        low: 'Низкий',
    }

    def __init__(self, **kwargs):
        super().__init__()
        for key in kwargs:
            setattr(self, key, kwargs[key])
            setattr(self, key, kwargs[key])
        self.idTypeTask = 0
        self.doneTacts = 0
        self._max_tacts_doing = self.count_tact 

    def counter(self):
        if self.doneTacts >= self._max_tacts_doing:
            self.doneTacts = self._max_tacts_doing
            self.idTypeTask = 2
            return 0
        self.doneTacts += 1
        return self._max_tacts_doing - self.doneTacts
    
    def getProgress(self):
        return self.doneTacts * 100 / self._max_tacts_doing

    def getTypeTask(self):
        return self.typeTask[self.idTypeTask]
    
    def getInfo(self):
        return str()
