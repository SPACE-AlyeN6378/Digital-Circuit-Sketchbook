from __future__ import annotations
from PyQt6.QtWidgets import QGraphicsScene
from graphics.connector import Connector
from py_objects.gates.gate import Gate

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from py_objects.components.component import Component

class Signal:

    def _size_to_vhdl(self):
        if self.bit_size > 1:
            return f"std_logic_vector({self.bit_size - 1} downto 0)" 
        else:
            return "std_logic"
        
    def __init__(self, name: str, size: int):
        """Constructor for the signal"""
        self.name = name
        self.bit_size = size
        self.src: Gate | Component | None = None
        self.src_port: str = None
        self.dests: list[tuple[str, Gate | Component]] = []
        self.connectors: list[Connector] = []

    def __str__(self):
        """Generates a line of VHDL code for the wire"""
        return f"undefined signal of length {self.bit_size}"
    
    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return str(self)
    
    def __connect_src(self, src: Component | Gate, port_name: str) -> None:
        """
        Connects the wire to the source component
        """
        if self.src is not None and self.src != src:
            raise ValueError(f"Source already connected to {self.src.name} on port {self.src_port}")
        
        if isinstance(src, Gate):
            if self.bit_size != 1:
                raise ValueError("Gates are compatible with single-bit wires/signals")
        
        if isinstance(src, Gate):
            src.connect(self, port_name)

        
        
        self.src = src
        self.src_port = port_name

    def _connect_dest(self, dest: Gate | Component, port_name: str) -> None:
        """
        Connects the wire to the destination component
        """
        if isinstance(dest, Gate):
            if self.bit_size != 1:
                raise ValueError("Gates are compatible with single-bit wires/signals")
            
        
        dest.connect(self, port_name)        
        self.dests.append((dest, port_name))

    def connect(self, src: Gate | Component, src_port: str, dest: Gate | Component, dest_port: str) -> None:
        
        self.__connect_src(src, src_port)
        self._connect_dest(dest, dest_port)

    def draw(self, scene: QGraphicsScene) -> None:
        # Draws a line connector to the scene
        for dest, dest_port in self.dests:
            connector = Connector(self.src.vector_item, self.src_port, dest.vector_item, dest_port)

            # Attach connector to gates so they notify it when moved
            self.src.vector_item.add_connector(connector, self.src_port)
            dest.vector_item.add_connector(connector, dest_port)
            self.connectors.append(connector)

            # Show it to scene
            scene.addItem(connector)

    def export_dict(self) -> dict:
        # Retrieve the key of the source
        if isinstance(self.src, Gate):
            src_key = self.src.id
        
        # elif isinstance(self.src, Component):
        # TODO: Make another 'if' condition for the subcomponent

        else:
            src_key = None

        # Retrieve the keys of the destination
        dest_keys = []
        for comp, dest_port in self.dests:
            if isinstance(comp, Gate):
                dest_keys.append((comp.id, dest_port))

            # elif isinstance(self.src, Component):
            # TODO: Make another 'if' condition for the subcomponent
        
        return {
            "__class__": "Signal",
            "name": self.name,
            "bit_size": self.bit_size,
            "src_key": src_key,
            "src_port": self.src_port,
            "dests": dest_keys
        }

