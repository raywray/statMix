from pipeline_modules import generate_hwe_results, estimate_population_structure, generate_sfs

VCF_FILE = "data/hops.vcf"

generate_hwe_results.hwe_test(vcf_file=VCF_FILE)
best_fit_k = estimate_population_structure.run(vcf_file=VCF_FILE, output_prefix="hops", num_subpops_to_test=10)
generate_sfs.run(VCF_FILE, best_fit_k)

