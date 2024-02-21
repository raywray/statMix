import os

from visulatization import generate_structure_plot

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
        # TODO switch out for PPP admixture when cv is added
        # os.system(f"admixture.py --binary-ped-prefix {plink_dir_path}/{output_prefix} --pop {k} --cv > {admixture_dir_path}/log{k}.out")
    os.system(f"mv {output_prefix}* output/admixture")


def least_cv_error(output_prefix):
    # estimate which has the least cross validation error
    os.system(f"bash scripts/bash/estimate_least_cv_error.sh {admixture_dir_path} {output_prefix}")
    return find_k_least_cv(f"{admixture_dir_path}/{output_prefix}.cv.error")
    

def find_k_least_cv(file_path):
    with open(file_path) as f:
        min_row = min(f, key=lambda line: float(line.split()[1]))
    return min_row.split()[0]


def convert_vcf_to_bed(vcf_file, output_prefix):
    os.system(f"vcf_format_conversions.py --vcf {vcf_file} --out-prefix {output_prefix} --out-format binary-ped")
    os.system(f"mv {output_prefix}* {plink_dir_path}")


def create_structure_plots(num_subpops_to_test, output_prefix):
    # TODO create one that keeps the populations in the same order so one can compare
    for k in range(1, num_subpops_to_test + 1):
        generate_structure_plot.create_clustered_plot(
            f"{plink_dir_path}/{output_prefix}",
            f"{admixture_dir_path}/{output_prefix}.{k}.Q",
            k
        )


def run(vcf_file, num_subpops_to_test=1, output_prefix=""):
    unique_output_prefix = f"{output_prefix}_structure"
    make_output_dirs()
    # TODO
    # convert_vcf_to_bed(vcf_file, unique_output_prefix)
    # TODO
    run_admixture(num_subpops_to_test, unique_output_prefix)
    best_fit_k = least_cv_error(unique_output_prefix)
    # print(best_fit_k) # TODO maybe instead of generating all the outputs, we just do a range around the best fit k?
    # create_structure_plots(num_subpops_to_test, unique_output_prefix)
    return best_fit_k
   
