from __future__ import annotations
from py_objects.gates.gate import Gate
from py_objects.signals.wire import Wire
from py_objects.signals.io_port import IOPort
from py_objects.components.component import Component
import json

class ComponentEncoder(json.JSONEncoder):
    def default(self, obj):
        # Gate
        if isinstance(obj, (Gate, Wire, IOPort, Component)):
            # TODO: When the subcomponent class is created, add the subcomponent in the isinstance check
            return obj.export_dict()

        return super().default(obj)

class ComponentDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        # Check if the object is a dictionary and contains the '__class__' key
        # If it does, we can assume it's a serialized object
        if '__class__' in obj:
            if obj['__class__'] == 'Component':
                # Initialize the component with the name and architecture
                component = Component(obj['name'], obj['architecture'])

                # Add the gates
                for gate in obj['gates']:
                    gate.pop('__class__', None)  # Ignores the __class__ key
                    gate['id_'] = gate.pop('id')  # Changes 'id' to 'id_'
                    gate['type_'] = gate.pop('type')  # Changes 'type' to 'type_'
                    # Now, we can create the gate
                    component.create_gate(**gate)
                
                # Add the subcomponents
                # TODO: Add the subcomponents here

                # Add the connections
                for connection in obj['connections']:
                    # Iterate over each destination
                    for dest in connection['dests']:
                        component.connect_wire(
                            connection['name'],
                            connection['bit_size'],
                            connection['src_key'],
                            connection['src_port'],
                            dest[0],
                            dest[1],
                        )

                # Add the I/O ports
                for io_port in obj['io_ports']:
                    dests = io_port.pop('dests')    # Extract the destinations
                    io_port.pop('__class__', None)  # Ignores the __class__ key

                    # Now, we can create the I/O port
                    component.add_port(**io_port)
                    
                    # Iterate over each destination, and connect it
                    for dest in dests:
                        component.connect_port(io_port['name'], dest[0], dest[1])
                    
                # Return the component
                return component
            
        return obj
