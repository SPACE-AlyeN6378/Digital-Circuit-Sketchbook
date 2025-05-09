import re

# Sometimes, a sub-component can be loaded from a VHDL file. Not necessarily from a JSON file.
# This regex is used to find the ports in a VHDL file. It can be used to load the component from a VHDL file.
# The regex is case-insensitive and matches the port name, direction (in, out, inout), and type (e.g., std_logic, std_logic_vector).


# Regex to find input and output ports in a VHDL file
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


# TODO: Create a sub-component class and implement the methods to load the component from either a JSON file or a VHDL file.
