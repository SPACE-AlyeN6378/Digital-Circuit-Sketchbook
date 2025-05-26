import re
import os

from py_objects.dao.connection_dao import IOPortDAO
from py_objects.components.component import Component

class SubComponent(Component):
    """
    Represents a reusable sub-component within a larger digital circuit component.

    A SubComponent encapsulates a specific functionality and is structurally instantiated
    inside another component. It is defined by its name, a list of ports for interfacing,
    and an filename in JSON and/or VHDL. The ports are used for VHDL port mapping,
    enabling integration of the sub-component into the parent component's architecture.
    """
    # TODO: Finish this code

    # ========== Private Functions ==========
    # Some helpful regex functions to extract sections and ports from the VHDL code
    @staticmethod
    def __get_entity_section(vhdl_code: str) -> str:
        """
        Extracts the entity section from the VHDL code.

        Args:
            vhdl_code (str): The VHDL code as a string.

        Returns:
            str: The entity section of the VHDL code.
        """
        entity_regex = r"(?i)entity\s+(\w+)\s+is(.*?)end\s+\1;"
        match = re.search(entity_regex, vhdl_code, re.DOTALL)
        if match:
            return match.group(0)
        return ""
    
    @staticmethod
    def _get_bit_size_from_type(port_type: str) -> int:
        """
        Extracts the bit size from a port type string.

        Args:
            port_type (str): The port type string (e.g., 'std_logic_vector(7 downto 0)').

        Returns:
            int: The bit size of the port.
        """
        std_logic_vector_regex = r"std_logic_vector\((\d+)\s+downto\s+\d+\)"
        match = re.search(std_logic_vector_regex, port_type)
        if match:
            return int(match.group(1)) + 1
        else:
            return 1


    # ========== Public Functions ==========
    def __init__(self, label: str, name: str, io_ports: list[dict[str, str | int]] = []):
        super().__init__(name, None)
        self.label: str = label
        self.io_ports: IOPortDAO = IOPortDAO(abstraction=True)
        self.add_ports(io_ports)
        self.vhdl_filename = ""
        self.vector_item = None     # TODO: Create a graphics item for the sub-component

        # The following attributes are deleted and ignored
        del self.architecture
        del self.gates
        del self.connections
        del self.sub_components


    def add_port(self, name: str, bit_size: int, is_input: bool) -> None:
        self.io_ports.create(name, bit_size, is_input)

    def add_ports(self, ports: list[dict[str, str | int]]) -> None:
        """
        Adds multiple ports to the sub-component.

        Args:
            ports (list[dict[str, str | int]]): A list of dictionaries representing the ports to be added.
                Each dictionary should contain 'name', 'bit_size', and 'is_input' keys.
        """
        for port in ports:
            self.add_port(**port)

    @staticmethod
    def load_from_vhdl(filename: str, label: str):
        """
        Sometimes, a sub-component can be loaded from a VHDL file. Not necessarily from a JSON file.
        This regex is used to find the ports in a VHDL file. It can be used to load the component
        from a VHDL file. The regex is case-insensitive and matches the port name, direction (in, out, inout), 
        and type (e.g., std_logic, std_logic_vector).
        
        This function loads the sub-component from a VHDL file.

        Args:
            filename (str): The path to the VHDL file.
        """
        
        # Some regex patterns
        port_regex = r"^\s*([\w\s,]+):\s*(in|out|inout)\s+([\w_]+(?:\s*\([\w\s<>:=]+\))?)"
        entity_name_regex = r"(?i)entity\s+(\w+)\s+is"

        # Make a new instance of the SubComponent class

        # Read the VHDL file
        with open(filename, 'r') as file:
            vhdl_code = file.read()

            # Extract the entity section from the VHDL code
            entity_section = SubComponent.__get_entity_section(vhdl_code)

            if not entity_section:
                raise ValueError("No entity section found in the VHDL file.")
            
        # Initialize the SubComponent with the label
        sub_component = SubComponent(label, None)
        sub_component.vhdl_filename = os.path.basename(filename)
        sub_component.directory = os.path.dirname(filename)

        for line in entity_section.splitlines():
            port_match = re.match(port_regex, line)
            entity_name_match = re.search(entity_name_regex, vhdl_code)

            # Find matches for the port regex in the entity section
            # If a match is found, extract the port name, direction, and type
            if port_match:
                port_names = [name.strip() for name in port_match.group(1).strip().split(',')]
                direction = port_match.group(2).strip() == 'in'
                port_type = port_match.group(3).strip()
                bit_size = SubComponent._get_bit_size_from_type(port_type)

                for port_name in port_names:
                    # Print or process the port information
                    # Here we just print it, but you can modify this to store it in a data structure

                    # print(f"Port Name: {port_name}, Direction: {'Input' if direction else 'Output'}, Bit size: {bit_size}")
                    sub_component.add_port(port_name, bit_size, direction)

            elif entity_name_match:
                # If an entity name match is found, print the entity name
                sub_component.name = entity_name_match.group(1)
                
        return sub_component

    @staticmethod
    def load_from_json(filename: str, label: str):
        """
        Loads the sub-component from a JSON file.

        Args:
            filename (str): The path to the JSON file.
            label (str): The label for the sub-component.
        """
        from py_objects.components.component_json import SubComponentDecoder, json

        with open(filename, 'r') as file:
            sub_component = json.load(file, cls=SubComponentDecoder)
            sub_component.label = label
            sub_component.directory = os.path.dirname(filename)
            sub_component.json_filename = os.path.basename(filename)

            # Assuming that the JSON and VHDL filenames have the same name in the same location
            sub_component.vhdl_filename = sub_component.json_filename.replace('.dcs.json', '.vhd')

            return sub_component     




