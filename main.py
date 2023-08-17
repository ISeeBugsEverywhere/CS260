#!/usr/bin/python3
import sys, os, math
from PyQt5 import QtCore, QtGui, QtWidgets
from GUI.CS260 import Ui_MainWindow
from HW.OrielCS260USB import Oriel

WAVE_LABEL_TEXT = "Current wave [nm]: {}"

class OrielWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.signals()
        self.oriel = Oriel()

    def signals(self):
        self.ui.quitBtn.clicked.connect(self.quit_fn)
        self.ui.connectBtn.clicked.connect(self.connect_fn)
        self.ui.goBtn.clicked.connect(self.go_fn)
        self.ui.shutterToggleBtn.clicked.connect(self.toggle_fn)
        self.ui.shutterCheckBtn.clicked.connect(self.check_fn)
        self.ui.waveBtn.clicked.connect(self.wave_fn)
        self.ui.actionQuit.triggered.connect(self.quit_fn)

    def quit_fn(self):
        sys.exit(0)
    def connect_fn(self):
        r = self.oriel.setup()
        if r == 0:
            self.ui.statusLabel.setText("CONNECTED")
        elif r == 1:
            self.ui.responsesField.appendPlainText(f"NOT CONNECTED, status {r}\n")
        else:
            self.ui.responsesField.appendPlainText(f"STRANGE::{r}\n")
        pass
    def go_fn(self):
        val =  self.ui.entryBox.value()
        unit = 'nm' # default
        if val < 179:
            unit = 'ev'
            self.ui.evRadioBtn.setChecked(True)
            self.ui.nmRadioBtn.setChecked(False)
        elif val > 180:
            unit = 'nm'
            self.ui.evRadioBtn.setChecked(False)
            self.ui.nmRadioBtn.setChecked(True)
        # if self.ui.nmRadioBtn.isChecked():
        #     unit = 'nm'
        # elif self.ui.evRadioBtn.isChecked():
        #     unit = 'ev'
        bts = self.oriel.gowave(val, unit)
        self.ui.responsesField.appendPlainText(f"Bytes written: {bts}\n")
    def toggle_fn(self):
        s = self.oriel.shutter()
        # self.ui.responsesField.appendPlainText(str(s)+"\n")
        if s.lower() == 'c':
            self.oriel.openShutter()
            self.ui.shutterStatusLabel.setText("OPENED")
        elif s.lower() == 'o':
            self.oriel.closeShutter()
            self.ui.shutterStatusLabel.setText("CLOSED")
    def check_fn(self):
        s = self.oriel.shutter()
        # self.ui.responsesField.appendPlainText(str(s) + "\n")
        if s.lower() == 'c':
            self.ui.responsesField.appendPlainText("Shutter is closed.\n")
        elif s.lower() == 'o':
            self.ui.responsesField.appendPlainText("Shutter is opened.\n")
    def wave_fn(self):
        w = self.oriel.wave()
        self.ui.waveLabel.setText(WAVE_LABEL_TEXT.format(w))
        self.ui.responsesField.appendPlainText(f"Current wave: {w}\n")

    pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = OrielWindow()
    win.show()
    sys.exit(app.exec())
