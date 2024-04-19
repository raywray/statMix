import os
import csv

from utilities import generate_model_files, utilities

OUTPUT_DIR = "output"
STATS_DIR = f"{OUTPUT_DIR}/stats"


def execute_command(command_list):
    command = " ".join(command_list)
    os.system(command)


def create_directory(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def build_stats_command(
        calc_stat, 
        output_prefix=None,
        vcf_file=None, 
        statistic_window_size=None, 
        model_file=None, 
        model_name=None, 
        output_dir=None
):

    command = [
        "vcf_calc.py",
        f"--calc-statistic {calc_stat}"
    ]
    if vcf_file: command.append(f"--vcf {vcf_file}")
    if statistic_window_size: command.append(f"--statistic-window-size {statistic_window_size}")
    if model_file: command.append(f"--model-file {model_file}")
    if model_name: command.append(f"--model {model_name}")
    
    if output_prefix: command.append(f"--out-prefix {output_prefix}")
    elif output_dir: command.append(f"--out-dir {output_dir}")
   
    execute_command(command)

def get_model_files(k):
    model_name, model_file = generate_model_files.run(k)
    return model_name, model_file

def calculate_pi_per_pop(vcf_file):
    # this is all kinda hard-coded because of PPP errors
    output_dir = f"{STATS_DIR}/site_pi_per_pop"
    create_directory(output_dir)

    # step 1: get pop files in a list
    model_files_dir = "output/model_files"
    all_files = os.listdir(model_files_dir)
    pop_files = [f for f in all_files if f.startswith("pop") and f != "populations_list.txt"]

    # step 2: loop through and send through vcftools
    for i in range(len(pop_files)):
        file_path = f"{model_files_dir}/{pop_files[i]}"
        file_basename = utilities.get_file_base_path(file_path).split("/")[-1]
        site_pi_filepath = f"{output_dir}/{file_basename}.sites.pi"
        command = f"vcftools --vcf {vcf_file} --keep {file_path} --site-pi --out {file_basename}"
        # execute command
        os.system(command)
        # move file
        os.rename(f"{file_basename}.sites.pi", site_pi_filepath)
        os.rename(f"{file_basename}.log", f"{output_dir}/{file_basename}.log")

        # step 3: calculate average
        calculate_average_pi_per_pop(site_pi_filepath)

def calculate_average_pi_per_pop(pop_pi_filepath):
    sum_pi = 0
    count = 0

    file_basename = utilities.get_file_base_path(pop_pi_filepath).split("/")[-1]

    # Read the file and calculate sum and count
    with open(pop_pi_filepath, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        next(reader)  # Skip the header
        for row in reader:
            pi_value = float(row[2])  
            sum_pi += pi_value
            count += 1

    # Calculate the average
    if count > 0:
        average_pi = sum_pi / count
        with open(f"output/stats/site_pi_per_pop/{file_basename}_average.txt", 'w') as output_file:
            output_file.write(str(average_pi))
    else:
        with open(f"output/stats/site_pi_per_pop/{file_basename}_average.txt", 'w') as output_file:
            output_file.write("No valid PI values found.")

def calculate_pi(vcf_file, output_prefix):
    command = f"vcftools --vcf {vcf_file} --site-pi --out {output_prefix}"
    os.system(command)



def run(
        output_prefix, 
        vcf_file, 
        statistic_window_size,
        k 
):
    stat_output_prefix = f"{STATS_DIR}/{output_prefix}"
    model_name, model_file = get_model_files(k)

    # create dirs
    create_directory(OUTPUT_DIR)
    create_directory(STATS_DIR)
    
    # run all stats   
    # calc tajimas d
    build_stats_command(
        calc_stat="TajimaD", 
        output_prefix=stat_output_prefix, 
        vcf_file=vcf_file, 
        statistic_window_size=statistic_window_size
    )
   
    # windowed weir fst
    build_stats_command(
        calc_stat="windowed-weir-fst",
        output_dir=f"{STATS_DIR}/windowed_weir_fst",
        vcf_file=vcf_file,
        statistic_window_size=statistic_window_size,
        model_file=model_file,
        model_name=model_name,
    )

    # weir fst
    build_stats_command(
        calc_stat="weir-fst",
        vcf_file=vcf_file,
        model_name=model_name,
        model_file=model_file,
        output_dir=f"{STATS_DIR}/weir_fst"
    )

    # site pi NOTE: there is a bug in PPP for this one.
    # build_stats_command(
    #     calc_stat="site-pi",
    #     vcf_file=vcf_file,
    #     output_prefix=stat_output_prefix,
    # )

    # running this instead
    calculate_pi(vcf_file=vcf_file, output_prefix=stat_output_prefix)
    

    # site pi per pop NOTE: there is a bug in PPP for this one. 
    # build_stats_command(
    #     calc_stat="site-pi",
    #     vcf_file=vcf_file,
    #     model_file=model_file,
    #     model_name=model_name,
    #     output_dir=f"{STATS_DIR}/site_pi_per_pop"
    # )

    # running this instead
    calculate_pi_per_pop(vcf_file=vcf_file)

    # windowed pi
    build_stats_command(
        calc_stat="window-pi",
        vcf_file=vcf_file,
        statistic_window_size=statistic_window_size,
        output_prefix=stat_output_prefix,
    )
    
    # windowed pi per pop
    build_stats_command(
        calc_stat="window-pi",
        vcf_file=vcf_file,
        statistic_window_size=statistic_window_size,
        model_file=model_file,
        model_name=model_name,
        output_dir=f"{STATS_DIR}/windowed_pi_per_pop"
    )

    # het-fis
    build_stats_command(
        calc_stat="het-fis",
        vcf_file=vcf_file,
        model_name=model_name,
        model_file=model_file,
        output_prefix=f"{stat_output_prefix}_fis"
    )

    # het-fit
    build_stats_command(
        calc_stat="het-fit",
        vcf_file=vcf_file,
        output_prefix=f"{stat_output_prefix}_fit"
    )

    # freq 
    build_stats_command(
        calc_stat="freq",
        vcf_file=vcf_file,
        output_prefix=stat_output_prefix
    )