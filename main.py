from utils.parser import setup_parser_main
from app import app


if __name__ == "__main__":
    (known_args, pipeline_options) = setup_parser_main()

    # todo: implement no-op
    if known_args.no_op:
        exit()

    app.run(pipeline_options)
