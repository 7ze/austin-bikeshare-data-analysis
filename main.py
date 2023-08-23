from argparse import ArgumentParser
from utils.logger import setup_logger


def main():
    logger = setup_logger()

    logger.debug("starting...")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
    logger.debug("exiting...")


if __name__ == "__main__":
    parser = ArgumentParser(
        description="austin bikeshare data analysis pipeline"
    )
    parser.add_argument(
        "-n",
        "--no-op",
        help="dry run, does not perform any operation, purely for debugging",
        action="store_true",
    )
    args = parser.parse_args()

    # todo: implement no-op
    if args.no_op:
        exit()

    main()
