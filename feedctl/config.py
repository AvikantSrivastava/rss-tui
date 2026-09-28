import logging
import os
import tomllib

from feedctl.constants import CONFIG_PATH


class Config:
    def __init__(self, path=CONFIG_PATH) -> None:
        self.path = path
        self.app = {}
        self.feeds = []
        self.reload()

    def reload(self) -> None:
        """Re-read the config file from disk.

        Called on startup and again on every refresh so edits to config.toml
        (adding, removing, or renaming feeds) take effect without restarting.
        """
        try:
            with open(self.path, "rb") as f:
                data = tomllib.load(f)
            self.app = data["app"]
            self.feeds = data["feeds"]
        except (KeyError, tomllib.TOMLDecodeError):
            raise ValueError("Invalid configuration file")
        except FileNotFoundError:
            logging.error(f"Config file not found at path: {self.path}")


config_path = os.environ.get("CONFIG_PATH", CONFIG_PATH)
config = Config(config_path)
