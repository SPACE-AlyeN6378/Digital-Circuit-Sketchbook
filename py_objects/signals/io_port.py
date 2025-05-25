from __future__ import annotations
from exceptions.illegal_operation_exception import IllegalOperationException
from py_objects.signals.signal import Signal
from graphics.io_port_graphics import IOPortGraphics
from PyQt6.QtWidgets import QGraphicsScene

from exceptions.bitsizemismatch_exception import BitSizeMismatchException
from exceptions.object_existence_exception import ObjectExistsException

from typing import TYPE_CHECKING

from py_objects.signals.wire import Wire

if TYPE_CHECKING:
    from py_objects.gates.gate import Gate
    from py_objects.components.component import Component


class IOPortAbstract:
    """
    Abstract class for I/O Ports used in sub-components for port mapping.

    This class serves as a base for creating input and output ports that belong to sub-components
    within a larger digital circuit. These ports are used for port mapping when integrating
    sub-components into higher-level designs. It provides methods to generate VHDL code,
    connect to other components, and manage graphical representation.
    """
    def __init__(self, name: str, size: int, is_input: bool) -> None:
        self.name: str = name
        self.bit_size: int = size
        self.is_input: bool = is_input
        self.mapped_wire: Wire = None
        self.mapped_port: IOPort = None

    def __str__(self):
        """Generates a line of VHDL code for the I/O Port"""
        signal = self.mapped_port.name if self.mapped_port is not None else "undefined"
        signal = self.mapped_wire.name if self.mapped_wire is not None else signal
        return f"{self.name} => {signal}"
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self, other):
        self.name == other.name and self.bit_size == other.bit_size
    
    def connect(self, signal: Wire | IOPort | IOPortAbstract) -> None:
        """
        Connects the I/O port to a signal or another I/O port.

        Args:
            signal (Wire | IOPort): The signal or I/O port to connect to.
        """
        # 1. Make sure that the bit size of the signal matches the port
        if signal.bit_size != self.bit_size:
                raise BitSizeMismatchException("Bit size mismatch")
        
        # 2. Only one signal can be connected to an input port
        if self.is_input:       
            if signal.mapped_port is not None or signal.mapped_wire is not None:
                raise IllegalOperationException("Input port already connected")
        
        # For wires, check if the signal is already connected to another port
        if isinstance(signal, Wire):
            # 3. Same wire should be connected to the same port
            if self.mapped_wire != signal:
                raise IllegalOperationException("Another wire is already connected. Please use the same wire.")
            
            if self.mapped_wire is None:
                self.mapped_wire = signal

        elif isinstance(signal, (IOPort, IOPortAbstract)):
            # 4. Check if the signal is connecting to the same type of port
            if not (self.mapped_port.is_input ^ signal.is_input):
                raise IllegalOperationException("Cannot connect input to input or output to output")
            
            # 5. Check if the signal is already connected to another port
            if signal.mapped_port is not None:
                raise IllegalOperationException("Another port is already connected")
            
            self.mapped_port = signal


class IOPort(Signal):

    def __generate_label(self) -> str:
        """PRIVATE: Generates label for the text"""
        last_bit = self.bit_size - 1
        return f"{self.name.upper()}[{last_bit}:0]"
    
    def __init__(self, name: str, size: int, is_input: bool, x: float=20, y: float=20) -> None:

        # Constants
        SIZE = 40      # Vector object size

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
            "is_input": self.is_input,
            "scene_x": self.vector_item.pos().x(),
            "scene_y": self.vector_item.pos().y()
        })
        main_dict.pop("src_key")
        main_dict.pop("src_port")
        
        return main_dict