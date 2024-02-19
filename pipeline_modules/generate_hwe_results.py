import os
import pgpipe.vcf_calc as vcf_calc

VCF_FILE_PATH = "hops.vcf"
OUTPUT_PREFIX = "hwe_hops"
OUTPUT_DIR = "hwe_results"

output_dir_path = f"output/{OUTPUT_DIR}"

def hwe_test(p_value="0.05"):
    # test for HWE
    vcf_calc.run(vcf=VCF_FILE_PATH, calc_statistic="hardy-weinberg", out=OUTPUT_PREFIX)
    if not os.path.exists(output_dir_path): os.mkdir(output_dir_path)

    # move output to the output directory
    os.system(f"mv {OUTPUT_PREFIX}* {output_dir_path}")

    # create a “reduced” file with only loci that are in HWE at a p-value cutoff of 0.05
    os.system(f"vcftools --vcf {VCF_FILE_PATH} --hwe {p_value} --recode --stdout > {output_dir_path}/hops_in_hwe.vcf")

