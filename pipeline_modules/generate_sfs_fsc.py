import os

"""
All commands and functions to build an SFS compatible for fastsimcoal analyses
"""

from utilities import generate_model_files, utilities

OUTPUT_DIR = "output"
SFS_DIR = f"{OUTPUT_DIR}/sfs_for_fsc"

def execute_command(command_list):
    command = " ".join(command_list)
    os.system(command)


def create_directory(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def build_sfs_command(
    vcf_file, model_file, model_name, output_prefix
):
    # TODO: should we include this? --downsamplesizes <down sample sizes>
    sfs_command = [
        "vcf_to_fastsimcoal.py",
        f"--vcf {vcf_file}",
        f"--model-file {model_file}",
        f"--modelname {model_name}",
        "--dim 1 2 m",
        f"--basename {output_prefix}",
    ]
    execute_command(sfs_command)

def run(vcf_file, k, output_prefix):
    # get model files
    model_name, model_file = generate_model_files.run(k)
   
    # create dirs
    create_directory(OUTPUT_DIR)
    create_directory(SFS_DIR)

    output_basename = f"{SFS_DIR}/{output_prefix}"

    build_sfs_command(vcf_file, model_file, model_name, output_basename)

    utilities.unzip_output(f"{output_basename}.zip", SFS_DIR)