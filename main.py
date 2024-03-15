from pipeline_modules import generate_pixy_stats

VCF_FILE = "data/hops.vcf"
OUTPUT_PREFIX = "hops"

def run_summary_stats():
    # generate_hwe_results.hwe_test(vcf_file=VCF_FILE, p_value="0.05")
    # best_fit_k = estimate_population_structure.run(vcf_file=VCF_FILE, output_prefix=OUTPUT_PREFIX, num_subpops_to_test=10)
    # generate_sfs.run(VCF_FILE, best_fit_k)
    # generate_other_stats.get_stats(
    #     output_prefix=OUTPUT_PREFIX,
    #     vcf_file=VCF_FILE,
    #     statistic_window_size=10000,
    #     model_file="output/sfs/model_files/4Pop.model",
    #     model_name="4Pop"
    # )
    generate_pixy_stats.run("data/hops.vcf", "output/sfs/model_files/assigned_populations.csv", "hops", 10000, bypass_invariant_check=True)

if __name__ == '__main__':
    run_summary_stats()