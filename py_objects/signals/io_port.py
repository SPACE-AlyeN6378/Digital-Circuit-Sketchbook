from __future__ import annotations
from py_objects.signals.signal import Signal
from graphics.io_port_graphics import IOPortGraphics
from PyQt6.QtWidgets import QGraphicsScene

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from py_objects.gates.gate import Gate
    from py_objects.components.component import Component

class IOPort(Signal):

    def __generate_label(self) -> str:
        """PRIVATE: Generates label for the text"""
        last_bit = self.bit_size - 1
        return f"{self.name.upper()}[{last_bit}:0]"
    
    def __init__(self, name: str, size: int, is_input: bool, x: float=20, y: float=20) -> None:

        # Constants
        SIZE = 40

        super().__init__(name, size)
        self.is_input: bool = is_input
        self.vector_item = IOPortGraphics(self.__generate_label(), is_input, SIZE)
        self.vector_item.setPos(x, y)

    def __str__(self):
        """Generates a line of VHDL code for the I/O Port"""
        in_out = "in" if self.is_input else "out"
        return f"{self.name}: {in_out} {self._size_to_vhdl()}"
    
    def draw_port(self, scene: QGraphicsScene) -> None:
        """Draws a diagram of the I/O"""
        scene.addItem(self.vector_item)

    def connect(self, dest: Gate | Component, dest_port: str):
        """Connects the input to a port"""
        return super().connect(self, "out", dest, dest_port)
    
    def decode_to_vhdl(self, indentation: int) -> str:
        """Generates a line of VHDL code for the I/O Port with indentation"""
        in_out = "in" if self.is_input else "out"
        first_spacing = ' ' * (indentation - len(self.name))
        second_spacing = ' ' * (4 - len(in_out))
        return f"{self.name}{first_spacing} : {in_out}{second_spacing}{self._size_to_vhdl()}"

    def export_dict(self):
        main_dict = super().export_dict()
        main_dict.update({
            "__class__": "IOPort",
            "is_input": self.is_input
        })
        main_dict.pop("src_key")
        main_dict.pop("src_port")
        
        return main_dict