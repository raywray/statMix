import os

plink_dir_path = f"output/plink"
admixture_dir_path = f"output/admixture"

def make_output_dirs():
    # make output dir for plink
    if not os.path.exists(plink_dir_path): os.mkdir(plink_dir_path)
    # make otuput dir for admixture
    if not os.path.exists(admixture_dir_path): os.mkdir(admixture_dir_path)


def run_admixture(vcf_file, num_of_subpops_to_test=5, output_prefix=""):
    unique_output_prefix = f"{output_prefix}_structure"
    make_output_dirs()
    # convert vcf to bim for admixture
    os.system(f"bash scripts/bash/convert_vcf_to_bim.sh {vcf_file} {unique_output_prefix}")

    # run admixture to test different number of subpopulations
    for k in range(0, num_of_subpops_to_test):
        os.system(f"admixture --cv output/plink/{unique_output_prefix}.bed {k} > {admixture_dir_path}/log{k}.out")
    os.system(f"mv {unique_output_prefix}* output/admixture")
    
    
