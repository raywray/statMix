import os

from utilities import generate_model_files

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

    # site pi
    build_stats_command(
        calc_stat="site-pi",
        vcf_file=vcf_file,
        output_prefix=stat_output_prefix,
    )

    # site pi per pop
    build_stats_command(
        calc_stat="site-pi",
        vcf_file=vcf_file,
        model_file=model_file,
        model_name=model_name,
        output_dir=f"{STATS_DIR}/site_pi_per_pop"
    )

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
