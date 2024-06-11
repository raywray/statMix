import os

"""
All commands and functions for calculating Eigenstrat F statistics

NOTE: unfinished
"""

from utilities import convert_vcf_to_bed, utilities

OUTPUT_DIR = "output"
F_STATS_DIR = f"{OUTPUT_DIR}/f_stats"

"""
TODO: fix this when have a vcf that will work to test this
"""

def execute_command(command_list):
    command = " ".join(command_list)
    os.system(command)

def create_directory(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def convert_bed_to_eigenstrat(bed_file_prefix):
    convert_command = [
        "vcf_format_conversions.py",
        f"--binary-ped-prefix {bed_file_prefix}",
        f"--out-prefix {F_STATS_DIR}/hops",
        "--out-format eigenstrat"
    ]
    execute_command(convert_command)

def calculate_pattersons_d(eigenstrat_prefix):
    """
    TODO: finish filling this out
    """

    pattersons_command = [
        "eigenstrat_fstats.py",
        f"--eigenstrat-prefix {eigenstrat_prefix}",
        "--calc-admix-statistic D",
        "--admix-w-pop",
        "--admix-x-pop",
        "--admix-y-pop",
        "--admix-z-pop"
    ]
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

def run(vcf_file, output_prefix):
    convert_vcf_to_bed(vcf_file, output_prefix)
    bed_file_prefix = utilities.get_unique_prefix(output_prefix)

    # create directories
    create_directory(OUTPUT_DIR)
    create_directory(F_STATS_DIR)

    # prepare for eigenstrat
    convert_bed_to_eigenstrat(bed_file_prefix) 

    eigenstrat_prefix = bed_file_prefix # TODO change this when you get more information
    calculate_pattersons_d(eigenstrat_prefix)