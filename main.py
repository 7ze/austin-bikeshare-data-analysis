from utils.parser import configure_parser
from app import app


if __name__ == "__main__":
    (known_args, pipeline_options) = configure_parser()

    # todo: implement no-op
    if known_args.no_op:
        exit()

    app.run(pipeline_options)
