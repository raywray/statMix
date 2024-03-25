import os

HWE_OUTPUT_DIR = f"output/hwe_results"

def execute_command(command):
    os.system(command)


def create_directory(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def run(vcf_file, p_value):
    # Step 1: create dirs
    create_directory("output")
    create_directory(HWE_OUTPUT_DIR)

    # Step 2: build and run hwe command
    hwe_command = f"vcf_calc.py --vcf {vcf_file} --calc-statistic hardy-weinberg --out {HWE_OUTPUT_DIR}/hwe_test"
    execute_command(hwe_command)

    # Step 3: create a “reduced” file with only loci that are in HWE at a p-value cutoff of 0.05
    hwe_reduced_command = f"vcftools --vcf {vcf_file} --hwe {p_value} --recode --stdout > {HWE_OUTPUT_DIR}/loci_in_hwe.vcf"
    execute_command(hwe_reduced_command)
