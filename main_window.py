from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsPathItem, QGraphicsLineItem, QGraphicsEllipseItem
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath, QColor, QPen, QBrush, QFont, QKeySequence, QShortcut
from PyQt6.QtCore import QSize, Qt, QRectF
from py_objects.components.component import Component
from py_objects.signals.io_port import IOPort
import os

from py_objects.components.component_json import ComponentEncoder, json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        view = QGraphicsView()
        scene = QGraphicsScene()
        scene.setBackgroundBrush(QBrush(Qt.GlobalColor.white))
        view.setScene(scene)

        self.setCentralWidget(view)
        self.resize(1000, 600)
        self.setMinimumSize(800, 600)
        self.setWindowTitle("Component Creator")

        # TEST: Creating a D-Latch ===================================================
        # TODO: Simulate the D-Latch below

        # dLatch.save("test_component.json")
        dLatch = Component.load("samples/DLatch.dcs.json")
        dLatch.draw_all_internals(scene)

        print(dLatch.gates.search(4).out)
        print(dLatch.gates.search(5).out)


    # def mouseMoveEvent(self, event):

    # def mouseReleaseEvent(self, event):

        

app = QApplication([])
window = MainWindow()
window.show()
app.exec()


