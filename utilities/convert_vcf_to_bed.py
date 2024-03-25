import os

PLINK_DIR_PATH = f"output/plink"


def create_directory(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def execute_command(command):
    os.system(command)


def convert(vcf_file, output_prefix):
    # check if it has already been done
    if not os.path.exists(PLINK_DIR_PATH):
        os.makedirs(PLINK_DIR_PATH)
    elif os.path.exists(PLINK_DIR_PATH) and os.listdir(PLINK_DIR_PATH):
        return

    convert_command = f"vcf_format_conversions.py --vcf {vcf_file} --out-prefix {PLINK_DIR_PATH}/{output_prefix} --out-format binary-ped"
    execute_command(convert_command)
