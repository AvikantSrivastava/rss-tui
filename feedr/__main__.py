from .tui import RSSApp
from .utils import check_config_file, create_config_dir


def main():
    app = RSSApp()
    app.run()


if __name__ == "__main__":
    main()
