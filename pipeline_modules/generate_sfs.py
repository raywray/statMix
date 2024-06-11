import os

from utilities import generate_model_files

OUTPUT_DIR = "output"
OUTPUT_SFS_DIR = f"{OUTPUT_DIR}/sfs"

def execute_command(command):
    os.system(command)


def create_directory(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def build_sfs(vcf_file, modelname, model_file):
    # build sfs command 
    build_sfs_command_list = [
        f"vcf_to_sfs.py",
        f"--vcf {vcf_file}",
        f"--model-file {model_file}",
        f"--modelname {modelname}",
        f"--folded", 
        f"--out {OUTPUT_SFS_DIR}/{modelname}_sfs.out"
    ]
    build_sfs_command = " ".join(build_sfs_command_list)

    # execute command
    execute_command(build_sfs_command)



def run(vcf_file, k):
    # Step 1: make sure all directories exist
    create_directory(OUTPUT_DIR)
    create_directory(OUTPUT_SFS_DIR)
    
    # Step 2: select best fit K  (from estimate pop structure) ✓

    # Step 3: create model file for that K
    model_name, model_file = generate_model_files.run(k)

    # Step 4: use that to create SFS with PPP
    build_sfs(vcf_file, model_name, model_file)
