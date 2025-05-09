from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsPathItem, QGraphicsLineItem, QGraphicsEllipseItem
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath, QColor, QPen, QBrush, QFont, QKeySequence, QShortcut
from PyQt6.QtCore import QSize, Qt, QRectF
from py_objects.components.component import Component
from py_objects.signals.io_port import IOPort

from py_objects.components.component_json import ComponentEncoder, json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        view = QGraphicsView()
        scene = QGraphicsScene()
        view.setScene(scene)

        self.setCentralWidget(view)
        self.resize(1000, 600)
        self.setMinimumSize(800, 600)

        # TEST: Creating a D-Latch ====================================================

        dLatch = Component("DLatch", "dataflow")

        dLatch.create_gate('NAND', 100, 80)
        dLatch.create_gate('NOT', -50, 215)
        dLatch.create_gate('NAND', 100, 200)
        dLatch.create_gate('NAND', 350, 65)
        dLatch.create_gate('NAND', 350, 215)
        

        dLatch.add_port('D', 1, True, -150, 80)
        dLatch.connect_port('D', dest_key=1, dest_port='in1')
        dLatch.connect_port('D', dest_key=2, dest_port='in1')
        dLatch.connect_wire('Dbar', 1, src_key=2, src_port='out', dest_key=3, dest_port='in2')

        dLatch.add_port('EN', 1, True, 0, 155)
        dLatch.connect_port('EN', dest_key=1, dest_port='in2')
        dLatch.connect_port('EN', dest_key=3, dest_port='in1')

        dLatch.connect_wire('R', 1, src_key=1, src_port='out', dest_key=4, dest_port='in1')
        dLatch.connect_wire('S', 1, src_key=3, src_port='out', dest_key=5, dest_port='in2')

        dLatch.connect_wire("Q_int", 1, src_key=4, src_port='out', dest_key=5, dest_port='in1')
        dLatch.connect_wire("Qbar_int", 1, src_key=5, src_port='out', dest_key=4, dest_port='in2')

        dLatch.add_port('Q', 1, False, 520, 80)
        dLatch.connect_port('Q', dest_key=4, dest_port='out')

        dLatch.add_port('Qbar', 1, False, 520, 230)
        dLatch.connect_port('Qbar', dest_key=5, dest_port='out')
        
        dLatch.draw_all_internals(scene)
        # TODO: Compile the above test component into a VHDL code and simulate it

    
    # def mouseMoveEvent(self, event):

    # def mouseReleaseEvent(self, event):

        

app = QApplication([])
window = MainWindow()
window.show()
app.exec()


