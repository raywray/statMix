import os

OUTPUT_DIR = "output"
STATS_DIR = f"{OUTPUT_DIR}/stats"

"""
--calc-statistic <weir-fst, windowed-weir-fst, site-pi, window-pi, 
freq, het-fit, het-fis, hardy-weinberg>

--calc-statistic weir-fst
Requires: --pop-file/--model.
--calc-statistic windowed-weir-fst
Requires: --pop-file/--model and --statistic-window-size. If --statistic-window-step is not given, it will default to the value of --statistic-window-size.

--calc-statistic site-pi
Optional: --pop-file/--model.
--calc-statistic windowed-pi
Requires: --statistic-window-size. . If --statistic-window-step is not given, it will default to the value of --statistic-window-size. Optional: --pop-file/--model.
--calc-statistic het-fis
Requires: --pop-file/--model.
"""

def build_and_execute_command(command_list):
    command = " ".join(command_list)
    os.system(command)


def create_directory(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def calc_tajimas_d(output_prefix, vcf_file, stat_window_size):
    tajimas_d_command_list = [
        "vcf_calc.py",
        f"--vcf {vcf_file}",
        f"--calc-statistic TajimaD",
        f"--statistic-window-size {stat_window_size}",
        f"--out-prefix {STATS_DIR}/{output_prefix}"
    ]
    build_and_execute_command(tajimas_d_command_list)


def run(output_prefix, vcf_file, statistic_window_size):
    # create dirs
    create_directory(OUTPUT_DIR)
    create_directory(STATS_DIR)
    # run all stats
    calc_tajimas_d(output_prefix, vcf_file, statistic_window_size)
    
run("hops", "data/hops.vcf", 10000)