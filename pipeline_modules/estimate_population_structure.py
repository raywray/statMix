import os

"""
All commands and functions to run a full population structure analysis using admixture. 

Converts the vcf to bed, runs admixture, finds the best fitting model/number of populations, and creates structure plots
"""

from visulatization import generate_structure_plot, generate_cv_error_plot
from utilities import convert_vcf_to_bed, utilities, estimate_least_cv_error

PLINK_DIR_PATH = f"output/plink"
ADMIXTURE_DIR_PATH = f"output/admixture"

def execute_command(command):
    os.system(command)


def create_directory(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def run_admixture(num_subpops_to_test, output_prefix):
    # run admixture to test different number of subpopulations
    for k in range(1, num_subpops_to_test + 1):
        admixture_command = f"admixture --cv {PLINK_DIR_PATH}/{output_prefix}.bed {k} > {ADMIXTURE_DIR_PATH}/log{k}.out"
        execute_command(admixture_command)
        # TODO switch out for PPP admixture when cv is added
        # os.system(f"admixture.py --binary-ped-prefix {plink_dir_path}/{output_prefix} --pop {k} --cv > {admixture_dir_path}/log{k}.out")
   
    move_files_command = f"mv {output_prefix}* {ADMIXTURE_DIR_PATH}"
    execute_command(move_files_command)


def least_cv_error(output_prefix):
    # estimate which has the least cross validation error
    estimate_least_cv_error.find_least_cv_error(ADMIXTURE_DIR_PATH, output_prefix)
    cv_error_filepath = f"{ADMIXTURE_DIR_PATH}/{output_prefix}.cv.error"

    # plot cv errors
    generate_cv_error_plot.plot_cv_error(cv_error_filepath)
    
    return find_k_least_cv(cv_error_filepath)
    

def find_k_least_cv(file_path):
    with open(file_path) as f:
        min_row = min(f, key=lambda line: float(line.split()[1]))
    return min_row.split()[0]
    

def create_structure_plots(num_subpops_to_test, output_prefix):
    # TODO create one that keeps the populations in the same order so one can compare
    for k in range(1, num_subpops_to_test + 1):
        generate_structure_plot.create_plots(
            f"{ADMIXTURE_DIR_PATH}/{output_prefix}.{k}.Q",
            f"{PLINK_DIR_PATH}/{output_prefix}.nosex",
            k
        )


def run(vcf_file, num_subpops_to_test=1, output_prefix=""):
    unique_output_prefix = utilities.get_unique_prefix(output_prefix)
    
    # create directories
    create_directory(ADMIXTURE_DIR_PATH)
    
    # convert vcf to bed file for admixture
    convert_vcf_to_bed.convert(vcf_file, unique_output_prefix)

    # run admixture
    run_admixture(num_subpops_to_test, unique_output_prefix)

    # find the best fitting k
    best_fit_k = least_cv_error(unique_output_prefix) # TODO maybe instead of generating all the outputs, we just do a range around the best fit k?

    # plot the different admixtures
    create_structure_plots(num_subpops_to_test, unique_output_prefix)
    
    return best_fit_k