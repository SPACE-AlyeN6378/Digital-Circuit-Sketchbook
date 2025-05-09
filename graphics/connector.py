from PyQt6.QtWidgets import QGraphicsLineItem
from PyQt6.QtCore import QLineF, QPointF
from PyQt6.QtGui import QPen, QColor
from graphics.graphical_object import GraphicsItem

class Connector(QGraphicsLineItem):
    def __init__(self, src: GraphicsItem, src_port: str, dest: GraphicsItem, dest_port: str):
        super().__init__()
        self.src = src
        self.dest = dest

        # Get scene positions of the source output pin and destination input pin
        self.source_offset = src.port_pos[src_port]
        self.dest_offset = dest.port_pos[dest_port]
        
        self.black_pen = QPen(QColor('black'), 2)
        self.blue_pen = QPen(QColor('blue'), 2)

        self.setPen(self.black_pen)
        
        # Update whenever the gate moves
        self.update_position()

    def update_position(self):
        source_pos = self.src.mapToScene(self.source_offset)
        dest_pos = self.dest.mapToScene(self.dest_offset)

        self.setLine(QLineF(source_pos, dest_pos))

    def eventFilter(self, watched, event):
        # Update the line when either gate is moved
        if event.type().name == "GraphicsSceneMouseMove":
            self.update_position()
        return False

