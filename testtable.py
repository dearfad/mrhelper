
import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QMainWindow, QPushButton, QVBoxLayout, QTableWidgetItem


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.table = QTableWidget()
        self.table.setRowCount(20000)
        self.table.setColumnCount(20)
        self.setCentralWidget(self.table)
        self.setGeometry(400, 200, 600, 600)
        self.table.cellClicked.connect(self.additem)
        # self.table.cellClicked.connect(self.addtable)
        self.statusBar()

    def addtable(self):
        t_start = time.clock()
        for row in range(20000):
            for column in range(20):
                qitem = QTableWidgetItem(str(row))
                self.table.setItem(row, column, qitem)
                # self.statusBar().showMessage(str(row))
                # self.sigitem.emit((row, column, qitem))
        t_end = time.clock()
        self.statusBar().showMessage(str(t_end))


    def additem(self):
        self.qthread = TableThread(self.table)
        self.qthread.sigitem.connect(self.tableitem)
        self.qthread.sigmsg.connect(self.showmsg)
        self.qthread.sigover.connect(self.showtable)
        t_start = time.clock()
        self.qthread.start()
    
    def showtable(self):
        t_end = time.clock()
        self.statusBar().showMessage(str(t_end))

    def tableitem(self, content):
        row, column, qitem = content[0], content[1], content[2]
        self.table.setItem(row, column, qitem)
    
    def showmsg(self, msg):
        self.statusBar().showMessage(msg)


class TableThread(QThread):

    sigitem = pyqtSignal(tuple)
    sigmsg = pyqtSignal(str)
    sigover = pyqtSignal()

    def __init__(self, table):
        super().__init__()
        self.table = table

    def run(self):
        for row in range(20000):
            for column in range(20):
                qitem = QTableWidgetItem(str(row))
                self.table.setItem(row, column, qitem)
                # self.sigitem.emit((row, column, qitem))
                # if row%100 == 0:
                # self.sigmsg.emit(str(row))
        self.sigover.emit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())
