import os
import platform

APP_NAME = "feedr"

system = platform.system()
if system == "Linux":
    base = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
elif system == "Darwin":  # macOS
    base = os.path.expanduser("~/Library/Application Support")
elif system == "Windows":
    base = os.getenv("APPDATA")
else:
    base = os.path.expanduser("~")

CONFIG_DIR = os.path.join(base, APP_NAME)
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.toml")
CONFIG_CONTENT = '''
[ui]
theme = "default"

[[feeds]]
name = "Hacker News"
url = "https://news.ycombinator.com/rss"

[[feeds]]
name = "Reddit Programming"
url = "https://www.reddit.com/r/programming/.rss"
'''
