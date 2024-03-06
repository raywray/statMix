import os
import pandas as pd

output_model_dir_path = "output/model_files"
population_csv_path = f"{output_model_dir_path}/population_assignment.csv"


def execute_command(command):
    os.system(command)


def create_directory(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def assign_inds_to_pops(admixture_csv_filename):
    # Ensure the output directory exists
    create_directory(output_model_dir_path)

    df = pd.read_csv(admixture_csv_filename)  # Load the CSV data

    # Assign the population based on the max proportion value
    df["Assigned_Pop"] = df.drop(columns=["Sample"]).idxmax(axis=1)

    # Sort by 'Assigned_Pop'
    df_sorted = df[["Sample", "Assigned_Pop"]].sort_values(by="Assigned_Pop")

    # Save the sorted DataFrame to a new CSV
    df_sorted.to_csv(f"{output_model_dir_path}/assigned_populations.csv", index=False)

    # Extract unique populations
    unique_pops = df_sorted["Assigned_Pop"].unique()

    # Save unique populations to a text file
    with open(f"{output_model_dir_path}/populations_list.txt", "w") as pop_file:
        for pop in unique_pops:
            pop_file.write(pop + "\n")

    # Save individuals assigned to each population to separate text files
    for pop in unique_pops:
        individuals = df_sorted[df_sorted["Assigned_Pop"] == pop]["Sample"]
        with open(f"{output_model_dir_path}/{pop}_individuals.txt", "w") as ind_file:
            for ind in individuals:
                ind_file.write(ind + "\n")


def create_model_file(k):
    # Step 1: assign individuals to a population
    assign_inds_to_pops(f"output/admixture/Admixture-K{k}.csv")

    # Step 2: build command with output from step 1
    command_list = [
        f"model_creator.py",
        f"--model {k}Pop",
        f"--model-pop-file {k}Pop {output_model_dir_path}/populations_list.txt",
        *[
            f"--pop-ind-file pop{i} {output_model_dir_path}/pop{i}_individuals.txt"
            for i in range(1, k + 1)
        ],
        f"--out {output_model_dir_path}/{k}Pop_model_file.model"
    ]
    command = " ".join(command_list)

    # Step 3: run command
    execute_command(command)


def run(vcf_file, k):
    # Step 1: select best fit K  (from estimate pop structure) ✓
    # Step 2: create model file for that K
    create_model_file(k)
    # Step 3: use that to create SFS with PPP
    # os.system(f"vcf_to_sfs.py --vcf {vcf_file}")


run("data/hops.vcf", 4)
