#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot
from Window import Window
Window
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("mac") 
    ex = Window()
    sys.exit(app.exec_())  
