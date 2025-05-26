from __future__ import annotations
from py_objects.dao.gate_dao import GateDAO
from py_objects.dao.connection_dao import ConnectionDAO, IOPortDAO
from PyQt6.QtWidgets import QGraphicsScene
import os

from exceptions.object_existence_exception import ObjectExistsException

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from py_objects.signals.wire import Wire
    from py_objects.gates.gate import Gate

class Component:
    def __init__(self, name: str, architecture: str):
        self.name: str = name
        self.architecture: str = architecture
        self.gates: GateDAO = GateDAO()
        self.connections: ConnectionDAO = ConnectionDAO()
        self.io_ports: IOPortDAO = IOPortDAO()
        self.sub_components = []    # TODO: Create a sub-component class
        # self.behavioral_code: str = ""

        # Filename and directory
        self.filename = ""
        self.directory = ""

    def __str__(self):
        return f"{self.name}: {self.architecture}"
    
    def __repr__(self):
        return str(self)
    
    def create_gate(self, type_: str, scene_x: float=20, scene_y: float=20, id_: int = None) -> None:
        self.gates.create(type_, scene_x, scene_y, id_)

    def retrieve_object(self, key: str | int):
        # Import here to avoid circular import
        from py_objects.gates.gate import Gate
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
            self.retrieve_object(src_key), src_port,
            self.retrieve_object(dest_key), dest_port
        )

    def add_port(self, name: str, bit_size: int, is_input: bool, scene_x: float=20, scene_y: float=20) -> None:

        # Check for any existing connection names
        if self.connections.search(name) is not None:
            raise ObjectExistsException(f"There's already an connection with name '{name}'. Please try a different one.")
        
        # Create an I/O Port
        self.io_ports.create(name, bit_size, is_input, scene_x, scene_y)

    def connect_port(self, io_port: str, dest_key: int | str, dest_port: str) -> None:
        self.io_ports.search(io_port).connect(self.retrieve_object(dest_key), dest_port)

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

    def save(self, filename: str) -> None:
        """Saves the component to a JSON file"""
        # Import here to avoid circular import
        from py_objects.components.component_json import ComponentEncoder, json
        
        # Save the json file
        with open(filename, 'w') as file:
            json.dump(self.export_dict(), file, cls=ComponentEncoder, indent=4)

        self.json_filename = os.path.basename(filename)
        self.directory = os.path.dirname(filename)

        vhdl_filename = os.path.join(self.directory, f"{self.name}.vhd")

        # Save the VHDL file in the same directory as the JSON file
        with open(vhdl_filename, 'w') as vhdl_file:
            vhdl_file.write(self.generate_vhdl_code())
            

    @staticmethod
    def load(filename: str) -> Component:
        """Loads a component from a JSON file"""
        # Import here to avoid circular import
        from py_objects.components.component_json import ComponentDecoder, json
        
        with open(filename, 'r') as file:
            component = json.load(file, cls=ComponentDecoder)
            component.json_filename = os.path.basename(filename)
            component.directory = os.path.dirname(filename)

            return component
    