import os

OUTPUT_DIR = "output"
STATS_DIR = f"{OUTPUT_DIR}/stats"
PIXY_DIR = f"{STATS_DIR}/pixy"

def execute_command(command_list):
    command = " ".join(command_list)
    os.system(command)


def create_directory(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def compute_statistics(vcf_file, pop_file, output_prefix, window_size=None, bed_file=None):
    stat_command = [
        "pixy",
        f"--vcf {vcf_file}",
        f"--stats pi fst dxy",
        f"--populations {pop_file}"
    ]
    if window_size: stat_command.append(f"--window_size {window_size}")
    elif bed_file: stat_command.append(f"--bed_file {bed_file}")
    stat_command.append(f"--output_folder {PIXY_DIR}")
    stat_command.append(f"--output_prefix {output_prefix}")
    return

def run(vcf_file, pop_file, output_prefix, window_size, bed_file):
    # make sure all directories are created
    create_directory(OUTPUT_DIR)
    create_directory(STATS_DIR)
    create_directory(PIXY_DIR)

    # get pixy stats
    compute_statistics(vcf_file, pop_file, output_prefix, window_size, bed_file)

run("data/hops.vcf", )