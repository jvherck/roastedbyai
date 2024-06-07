# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Public License (jvherck on GitHub)

from importlib.util import find_spec

from .roasted import *
from .errors import *
from .models import *

__version__ = "1.3.0"

if find_spec("brotli") is None:
    raise ModuleNotFoundError("Package `brotli` is required but not found. Please install brotli first.")
