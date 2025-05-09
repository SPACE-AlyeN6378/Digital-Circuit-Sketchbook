from __future__ import annotations

from PyQt6.QtWidgets import QGraphicsPathItem, QGraphicsRectItem, QGraphicsEllipseItem
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QColor, QPen, QBrush

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from graphics.connector import Connector

class GraphicsItem(QGraphicsPathItem):
    def __init__(self):
        # Constants
        self.GRID_SIZE = 5
        self.DOT_RADIUS = 3.5

        super().__init__()
        self.port_pos: dict[str, QPointF] = dict()
        self.connectors: dict[str, list[Connector]] = dict()
        self.junction_dots: dict[str, QGraphicsEllipseItem] = dict()

        self._pen = QPen(QPen(QColor('black'), 2))

        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemSendsScenePositionChanges)

    def itemChange(self, change, value):

        if change == QGraphicsPathItem.GraphicsItemChange.ItemPositionHasChanged:
            for connector_list in self.connectors.values():
                for connector in connector_list:
                    connector.update_position()

        if change == QGraphicsPathItem.GraphicsItemChange.ItemPositionChange:
            # Snap to grid size
            x = round(value.x() / self.GRID_SIZE) * self.GRID_SIZE
            y = round(value.y() / self.GRID_SIZE) * self.GRID_SIZE

            return QPointF(x, y)
        
        return super().itemChange(change, value)
    
    def add_connector(self, connector: Connector, port_name: str) -> None:
        if port_name not in self.connectors:
            self.connectors[port_name] = []
            self.junction_dots[port_name] = None
            
        self.connectors[port_name].append(connector)
        self.add_junction_dot(port_name)

    def add_junction_dot(self, port_name: str) -> None:

        # If the junction dot doesn't exist, AND there is more than one connection
        if self.junction_dots[port_name] is None and len(self.connectors[port_name]) > 1:
            dot = QGraphicsEllipseItem(
                    self.port_pos[port_name].x() - self.DOT_RADIUS, 
                    self.port_pos[port_name].y() - self.DOT_RADIUS,
                    self.DOT_RADIUS * 2,
                    self.DOT_RADIUS * 2,
                    parent=self
                )
            
            dot.setBrush(QBrush(QColor('black')))
            dot.setPen(self._pen)

            self.junction_dots[port_name] = QGraphicsEllipseItem(parent=self)
            
    
class RectangularItem(QGraphicsRectItem):
    def __init__(self, parent):
        super().__init__(parent)

        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemSendsGeometryChanges)

    def itemChange(self, change, value):

        if change == QGraphicsRectItem.GraphicsItemChange.ItemPositionChange:

            # Snap to grid size
            grid_size = 10
            x = round(value.x() / grid_size) * grid_size
            y = round(value.y() / grid_size) * grid_size

            return QPointF(x, y)
        
        return super().itemChange(change, value)
