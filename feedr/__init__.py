from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("feedr")
except PackageNotFoundError:
    __version__ = "unknown"

from .config import config
