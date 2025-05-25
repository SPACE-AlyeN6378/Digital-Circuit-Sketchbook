from py_objects.dao.dao import DataAccessObject
from exceptions.object_existence_exception import ObjectExistsException
from py_objects.signals.wire import Wire
from py_objects.signals.io_port import IOPort, IOPortAbstract

class ConnectionDAO(DataAccessObject):

    def __init__(self) -> None:
        """DAO Constructor"""
        self.wires: list[Wire] = []

    def __len__(self):
        return len(self.wires)

    def search(self, key: str) -> Wire:
        for wire in self.wires:
            if key == wire.name:
                return wire
            
        return None
    
    def create(self, name: str, bit_size: int) -> None:
        if self.search(name) is not None:
            raise ObjectExistsException(f"A signal with name '{name}' already exists")
        
        self.wires.append(Wire(name, bit_size))

    def retrieve(self, search_str: str=None, size: int=None) -> list[Wire]:
        if search_str is not None and size is not None:
            return list(filter(lambda wire: search_str in wire.name and size == wire.bit_size, self.wires))
        
        elif search_str is not None and size is None:
            return list(filter(lambda wire: search_str in wire.name, self.wires))
        
        elif search_str is None and size is not None:
            return list(filter(lambda wire: size == wire.bit_size, self.wires))
        
        else:
            raise AttributeError("None of the parameters are given")
        
    def list_items(self):
        return self.wires
    
    def decode_to_vhdl(self) -> str:
        """Generates lines of VHDL code for the wires with indentation"""
        indentation = max(map(len, [wire.name for wire in self.wires]))
        return ";\n    ".join([wire.decode_to_vhdl(indentation) for wire in self.wires]) + ';'
    

class IOPortDAO(DataAccessObject):

    def __init__(self, abstraction: bool=False) -> None:
        """DAO Constructor"""
        self.ports: list[IOPort] = []
        self.abstraction = abstraction

    def __len__(self):
        return len(self.ports)

    def search(self, key: str) -> IOPort:
        for port in self.ports:
            if key == port.name:
                return port
            
        return None
    
    def create(self, name: str, bit_size: int, is_input: bool, scene_x: float=20, scene_y: float=20) -> None:
        if self.search(name) is not None:
            raise ObjectExistsException(f"An I/O Port with name '{name}' already exists")
        
        # If a vector object is not allowed
        if not self.abstraction:
            self.ports.append(IOPort(name, bit_size, is_input, scene_x, scene_y))
        else:
            self.ports.append(IOPortAbstract(name, bit_size, is_input))
            

    def retrieve(self, search_str: str=None, size: int=None) -> list[Wire]:
        if search_str is not None and size is not None:
            return list(filter(lambda wire: search_str in wire.name and size == wire.bit_size, self.ports))
        
        elif search_str is not None and size is None:
            return list(filter(lambda wire: search_str in wire.name, self.ports))
        
        elif search_str is None and size is not None:
            return list(filter(lambda wire: size == wire.bit_size, self.ports))
        
        else:
            raise AttributeError("None of the parameters are given")
        
    def list_items(self):
        return self.ports
    
    # TODO: Rename this function from decode_to_vhdl to to_vhdl
    def decode_to_vhdl(self) -> str:
        """Generates lines of VHDL code for the I/O Ports with indentation"""
        indentation = max(map(len, [port.name for port in self.ports]))
        return ";\n        ".join([port.decode_to_vhdl(indentation) for port in self.ports])