from py_objects.signals.signal import Signal

class Wire(Signal):
    
    def __init__(self, name: str, size: int):
        """Wire Constructor"""
        super().__init__(name, size)

    
    def __str__(self):
        """Generates a line of VHDL code for the wire"""
        # if self.type == "in" or self.type == "out":
        #     return f"{self.name}: {self.type} {self.__size_to_vhdl()}"
        # else:
        return f"signal {self.name}: {self._size_to_vhdl()}"
    
    def decode_to_vhdl(self, indentation: int) -> str:
        """Generates a line of VHDL code for the I/O Port with indentation"""
        first_spacing = ' ' * (indentation - len(self.name))
        return f"signal {self.name}{first_spacing} : {self._size_to_vhdl()}"
    
    def export_dict(self):
        main_dict = super().export_dict()
        main_dict["__class__"] = "Wire"
        return main_dict

if __name__ == "__main__":
    signal = Wire("in", "bridge", 5)
    print(signal)
