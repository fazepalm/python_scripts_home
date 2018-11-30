from PyQt4 import QtGui, QtCore
import sys
import string

class TopBar(QtGui.QHeaderView):
    def __init__(self, parent=None):
        super(TopBar, self).__init__(QtCore.Qt.Horizontal, parent)

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setMovable( True )
        self.customContextMenuRequested.connect(self.ctxMenu)
        self.hello = QtGui.QAction("Hello", self)
        self.hello.triggered.connect(self.printHello)
        self.currentSection = None

    def printHello(self):
        data = self.model().headerData(self.currentSection, QtGui.Qt.Horizontal)
        print data.toString()

    def ctxMenu(self, point):
        menu = QtGui.QMenu(self)
        self.currentSection = self.logicalIndexAt(point)
        menu.addAction(self.hello)
        menu.exec_(self.mapToGlobal(point))

class Table(QtGui.QTableWidget):
    def __init__(self, parent=None):
        super(Table, self).__init__(parent)
        self.setHorizontalHeader(TopBar(self))
        self.setRowCount(10)
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(['id', 'name', 'idColor'])
        self.populate()

    def populate(self):
        rowCount = self.rowCount()
        columnCount = self.columnCount()
        for column in range(columnCount):
            for row in range(rowCount):
                item = QtGui.QTableWidgetItem('Text%d' % row)
                if column == 2:
                    item = QtGui.QTableWidgetItem()
                    item.setBackground(QtGui.QColor(255,0,0))
                    item.setFlags(QtCore.Qt.ItemIsEditable)
                    # item.setFlags(QtCore.Qt.ItemIsUserCheckable |
                    #               QtCore.Qt.ItemIsEnabled)
                    # item.setCheckState(QtCore.Qt.Unchecked)
                self.setItem(row, column, item)
        self.itemClicked.connect(self.handleItemClicked)
        self._clickCount = 0

    def handleItemClicked(self, item):
        self._list = []
        itemColumn = item.column()
        itemRow = item.row()
        itemLoc = [itemRow, itemColumn]
        # if item.checkState() == QtCore.Qt.Checked:
        #     print('"%s" Checked' % item.text())
        #     self._list.append(item.row())
        #     print(self._list)
        # else:
        if itemColumn == 2:
            print self._clickCount
            if self._clickCount == 0:
                print "Set Color Green"
                item.setBackground(QtGui.QColor(0,255,0))
            elif self._clickCount == 1:
                print "Set Color Blue"
                item.setBackground(QtGui.QColor(0,0,255))
            elif self._clickCount == 2:
                print "Set Color Red"
                item.setBackground(QtGui.QColor(255,0,0))
            else:
                pass
            self._clickCount += 1
            if self._clickCount > 2:
                self._clickCount = 0

            print ( '"%s" Clicked' % item.text() )
            self._list.append( itemLoc )
            print ( self._list )

class Window(QtGui.QWidget):
    def __init__(self, rows, columns):
        QtGui.QWidget.__init__(self)
        #self.table = QtGui.QTableWidget(rows, columns, self)
        self.table = Table()
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.table)


if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window(6, 3)
    window.resize(350, 300)
    window.show()
    sys.exit(app.exec_())
