from __future__ import annotations
from py_objects.dao.gate_dao import GateDAO
from py_objects.dao.connection_dao import ConnectionDAO, IOPortDAO, IOPort
from PyQt6.QtWidgets import QGraphicsScene

from exceptions.object_existence_exception import ObjectExistsException

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from py_objects.signals.wire import Wire
    from py_objects.gates.gate import Gate

class Component:
    def __init__(self, name: str, architecture: str):
        # TODO: Write a function to open VHDL file and load the inputs and outputs
        self.name: str = name
        self.architecture: str = architecture
        self.gates: GateDAO = GateDAO()
        self.connections: ConnectionDAO = ConnectionDAO()
        self.io_ports: IOPortDAO = IOPortDAO()
        self.sub_components = []    # TODO: Create a sub-component class
        # self.behavioral_code: str = ""


    def create_gate(self, type_: str, scene_x: float=20, scene_y: float=20) -> None:
        self.gates.create(type_, scene_x, scene_y)

    def retrieve_component(self, key: str | int) -> Gate:
        if self.gates.search(key) is not None:
            return self.gates.search(key)
        
        # TODO: Make another DAO for sub-component and create another condition for that
        
        return None
        
    def generate_vhdl_code(self):
        placeholders = {
            "entity_name": self.name,
            "architecture_name": self.architecture,
            "port_declarations": self.io_ports.decode_to_vhdl(),
            "signal_declarations": self.connections.decode_to_vhdl(),
            "gate_operations": self.gates.decode_to_vhdl()
        }

        # Open the VHDL template
        with open("vhdl/template.vhd", 'r') as file:
            vhdl_template = file.read()

        return vhdl_template.format(**placeholders)

    def connect_wire(self, name: str, bit_size: int, 
                src_key: int | str, src_port: str, 
                dest_key: int | str, dest_port: str) -> None:
        
        # Check for any existing I/O ports
        if self.io_ports.search(name) is not None:
            raise ObjectExistsException(f"There's already an I/O signal with name '{name}'. Please try a different one.")
        
        # Create a wire
        self.connections.create(name, bit_size)

        # Connect the wire
        self.connections.search(name).connect(
            self.retrieve_component(src_key), src_port,
            self.retrieve_component(dest_key), dest_port
        )

    def add_port(self, name: str, bit_size: int, is_input: bool, scene_x: float=20, scene_y: float=20):

        # Check for any existing connections
        if self.connections.search(name) is not None:
            raise ObjectExistsException(f"There's already an connection with name '{name}'. Please try a different one.")
        
        # Create an I/O Port
        self.io_ports.create(name, bit_size, is_input, scene_x, scene_y)


    def connect_port(self, io_port: str, dest_key: int | str, dest_port: str) -> None:
        self.io_ports.search(io_port).connect(self.retrieve_component(dest_key), dest_port)

    def draw_all_internals(self, scene: QGraphicsScene) -> None:
        for gate in self.gates.list_items():
            gate.draw(scene)

        for port in self.io_ports.list_items():
            port.draw_port(scene)
            port.draw(scene)

        for wire in self.connections.list_items():
            wire.draw(scene)

    def export_dict(self):
        return {
            "__class__": "Component",
            "name": self.name,
            "architecture": self.architecture,
            "gates": self.gates.list_items(),
            "connections": self.connections.list_items(),
            "io_ports": self.io_ports.list_items()
        }


    