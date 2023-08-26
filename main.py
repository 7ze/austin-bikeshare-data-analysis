from utils.parser import setup_parser_main
from app import app


if __name__ == "__main__":
    app.main(*setup_parser_main())
