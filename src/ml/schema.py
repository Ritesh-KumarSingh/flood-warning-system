"""
Schema proxy — re-exports everything from the canonical copy in src/backend/schema.py.
This avoids duplicating the file while keeping 'from schema import ...' working
for all ML scripts that run from this directory.
"""

import os as _os
import sys as _sys
import importlib as _importlib

# Temporarily replace this module's entry so the backend schema can be found
_ML_DIR = _os.path.dirname(_os.path.abspath(__file__))
_SRC_DIR = _os.path.dirname(_ML_DIR)
_BACKEND_DIR = _os.path.join(_SRC_DIR, "backend")

# Remove the ML dir temporarily and add backend dir so 'schema' resolves to backend
_orig_path = _sys.path[:]
if _ML_DIR in _sys.path:
    _sys.path.remove(_ML_DIR)
_sys.path.insert(0, _BACKEND_DIR)

# Remove this proxy from sys.modules so the real schema can load
_self_module = _sys.modules.pop("schema", None)

try:
    _backend_schema = _importlib.import_module("schema")
finally:
    # Restore path and re-register this proxy
    _sys.path[:] = _orig_path

# Copy all public attributes from backend schema to this module
_this = _sys.modules[__name__] if __name__ in _sys.modules else _self_module
for _name in dir(_backend_schema):
    if not _name.startswith("_"):
        setattr(_this, _name, getattr(_backend_schema, _name))

# Re-register so future 'import schema' returns this module (with all attrs)
_sys.modules["schema"] = _this
