import argparse
import os


def parser_confirm_file():
    """Custom action to confirm file exists"""

    class customAction(argparse.Action):
        def __call__(self, parser, args, value, option_string=None):
            if not os.path.isfile(value):
                raise IOError("%s not found" % value)
            setattr(args, self.dest, value)

    return customAction


def check_params(args):
    if not any(
        analysis in args.analyses
        for analysis in ["sfs", "generic_stats", "fsc", "ima", "pixy"]
    ):
        raise IOError(
            "Must run Population Structure Analysis in order to run any of the other analyses."
        )
    return


def get_analyses_choices():
    return [
        "hwe",
        "pop_structure",
        "sfs",
        "generic_stats",
        "fsc",
        "pixy",
        "ima",
        "f_stats",
    ]


def parse():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Required Input Args
    parser.add_argument(
        "--vcf",
        help="Path to the vcf file",
        type=str,
        required=True,
        action=parser_confirm_file(),
    )

    # Summary Stats Analysis Args
    parser.add_argument(
        "--analyses",
        nargs="+",
        choices=get_analyses_choices(),
        help="List of analyses to run from the VCF, separated by spaces.\ne.g. '--stats hwe generic' will result in Hardy Weinberg and generic summary statistic calculations.",
        required=True,
    )

    # Optional Args
    parser.add_argument(
        "--out-prefix",
        help="Defines the output prefix (without the file extention)",
        type=str,
        default="out",
    )
    parser.add_argument(
        "--statistic-window-size",
        help="Defines the statistic window size, defaults to 10000",
        type=int,
        default=10000,
    )
    parser.add_argument(
        "--subpops-to-test",
        help="Defines the number of subpopulations to test for population structure. Defaults to 10",
        type=int,
        default=10
    )
    parser.add_argument(
        "--p-val",
        help="Defines p value to be used with Hardy Weinberg Tests. Defaults to 0.05",
        type=int,
        default=0.05
    )

    check_params(parser.parse_args())
    return parser.parse_args()
