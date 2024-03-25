from utilities import parse_parameters

from pipeline_modules import (
    generate_hwe_results,
    estimate_population_structure,
    generate_sfs,
    generate_other_stats,
    generate_sfs_fsc,
    generate_f_stats,
    generate_pixy_stats,
    run_ima_analysis,
)


def run_summary_stats():
    # get user arguements
    args = parse_parameters.parse()

    # get constants from user
    vcf_file = args.vcf
    output_prefix = args.out_prefix

    # perform analyses specified from user
    if "hwe" in args.analyses:
        generate_hwe_results.run(vcf_file=vcf_file, p_value=args.p_val)
    
    if "pop_structure" in args.analyses:
        best_fit_k = estimate_population_structure.run(
            vcf_file=vcf_file,
            output_prefix=output_prefix,
            num_subpops_to_test=args.subpops_to_test,
        )
        print(f"Best Fit K: {best_fit_k}")
    
    if "sfs" in args.analyses:
        generate_sfs.run(vcf_file=vcf_file, k=best_fit_k)
    
    if "generic" in args.analyses:
        generate_other_stats.run(
            vcf_file=vcf_file,
            statistic_window_size=args.statistic_window_size,
            k=best_fit_k,
        )
    
    if "fsc" in args.analyses:
        generate_sfs_fsc.run(
            vcf_file=vcf_file, k=best_fit_k, output_prefix=output_prefix
        )
    
    if "pixy" in args.analyses:
        generate_pixy_stats.run(
            vcf_file=vcf_file,
            output_prefix=output_prefix,
            window_size=args.statistic_window_size,
            k=best_fit_k,
        )
    
    if "ima" in args.analyses:
        run_ima_analysis.run(
            vcf_file=vcf_file, k=best_fit_k, output_prefix=output_prefix
        )
    
    if "f_stats" in args.analyses:
        generate_f_stats.run(vcf_file=vcf_file, output_prefix=output_prefix)


if __name__ == "__main__":
    run_summary_stats()
