import os

from visulatization import generate_structure_plots

plink_dir_path = f"output/plink"
admixture_dir_path = f"output/admixture"


def make_output_dirs():
    # make output dir for plink
    if not os.path.exists(plink_dir_path): os.mkdir(plink_dir_path)
    # make otuput dir for admixture
    if not os.path.exists(admixture_dir_path): os.mkdir(admixture_dir_path)


def run_admixture(num_subpops_to_test, output_prefix):
    # run admixture to test different number of subpopulations
    for k in range(1, num_subpops_to_test + 1):
        os.system(
            f"admixture --cv output/plink/{output_prefix}.bed {k} > {admixture_dir_path}/log{k}.out"
        )
    os.system(f"mv {output_prefix}* output/admixture")


def least_cv_error(output_prefix):
    # estimate which has the least cross validation error
    os.system(f"bash scripts/bash/estimate_least_cv_error.sh {admixture_dir_path} {output_prefix}")
    return find_k_least_cv(f"{admixture_dir_path}/{output_prefix}.cv.error")
    

def find_k_least_cv(file_path):
    with open(file_path) as f:
        min_row = min(f, key=lambda line: float(line.split()[1]))
    return min_row.split()[0]


def plot_structure(data_file):
    generate_structure_plots.create_plot(data_file)


def run(vcf_file, num_subpops_to_test=1, output_prefix=""):
    unique_output_prefix = f"{output_prefix}_structure"
    make_output_dirs()
    # convert vcf to bim for admixture
    os.system(
        f"bash scripts/bash/convert_vcf_to_bim.sh {vcf_file} {unique_output_prefix}"
    )

    # TODO
    # run_admixture(num_subpops_to_test, unique_output_prefix)
    best_fit_k = least_cv_error(unique_output_prefix)
    print(best_fit_k)
    plot_structure(f"{admixture_dir_path}/{unique_output_prefix}.{best_fit_k}.Q")
   
