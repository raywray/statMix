from pipeline_modules import generate_hwe_results, estimate_population_structure, generate_sfs

VCF_FILE = "data/hops.vcf"

def run_summary_stats():
    # generate_hwe_results.hwe_test(vcf_file=VCF_FILE, p_value="0.05")
    best_fit_k = estimate_population_structure.run(vcf_file=VCF_FILE, output_prefix="hops", num_subpops_to_test=10)
    print(best_fit_k)
    # generate_sfs.run(VCF_FILE, best_fit_k)

if __name__ == '__main__':
    run_summary_stats()