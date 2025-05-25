from PyQt6.QtWidgets import QGraphicsLineItem, QGraphicsPathItem, QGraphicsTextItem
from graphics.graphical_object import GraphicsItem
from PyQt6.QtGui import QPainterPath, QColor, QPen, QBrush
from PyQt6.QtCore import  QPointF

class IOPortGraphics(GraphicsItem):

    def __init__(self, label: str, is_input: bool, size: float):
        super().__init__()

        self.width = size
        self.height = size / 2
        self.label = QGraphicsTextItem(label, parent=self)

        self.is_input = is_input
        self.__color = QColor('blue') if is_input else QColor('red')
        self.__brush = QBrush(self.__color)
        self.__pen = QPen(QPen(QColor('black'), 2))

        self.setPath(self.__path())
        self.setBrush(self.__brush)
        self.setPen(self.__pen)
        self.draw_pin()
        self.add_label()

    def __path(self) -> QGraphicsPathItem:
        path = QPainterPath()

        if self.is_input:
            path.moveTo(0, self.height)
            path.lineTo(self.width * 0.75, self.height)
            path.lineTo(self.width, self.height * 0.5)
            path.lineTo(self.width * 0.75, 0)
            path.lineTo(0, 0)
            path.lineTo(0, self.height)

        else:
            path.moveTo(self.width, self.height)
            path.lineTo(self.width * 0.25, self.height)
            path.lineTo(0, self.height * 0.5)
            path.lineTo(self.width * 0.25, 0)
            path.lineTo(self.width, 0)
            path.lineTo(self.width, self.height)

        return path
    
    def draw_pin(self) -> None:
        """Draw the pins"""

        # Adding the output wire
        if self.is_input:
            pin = QGraphicsLineItem(self.width, self.height/2, self.width + 30, self.height/2, self)
            self.port_pos["out"] = QPointF(self.width + 30, self.height/2)
        
        else:
            pin = QGraphicsLineItem(0, self.height/2, -30, self.height/2, self)
            self.port_pos["out"] = QPointF(-30, self.height/2)
        
        pin.setPen(self.__pen)

    def add_label(self) -> None:
        self.label.setPos(0, -self.height - 3)
        self.label.setDefaultTextColor(QColor('black'))

