import os
import pandas as pd

OUTPUT_MODEL_DIR = f"output/model_files"


def execute_command(command):
    os.system(command)


def assign_inds_to_pops(admixture_csv_filename):
    df = pd.read_csv(admixture_csv_filename)  # Load the CSV data

    # Sort by 'Assigned_Pop'
    df_sorted = df[["Sample", "Assigned_Pop"]].sort_values(by="Assigned_Pop")

    # Save the sorted DataFrame to a new CSV
    df_sorted.to_csv(f"{OUTPUT_MODEL_DIR}/assigned_populations.csv", index=False)

    # Extract unique populations
    unique_pops = df_sorted["Assigned_Pop"].unique()

    # Save unique populations to a text file
    with open(f"{OUTPUT_MODEL_DIR}/populations_list.txt", "w") as pop_file:
        for pop in unique_pops:
            pop_file.write(pop + "\n")

    # Save individuals assigned to each population to separate text files
    for pop in unique_pops:
        individuals = df_sorted[df_sorted["Assigned_Pop"] == pop]["Sample"]
        with open(f"{OUTPUT_MODEL_DIR}/{pop}_individuals.txt", "w") as ind_file:
            for ind in individuals:
                ind_file.write(ind + "\n")


def run(k):
    # make sure directory exists
    modelname = f"{k}Pop"

    # if model files have already been made, return the modelname
    if not os.path.exists(OUTPUT_MODEL_DIR):
        os.makedirs(OUTPUT_MODEL_DIR)
    elif os.path.exists(OUTPUT_MODEL_DIR) and os.listdir(OUTPUT_MODEL_DIR):
        print("already there")
        return modelname

    # Step 1: assign individuals to a population
    assign_inds_to_pops(f"output/admixture/Admixture-K{k}.csv")

    # Step 2: build command with output from step 1

    model_file_name = f"{OUTPUT_MODEL_DIR}/{modelname}.model"
    create_model_command_list = [
        f"model_creator.py",
        f"--model {k}Pop",
        f"--model-pop-file {modelname} {OUTPUT_MODEL_DIR}/populations_list.txt",
        *[
            f"--pop-ind-file pop{i} {OUTPUT_MODEL_DIR}/pop{i}_individuals.txt"
            for i in range(1, int(k) + 1)
        ],
        f"--out {model_file_name}",
    ]
    create_model_command = " ".join(create_model_command_list)

    # Step 3: run command
    execute_command(create_model_command)
    return modelname
