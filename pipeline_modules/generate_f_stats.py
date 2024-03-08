import os

OUTPUT_DIR = "output"
F_STATS_DIR = f"{OUTPUT_DIR}/f_stats"

def execute_command(command):
    os.system(command)

def create_directory(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def convert_bed_to_eigenstrat(bed_file_prefix):
    """
    THIS HAS A BUG -- Right now, the error is: 
    
    initLogger - WARNING: PPP, version 0.1.12
    exp_handler - ERROR: fatalx:
    bad chrom: 000000
    Traceback (most recent call last):
    File "/anaconda3/envs/hops_stats_env/bin/vcf_format_conversions.py", line 389, in <module>
        run(**convert_argument_parser())
    File "/anaconda3/envs/hops_stats_env/bin/vcf_format_conversions.py", line 384, in run
        bed_to_eigenstrat(**vars(convert_args))
    File "/anaconda3/envs/hops_stats_env/lib/python3.7/site-packages/pgpipe/eigenstrat_wrapper.py", line 226, in bed_to_eigenstrat
        call_convertf(['-p', par_filename])
    File "/anaconda3/envs/hops_stats_env/lib/python3.7/site-packages/pgpipe/eigenstrat_wrapper.py", line 83, in call_convertf
        check_convertf_for_errors(convertf_stderr)
    File "/anaconda3/envs/hops_stats_env/lib/python3.7/site-packages/pgpipe/eigenstrat_wrapper.py", line 42, in check_convertf_for_errors
        raise Exception(convertf_stderr)
    Exception: fatalx:
    bad chrom: 000000
    """
    convert_command_list = [
        "vcf_format_conversions.py",
        f"--binary-ped-prefix {bed_file_prefix}",
        f"--out-prefix {F_STATS_DIR}/hops",
        "--out-format eigenstrat"
    ]
    convert_command = " ".join(convert_command_list)
    execute_command(convert_command)

def calculate_pattersons_d():
    eigenstrat_prefix = ""

    pattersons_command_list = [
        "eigenstrat_fstats.py",
        f"--eigenstrat-prefix {eigenstrat_prefix}",
        "--calc-admix-statistic D",
        "--admix-w-pop",
        "--admix-x-pop",
        "--admix-y-pop",
        "--admix-z-pop"
    ]

    pattersons_command = " ".join(pattersons_command_list)
    execute_command(pattersons_command)

    """
    EXAMPLE:
    eigenstrat_fstats.py 
    --eigenstrat-prefix snps 
    --calc-admix-statistic D 
    --admix-w-pop French 
    --admix-x-pop Yoruba 
    --admix-y-pop Vindija 
    --admix-z-pop Chimp 
    """

def run(bed_file_prefix):
    # create directories
    create_directory(OUTPUT_DIR)
    create_directory(F_STATS_DIR)

    # prepare for eigenstrat
    # TODO uncomment when this is fixed
    # convert_bed_to_eigenstrat(bed_file_prefix) 

run("output/plink/hops_structure")