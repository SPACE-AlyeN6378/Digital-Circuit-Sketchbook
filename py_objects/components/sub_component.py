import re
from py_objects.dao.connection_dao import IOPortDAO
from py_objects.signals.io_port import IOPort
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
    def __init__(self, label: str, name: str, io_ports: list[dict[str, str | int]] = []):
        super().__init__(name, None)
        self.label: str = label
        self.io_ports: IOPortDAO = IOPortDAO(abstraction=True)
        self.add_ports(io_ports)
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


# Sometimes, a sub-component can be loaded from a VHDL file. Not necessarily from a JSON file.
# This regex is used to find the ports in a VHDL file. It can be used to load the component from a VHDL file.
# The regex is case-insensitive and matches the port name, direction (in, out, inout), and type (e.g., std_logic, std_logic_vector).


# Regex to find input and output ports in a VHDL file
if __name__ == "__main__":
        
    vhdl_port_regex = r"(?i)(?P<port_name>\w+)\s*:\s*(in|out|inout)\s+(?P<port_type>[\w\s\(\)]+);"

    # Example usage
    vhdl_code = """
    entity Example is
        Port (
            clk : in std_logic;
            rst : in std_logic;
            data_in : in std_logic_vector(7 downto 0);
            data_out : out std_logic_vector(7 downto 0);
        );
    end Example;
    """

    matches = re.finditer(vhdl_port_regex, vhdl_code)

    for match in matches:
        print(f"Port Name: {match.group('port_name')}, Direction: {match.group(2)}, Type: {match.group('port_type')}")



