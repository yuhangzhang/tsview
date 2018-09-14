import sys

from PyQt5.QtWidgets import QWidget

from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFileDialog



from tsscene import TSScene
from tsasdf import TSASDF

class TSWindow(QWidget):
    def __init__(self):
        super(TSWindow,self).__init__()

        self.scene = TSScene()
        self.view = QGraphicsView(self.scene)


        self.filebutton = QPushButton("open file")
        self.filebutton.clicked.connect(self.openfile)




        layout = QHBoxLayout()
        layout.addWidget(self.view)

        buttonlayout = QVBoxLayout()
        buttonlayout.addWidget(self.filebutton)
        layout.addLayout(buttonlayout)


        self.setLayout(layout)
        self.setWindowTitle("TSView")

    def openfile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file','/g/data1/ha3/rakib/ausLAMP/Data/Output','asdf file (*.h5)')

        if len(fname[0])>0:
            self.scene.setdata(fname[0])




if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = TSWindow()
    widget.resize(1024, 768)
    widget.show()
    sys.exit(app.exec_())




