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
            return obj.export_dict()

        return super().default(obj)