
import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QMainWindow, QTableWidgetItem


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.table = QTableWidget()
        self.table.setRowCount(100000)
        self.table.setColumnCount(20)
        self.setCentralWidget(self.table)
        self.setGeometry(400, 200, 600, 600)
        self.table.cellClicked.connect(self.useqthread)
        # self.table.cellClicked.connect(self.usemainui)
        self.statusBar()

    def usemainui(self):
        t_start = time.process_time()
        for row in range(100000):
            for column in range(20):
                qitem = QTableWidgetItem(str(row))
                self.table.setItem(row, column, qitem)
        t_end = time.process_time()
        self.statusBar().showMessage(str(t_end))

    def useqthread(self):
        self.qthread = TableThread(self.table)
        self.qthread.sigitem.connect(self.tableitem)
        self.qthread.sigover.connect(self.showtable)
        # self.table.setUpdatesEnabled(False)
        self.qthread.start()

    def showtable(self, t_end):
        # self.table.setUpdatesEnabled(True)
        self.statusBar().showMessage(t_end)

    def tableitem(self, content):
        row, column, qitem = content[0], content[1], content[2]
        self.table.setItem(row, column, qitem)


class TableThread(QThread):

    sigitem = pyqtSignal(tuple)
    sigover = pyqtSignal(str)

    def __init__(self, table):
        super().__init__()
        self.table = table

    def run(self):
        t_start = time.process_time()
        for row in range(100000):
            for column in range(20):
                qitem = QTableWidgetItem(str(row))
                self.table.setItem(row, column, qitem)
                # self.sigitem.emit((row, column, qitem))
        t_end = time.process_time()
        self.sigover.emit(str(t_end))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())
