import os

from utilities import utilities, generate_model_files, convert_vcf_to_bed

OUTPUT_DIR = "output"
STATS_DIR = f"{OUTPUT_DIR}/stats"
PIXY_DIR = f"{STATS_DIR}/pixy"

"""
TODO change this file so that it's compatible with PPP pixy
"""

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
        f"--populations {pop_file}",
        "--n_cores 10"
    ]
    if window_size: stat_command.append(f"--window_size {window_size}")
    elif bed_file: stat_command.append(f"--bed_file {bed_file}")
    stat_command.append(f"--output_folder {PIXY_DIR}")
    stat_command.append(f"--output_prefix {output_prefix}")

    execute_command(stat_command)

def run(vcf_file, output_prefix, window_size, k):
    # get pop file
    model_name, model_file = generate_model_files.run(k)
    pop_file = "output/model_files/assigned_populations.csv"

    # get bed file
    convert_vcf_to_bed.convert(vcf_file)
    bed_prefix = utilities.get_unique_prefix(output_prefix)
    bed_file = f"output/plink/{bed_prefix}.bed"
    
    # make sure all directories are created
    create_directory(OUTPUT_DIR)
    create_directory(STATS_DIR)
    create_directory(PIXY_DIR)

    # convert vcf to vcf.gz
    vcf_file_base_name = utilities.get_file_base_path(vcf_file)
    gz_vcf_file = f"{vcf_file_base_name}_gz"
    os.system(f"cp {vcf_file_base_name}.vcf {gz_vcf_file}.vcf")
    os.system(f"bgzip {gz_vcf_file}.vcf")

    # index vcf with tabix
    os.system(f"tabix {gz_vcf_file}.vcf.gz")

    # if pop_file is a csv, convert to txt
    if utilities.get_file_extension(pop_file) == ".csv":
        pop_file_txt = utilities.change_extension(pop_file, "txt")
        utilities.csv_to_txt(pop_file, pop_file_txt)
        pop_file = pop_file_txt

    # get pixy stats
    compute_statistics(f"{gz_vcf_file}.vcf.gz", pop_file, output_prefix, window_size, bed_file)

