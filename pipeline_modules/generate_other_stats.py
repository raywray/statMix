import os

OUTPUT_DIR = "output"
STATS_DIR = f"{OUTPUT_DIR}/stats"

"""
--calc-statistic <weir-fst, site-pi, window-pi, 
freq, het-fit, het-fis, hardy-weinberg>

--calc-statistic weir-fst
Requires: --pop-file/--model.

--calc-statistic site-pi
Optional: --pop-file/--model.

--calc-statistic windowed-pi
Requires: --statistic-window-size. . If --statistic-window-step is not given, it will default to the value of --statistic-window-size. Optional: --pop-file/--model.

--calc-statistic het-fis
Requires: --pop-file/--model.
"""

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


def run(
        output_prefix, 
        vcf_file, 
        statistic_window_size, 
        model_file, 
        model_name,
):
    stat_output_prefix = f"{STATS_DIR}/{output_prefix}"

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
    
run(
    output_prefix="hops", 
    vcf_file="data/hops.vcf", 
    statistic_window_size=10000,
    model_file="output/sfs/model_files/4Pop.model",
    model_name="4Pop",
)