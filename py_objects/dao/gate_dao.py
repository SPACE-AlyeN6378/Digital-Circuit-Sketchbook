import json

from py_objects.dao.dao import DataAccessObject
from py_objects.gates.gate import Gate, ANDGate, ORGate, XORGate, NANDGate, NORGate, XNORGate, NOTGate
from py_objects.dao.helper import next_number

class GateDAO(DataAccessObject):

    def __init__(self) -> None:
        """DAO Constructor"""
        self.gates: list[Gate] = [] # type: ignore

    def __len__(self):
        return len(self.gates)

    def search(self, key: int) -> Gate:
        for gate in self.gates:
            if key == gate.id:
                return gate
            
        return None
    
    def get_all_ids(self) -> list[int]:
        return [gate.id for gate in self.gates]
    
    def create(self, type_: str, scene_x: float=20, scene_y: float=20, id_: int = None) -> None:
        new_id = next_number(self.get_all_ids()) if id_ is None else id_

        if type_.upper() == "AND": self.gates.append(ANDGate(new_id, scene_x, scene_y))
        elif type_.upper() == "OR": self.gates.append(ORGate(new_id, scene_x, scene_y))
        elif type_.upper() == "XOR": self.gates.append(XORGate(new_id, scene_x, scene_y))
        elif type_.upper() == "NAND": self.gates.append(NANDGate(new_id, scene_x, scene_y))
        elif type_.upper() == "NOR": self.gates.append(NORGate(new_id, scene_x, scene_y))
        elif type_.upper() == "XNOR": self.gates.append(XNORGate(new_id, scene_x, scene_y))
        elif type_.upper() == "NOT": self.gates.append(NOTGate(new_id, scene_x, scene_y))
        else:
            raise ValueError(f"Invalid type '{type_}'")
        
    def retrieve(self, type_: str):
        if type_.upper() == "AND": return [gate for gate in self.gates if isinstance(gate, ANDGate)]
        elif type_.upper() == "OR": return [gate for gate in self.gates if isinstance(gate, ORGate)]
        elif type_.upper() == "XOR": return [gate for gate in self.gates if isinstance(gate, XORGate)]
        elif type_.upper() == "NAND": return [gate for gate in self.gates if isinstance(gate, NANDGate)]
        elif type_.upper() == "NOR": return [gate for gate in self.gates if isinstance(gate, NORGate)]
        elif type_.upper() == "XNOR": return [gate for gate in self.gates if isinstance(gate, XNORGate)]
        elif type_.upper() == "NOT": return [gate for gate in self.gates if isinstance(gate, NOTGate)]
        else:
            raise ValueError(f"Invalid type '{type_}'")
        
    def list_items(self):
        return self.gates
    
    def decode_to_vhdl(self) -> str:
        """Generates lines of VHDL code for the I/O Port with indentation"""

        def max_length_output_name(gate: Gate) -> int:
            """Returns the maximum length of the signal name from the output. USED FOR INDENTATION PURPOSES!"""
            return max(map(lambda sig: len(sig.name), gate.out))
    
        indentation = max(map(lambda gate: max_length_output_name(gate), self.gates))
        return ";\n    ".join([gate.get_vhdl_operation(indentation) for gate in self.gates]) + ";"

# class GateEncoder(json.JSONEncoder):


