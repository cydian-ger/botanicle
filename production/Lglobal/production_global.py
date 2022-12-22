import sys
from typing import Dict, Any

from compiler.lcompiler.bottle import Bottle
from production.static.static import allowed_settings

Production = sys.modules[__name__]

Production.settings = None


def init_production(settings: Dict[str, Any], bottle: Bottle):
    if Production.settings is not None:
        raise RuntimeError("Variable already defined")

    settings: Dict[str, Any]
    # Remove all invalid settings
    for setting, value in settings.items():
        if setting not in allowed_settings:
            raise KeyError(f"User Setting '{setting}' is not an allowed User Setting.")

        if not isinstance(value, type(allowed_settings[setting])):
            raise ValueError(f"User Setting '{setting}' was provided the incorrect type <{type(value).__name__}>. "
                             f"Expected type <{type(allowed_settings[setting]).__name__}>.")

    # Write default values for all non specified settings
    for setting, value in allowed_settings.items():
        if setting not in settings:
            settings[setting] = value

    Production.settings = settings
