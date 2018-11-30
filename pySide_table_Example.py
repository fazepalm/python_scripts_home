import sys
import string
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class TopBar(QHeaderView):
    def __init__(self, parent=None):
        super(TopBar, self).__init__(Qt.Horizontal, parent)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setMovable( True )
        self.customContextMenuRequested.connect(self.ctxMenu)
        self.hello = QAction("Hello", self)
        self.hello.triggered.connect(self.printHello)
        self.currentSection = None

    def printHello(self):
        data = self.model().headerData(self.currentSection, Qt.Horizontal)
        print data.toString()

    def ctxMenu(self, point):
        menu = QMenu(self)
        self.currentSection = self.logicalIndexAt(point)
        menu.addAction(self.hello)
        menu.exec_(self.mapToGlobal(point))


class Table(QTableWidget):
    def __init__(self, parent=None):
        super(Table, self).__init__(parent)
        self.setHorizontalHeader(TopBar(self))
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(['id', 'name', 'username'])
        self.populate()

    def populate(self):
        self.setRowCount(10)
        rowCount = self.rowCount()
        for i in range(rowCount):
            for j,L in enumerate(string.letters[:3]):
                print QTableWidgetItem(L)
                self.setItem(i, j, QTableWidgetItem(L))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    t = Table()
    t.show()
    app.exec_()
    sys.exit()
