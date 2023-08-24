from argparse import ArgumentParser


def configure_parser():
    parser = ArgumentParser(description="austin bikeshare data analysis pipeline")
    parser.add_argument(
        "-n",
        "--no-op",
        help="dry run, does not perform any operation, purely for debugging",
        action="store_true",
    )
    args = parser.parse_known_args()
    return args
