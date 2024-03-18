import os
OUTPUT_DIR = "output"
IMA_DIR = f"{OUTPUT_DIR}/ima"

"""
TODO: finish writing this functionality
"""

def execute_command(command_list):
    command = " ".join(command_list)
    os.system(command)

def create_directory(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def vcf_to_ima(vcf_file, pop_file, bed_file, species_prefix):
    convert_command = [
        "vcf_to_ima.py",
        f"--vcf {vcf_file}",
        f"--model-file {pop_file}",
        f"--bed {bed_file}",
        f"--out {species_prefix}"
    ]
    execute_command(convert_command)

def run_ima_analysis(ima_input_file, species_prefix, max_pop_size=None, mig_rate=None, max_split_time=None): # TODO idk if those params are optional
    
    ima_command = [
        "ima3_wrapper.py",
        f"-i {ima_input_file}",
        f"-o {species_prefix}"
    ]
    if max_pop_size: ima_command.append(f"-q {max_pop_size}")
    if mig_rate: ima_command.append(f"-m {mig_rate}")
    if max_split_time: ima_command.append(f"-t {max_split_time}")

    execute_command(ima_command)


def run(vcf_file, population_file, bed_file, species_prefix):
    create_directory(OUTPUT_DIR)
    create_directory(IMA_DIR)
    
    # Step 1: convert vcf to ima
    vcf_to_ima(vcf_file, population_file, bed_file, species_prefix)

    # Step 2: run ima
    ima_file_name = f"{species_prefix}.ima" # TODO change this when you learn what the input file will look like
    run_ima_analysis(ima_file_name, species_prefix)