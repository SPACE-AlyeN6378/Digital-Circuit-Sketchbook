from PyQt6.QtWidgets import QGraphicsLineItem, QGraphicsPathItem, QGraphicsEllipseItem
from graphics.graphical_object import GraphicsItem
from PyQt6.QtGui import QPainterPath, QColor, QPen, QBrush
from PyQt6.QtCore import QRectF, QPointF

class GateGraphics(GraphicsItem):

    # Decide between paths according to type
    def __draw_path(self, type: str):
        if type == "AND" or type == "NAND": 
            self.setPath(self.and_gate())
        elif type == "OR" or type == "NOR": 
            self.setPath(self.or_gate())
        elif type == "XOR" or type == "XNOR":
            self.setPath(self.or_gate())
            self.draw_xor_arc()
        elif type == "NOT":
            self.setPath(self.do_nothing_gate())

    def __init__(self, type: str, size: float):
        super().__init__()

        self.__size = size
        self.__brush = QBrush(QColor('silver'))

        self.__draw_path(type)
        self.setBrush(self.__brush)
        self.setPen(self._pen)
        self.draw_pins(type)
        self.draw_bubble(type)


    # Draws the AND gate on to the canvas
    def and_gate(self):
        path = QPainterPath()

        # Rounded portion
        arc_rect = QRectF(0, 0, self.__size, self.__size)

        path.moveTo(0, self.__size)
        path.lineTo(0, 0)
        path.lineTo(self.__size/2, 0)
        path.arcTo(arc_rect, 90, -180)
        path.lineTo(0, self.__size)

        return path
    
    def or_gate(self):
        path = QPainterPath()

        # Start at bottom left
        path.moveTo(0, self.__size)
        path.quadTo(self.__size * 0.7, self.__size * 0.95, self.__size, self.__size * 0.5)
        path.quadTo(self.__size * 0.7, self.__size * 0.05, 0, 0)
        path.quadTo(self.__size * 0.3, self.__size * 0.5, 0, self.__size)

        path.closeSubpath()

        return path
    
    def do_nothing_gate(self):
        path = QPainterPath()

        path.moveTo(0, 0 + self.__size)
        path.lineTo(self.__size, self.__size * 0.5)
        path.lineTo(0, 0)
        path.lineTo(0, self.__size)

        return path
    
    def draw_xor_arc(self):
        path = QPainterPath()
        path.moveTo(-self.__size * 0.1, self.__size)
        path.quadTo(self.__size * 0.2, self.__size * 0.5, -self.__size * 0.1, 0)

        xor_arc = QGraphicsPathItem(path, parent=self)
        xor_arc.setPen(self._pen)
    
    def draw_pins(self, type):
        
        # To extend the wires to reach the back of the OR gates
        extension = 0

        if type == "OR" or type == "NOR": extension = 0.095
        elif type == "XOR" or type == "XNOR": extension = -0.005
        
        # Adding the output wires
        leg = QGraphicsLineItem(self.__size, self.__size/2, self.__size + 30, self.__size/2, self)
        self.port_pos["out"] = QPointF(self.__size + 30, self.__size/2)

        # Adding the input wires
        if type == "NOT":
            arm = QGraphicsLineItem(-30, self.__size * 0.5, 0, self.__size * 0.5, self)
            self.port_pos["in1"] = QPointF(-30, self.__size * 0.5)

            for wire in [arm, leg]:
                wire.setPen(self._pen)

        else:
            arm1 = QGraphicsLineItem(-30, self.__size * 0.2, extension * self.__size, self.__size * 0.2, self)
            self.port_pos["in1"] = QPointF(-30, self.__size * 0.2)
            arm2 = QGraphicsLineItem(-30, self.__size * 0.8, extension * self.__size, self.__size * 0.8, self)
            self.port_pos["in2"] = QPointF(-30, self.__size * 0.8)

            # Set the pen color of the wires
            for wire in [arm1, arm2, leg]:
                wire.setPen(self._pen)
        
    def draw_bubble(self, type: str):
        # Parameters
        diameter = 0.15 * self.__size
        bubble_x = self.__size
        bubble_y = self.__size / 2

        if type.upper() in ["NAND", "NOR", "XNOR", "NOT"]:
            # Create a bubble
            bubble = QGraphicsEllipseItem(bubble_x, bubble_y - diameter / 2, diameter, diameter, parent=self)
            bubble.setBrush(QBrush(QColor('white')))
            bubble.setPen(self._pen)

