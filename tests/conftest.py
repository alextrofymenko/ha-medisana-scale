"""Make the integration's pure modules importable without Home Assistant.

The package's __init__.py imports Home Assistant, so the packages are
registered as plain namespaces pointing at their directories instead.
"""
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

for name, path in (
    ("custom_components", ROOT / "custom_components"),
    ("custom_components.medisana", ROOT / "custom_components" / "medisana"),
):
    package = types.ModuleType(name)
    package.__path__ = [str(path)]
    sys.modules.setdefault(name, package)
