from pipeline_modules import generate_hwe_results, estimate_population_structure

VCF_FILE = "hops.vcf"

# TODO
# generate_hwe_results.hwe_test(vcf_file=VCF_FILE)
estimate_population_structure.run(vcf_file=VCF_FILE, output_prefix="hops", num_subpops_to_test=10)
