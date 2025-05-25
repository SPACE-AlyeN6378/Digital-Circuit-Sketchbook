from __future__ import annotations
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsScene
from graphics.gate_graphics import GateGraphics
from PyQt6.QtCore import QPointF

from exceptions.illegal_operation_exception import IllegalOperationException

if TYPE_CHECKING:
    from py_objects.signals.wire import Wire
    from py_objects.signals.io_port import IOPort

# ================================================================================= #

class Gate:
    # Constants
    SIZE = 50

    # Constructor
    def __init__(self, id_: int) -> None:
        self.id: int = id_
        self.in1: Wire = None
        self.in2: Wire = None
        self.out: Wire | IOPort = []
        self.vector_item: GateGraphics = None
        self.vhdl_op: str = "NULL"

    def __str__(self) -> str:
        gate_name = self.vhdl_op.upper() if self.vhdl_op is not None else "GATE"
        return f"{gate_name}{self.id:04d}"
    
    def __repr__(self) -> str:
        return str(self)
    
    def __eq__(self, other) -> bool:
        return self.id == other.id and self.vhdl_op == other.vhdl_op

    def check_connections(self) -> None:
        """
        Checks for any disconnected wires in the gate
        """
        if any(wire is None for wire in [self.in1, self.in2, self.out]):
            print(f"WARNING! One or more wires are disconnected in gate {self}")
            return False
        
        return True
    
    def __connect_input1(self, wire: Wire) -> None:
        if self.in1 is not None:
            raise IllegalOperationException(f"Input 1 is already connected in gate {self}.")
        
        self.in1 = wire
    
    def __connect_input2(self, wire: Wire) -> None:
        if self.in2 is not None:
            raise IllegalOperationException(f"Input 2 is already connected in gate {self}.")
        
        self.in2 = wire

    def __connect_output(self, wire: Wire | IOPort) -> None:
        if wire not in self.out:
            self.out.append(wire)
            
    def connect(self, wire: Wire, port: str) -> None:
        """
        Connects the gate to a wire.
        If the gate is NOT, it will only connect to input 1.
        """
        if port == "in1":
            self.__connect_input1(wire)
        elif port == "in2":
            if self.vhdl_op == "not":
                raise IllegalOperationException("Input 2 is ignored for NOT Gate, so it's not permitted. Please use Input 1.")
            self.__connect_input2(wire)
        elif port == "out":
            self.__connect_output(wire)
        else:
            raise IllegalOperationException(f"Invalid port '{port}' for gate {self.name}. Valid ports are 'in1', 'in2', and 'out'.")

    def draw(self, scene: QGraphicsScene) -> None:
            scene.addItem(self.vector_item)

    def setPos(self, x: float, y: float) -> None:
        self.vector_item.setPos(x, y)

    def get_vhdl_operation(self, indentation: int) -> str:
        """Converts to a stringified line of VHDL code"""
        code_lines = []
        operation = f"{self.vhdl_op} {self.in1.name}" if self.vhdl_op == "not" else f"{self.in1.name} {self.vhdl_op} {self.in2.name}"

        # If more than one outputs are being distributed
        if len(self.out) > 1:
            # Retrieve the wire
            wire = [output for output in self.out if "signal" in str(output)][0]

            # Iterate through each signal
            for output in self.out:
                # If one of them is carried by a wire
                spacing = ' ' * (indentation - len(output.name))
                if output == wire:
                    code_lines.append(f"{output.name}{spacing} <= {operation}")
                # The others are outputted directly from that wire above
                else:
                    code_lines.append(f"{output.name}{spacing} <= {wire.name}")

            return ";\n    ".join(code_lines)

        spacing = ' ' * (indentation - len(self.out[0].name))
        return f"{self.out[0].name}{spacing} <= {operation}"

    def pos(self) -> QPointF:
        return self.vector_item.scenePos()

    def export_dict(self):
        return {
            "__class__": "Gate",
            "id": self.id,
            "type": self.vhdl_op.upper(),
            "scene_x": self.pos().x(),
            "scene_y": self.pos().y()
        }        
# ================================================================================= #

class ANDGate(Gate):
    def __init__(self, id_: int, scene_x: float=20, scene_y: float=20) -> None:
        """AND Gate Constructor"""
        super().__init__(id_)
        self.vhdl_op = "and"
        self.vector_item = GateGraphics(self.vhdl_op.upper(), Gate.SIZE)
        self.setPos(scene_x, scene_y)
    

class ORGate(Gate):
    def __init__(self, id_: int, scene_x: float=20, scene_y: float=20) -> None:
        """OR Gate Constructor"""
        super().__init__(id_)
        self.vhdl_op = "or"
        self.vector_item = GateGraphics(self.vhdl_op.upper(), Gate.SIZE)
        self.setPos(scene_x, scene_y)


class XORGate(Gate):
    def __init__(self, id_: int, scene_x: float=20, scene_y: float=20) -> None:
        """XOR Gate Constructor"""
        super().__init__(id_)
        self.vhdl_op = "xor"
        self.vector_item = GateGraphics(self.vhdl_op.upper(), Gate.SIZE)
        self.setPos(scene_x, scene_y)


class NANDGate(Gate):
    def __init__(self, id_: int, scene_x: float=20, scene_y: float=20) -> None:
        """NAND Gate Constructor"""
        super().__init__(id_)
        self.vhdl_op = "nand"
        self.vector_item = GateGraphics(self.vhdl_op.upper(), Gate.SIZE)
        self.setPos(scene_x, scene_y)


class NORGate(Gate):
    def __init__(self, id_: int, scene_x: float=20, scene_y: float=20) -> None:
        """NOR Gate Constructor"""
        super().__init__(id_)
        self.vhdl_op = "nor"
        self.vector_item = GateGraphics(self.vhdl_op.upper(), Gate.SIZE)
        self.setPos(scene_x, scene_y)


class XNORGate(Gate):
    def __init__(self, id_: int, scene_x: float=20, scene_y: float=20) -> None:
        """XNOR Gate Constructor"""
        super().__init__(id_)
        self.vhdl_op = "xnor"
        self.vector_item = GateGraphics(self.vhdl_op.upper(), Gate.SIZE)
        self.setPos(scene_x, scene_y)


class NOTGate(Gate):
    def __init__(self, id_: int, scene_x: float=20, scene_y: float=20) -> None:
        """NOT Gate Constructor"""
        super().__init__(id_)
        self.vhdl_op = "not"
        self.vector_item = GateGraphics(self.vhdl_op.upper(), Gate.SIZE)
        self.setPos(scene_x, scene_y)

    def check_connections(self) -> None:
        """
        Checks for any disconnected wires in the gate
        """
        if any(wire is None for wire in [self.in1, self.out]):  # Since there's one input, input2 is ignored
            print(f"WARNING! One or more wires are disconnected in gate {self.name}")
            return False
        
        return True
        
    def connect_input2(self, wire: Wire) -> None:
        raise IllegalOperationException("Input 2 is ignored for NOT Gate, so it's not permitted. Please use Input 1.")
        
    def to_vhdl(self):
        """Converts to a stringified line of VHDL code"""
        return f"{self.out.name} <= {self.vhdl_op} {self.in1.name}"
        