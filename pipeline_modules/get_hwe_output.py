import os
import pgpipe.vcf_calc as vcf_calc

OUTPUT_PREFIX = "hwe_hops"
OUTPUT_DIR = "hwe_results"
output_dir_path = f"../output/{OUTPUT_DIR}"

# test for HWE
vcf_calc.run(vcf="../hops.vcf", calc_statistic="hardy-weinberg", out=OUTPUT_PREFIX)
if not os.path.exists(output_dir_path): os.mkdir(output_dir_path)

os.system(f"mv {OUTPUT_PREFIX}* {output_dir_path}")

# create a “reduced” file with only loci that are in HWE at a p-value cutoff of 0.05
os.system(f"vcftools --vcf ../hops.vcf --hwe 0.05 --recode --stdout > {output_dir_path}/hops_in_hwe.vcf")

