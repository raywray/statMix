import os
OUTPUT_DIR = "output"
IMA_DIR = f"{OUTPUT_DIR}/ima"

def execute_command(command):
    os.system(command)


def create_directory(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def vcf_to_ima(vcf_file, pop_file, bed_file):
    # Step 1: convert vcf to ima
    """
    Input Arguments
    --vcf <input_filename>
    Filename for input VCF if using BED file with locus information
    --vcfs <vcf_filename_1>...*<vcf_filename_n>*
    One or multiple VCF input filenames where each file contains sequences for a single locus. A file with lines corresponding to filenames can be provided with --vcfs @<vcf_filelist>
    --model-file <model_filename>
    Filename of model file.
    --model <model name>
    If model file contains multiple models, use this argument to specify name of population to use.
    --reference-fasta <reference_filename>
    Filename for reference FASTA file. File can be uncompressed or bg-zipped, but must be indexed with faidx. When option is specified, default options are to include sequence in output loci but not filter for CpGs (use --parse-cpg)
    --bed <bed_filename>
    Filename for BED file specifying loci if only one VCF is provided. Can be used with multiple VCFs if line count aligns, used for getting correct locus length.
    Output Arguments
    --out <out_filename>
    Output filename.
    Model Options
    --mutrate <mutation rate>
    Set mutation rate per base pair (default is 1e-9). This value is multiplied by locus length to get mutation rate per locus.
    --inheritance-scalar <scalar>
    Sets inheritance scalar for all loci. Default behavior is to set scalar to 1 for non-X/Y/MT chromosomes, .75 for 'X' and 'chrX', and .25 for 'y', 'chrY', 'MT', and 'chrMT'.
    Filtering Options
    --remove-multiallele
    Set all multiallelic sites to be reference.
    --drop-missing-sites <individual_count>
    Drops all sites where more than 'individual_count' individuals are missing data. Default is -1 (no dropping), and 0 will drop all sites missing data and replace them with the reference allele.
    --drop-missing-inds
    If set, if an individual is missing data at a locus, that individual will not be included at that locus and population counts for that locus will be adjusted.
    --remove-cpg
    Requires --reference-fasta. If set, will replace CpG sites with reference allele at site, setting them as invariant.
    Other Options
    --oneidx-start
    If set, indicates input BED regions are formatted as one-indexed, closed intervals, as opposed to the BED default of zero-based, half-open intervals. For example, the first million bases on a chromosome would be:

    Zero-based, half-open: 0,1000000 One-based, closed: 1,1000000
    --bed-column-index <start_col,end_col,chrom_col>
    Comma-separated list of zero-based indexes of start, end, and chromosome name columns in input BED file. Default value for traditionally structured BED is 1,2,0
    --noseq
    If set, and --reference-fasta is provided, will not output invariant sites to IM file
    """
    convert_command_list = [
        "vcf_to_ima.py",
        f"--vcf {vcf_file}",
        f"--model-file {pop_file}",
        f"--bed {bed_file}"
    ]
    convert_command = " ".join(convert_command_list)
    execute_command(convert_command)
# Step 2: run ima
"""
Input Arguments
-i <input_file>
Name of IMa3 input file generated by PPP
-o <output_file>
Name of IMa3 output file. Additional files will use this as prefix.
Parameter Arguments
-q <max_pop_size>
Sets maximum population size parameter for all populations.
-m <migration_rate>
Sets migration rate prior.
-t <max_split_time>
Sets maximum splitting time parameter.
Wrapper Arguments
--threads <thread_count>
Set number of threads to use. This will check that the proper version of IMa3 has been compiled and the system has mpirun installed.
--ima-path <path_to_ima>
Path to IMa executable to use if not on system path. This should include the name of the executable, not just the path to it.
"""
def run(vcf_file, population_file, bed_file):
    create_directory(OUTPUT_DIR)
    create_directory(IMA_DIR)


    vcf_to_ima(vcf_file, population_file, bed_file)

run("hops_all.vcf", "output/sfs/model_files/4Pop.model", "output/plink/hops_structure.bed")