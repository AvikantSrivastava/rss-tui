import os
from .constants import CONFIG_DIR, CONFIG_PATH, CONFIG_CONTENT

def create_config_dir():
    os.makedirs(CONFIG_DIR, exist_ok=True)

def create_config_file():
    with open(CONFIG_PATH, 'w') as f:
        f.write(CONFIG_CONTENT)

def check_config_file():
    return os.path.exists(CONFIG_PATH)
