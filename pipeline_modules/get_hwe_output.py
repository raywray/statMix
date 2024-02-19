import os
import pgpipe.vcf_calc as vcf_calc

OUTPUT_PREFIX = "hwe_hops"
OUTPUT_DIR = "hwe_results"
output_dir_path = f"../output/{OUTPUT_DIR}"

# test for HWE
vcf_calc.run(vcf="../hops.vcf", calc_statistic="hardy-weinberg", out=OUTPUT_PREFIX)
if not os.path.exists(output_dir_path): os.mkdir(output_dir_path)

os.system(f"mv {OUTPUT_PREFIX}* {output_dir_path}")
