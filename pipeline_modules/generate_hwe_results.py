import os
import pgpipe.vcf_calc as vcf_calc

OUTPUT_PREFIX = "hwe"

output_dir_path = f"output/hwe_results"

def hwe_test(vcf_file, p_value="0.05"):
    # test for HWE
    vcf_calc.run(vcf=vcf_file, calc_statistic="hardy-weinberg", out=OUTPUT_PREFIX)
    # if want to switch above statement for bash, do this:
    # os.system(f"vcf_calc.py --vcf {VCF_FILE_PATH} --calc-statistic hardy-weinberg --out {OUTPUT_PREFIX}")
   
    if not os.path.exists(output_dir_path): os.mkdir(output_dir_path)

    # move output to the output directory
    os.system(f"mv {OUTPUT_PREFIX}* {output_dir_path}")

    # create a “reduced” file with only loci that are in HWE at a p-value cutoff of 0.05
    os.system(f"vcftools --vcf {vcf_file} --hwe {p_value} --recode --stdout > {output_dir_path}/loci_in_hwe.vcf")

