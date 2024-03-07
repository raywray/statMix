import os
import pandas as pd

OUTPUT_SFS_DIR = "output/sfs"
OUTPUT_MODEL_DIR = f"{OUTPUT_SFS_DIR}/model_files"

def execute_command(command):
    os.system(command)


def create_directory(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def assign_inds_to_pops(admixture_csv_filename):
    df = pd.read_csv(admixture_csv_filename)  # Load the CSV data

    # Assign the population based on the max proportion value
    df["Assigned_Pop"] = df.drop(columns=["Sample"]).idxmax(axis=1)

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


def create_model_file(k):
    # Step 1: assign individuals to a population
    assign_inds_to_pops(f"output/admixture/Admixture-K{k}.csv")

    # Step 2: build command with output from step 1
    modelname = f"{k}Pop"
    model_file_name = f"{OUTPUT_MODEL_DIR}/{modelname}.model"
    create_model_command_list = [
        f"model_creator.py",
        f"--model {k}Pop",
        f"--model-pop-file {modelname} {OUTPUT_MODEL_DIR}/populations_list.txt",
        *[
            f"--pop-ind-file pop{i} {OUTPUT_MODEL_DIR}/pop{i}_individuals.txt"
            for i in range(1, k + 1)
        ],
        f"--out {model_file_name}"
    ]
    create_model_command = " ".join(create_model_command_list)

    # Step 3: run command
    execute_command(create_model_command)
    return modelname

def build_sfs(vcf_file, modelname):
    # build sfs command 
    build_sfs_command_list = [
        f"vcf_to_sfs.py",
        f"--vcf {vcf_file}",
        f"--model-file {OUTPUT_MODEL_DIR}/{modelname}.model",
        f"--modelname {modelname}",
        f"--folded", # needs to be folded for fsc
        f"--out {OUTPUT_SFS_DIR}/{modelname}_sfs.out"
    ]
    build_sfs_command = " ".join(build_sfs_command_list)

    # execute command
    execute_command(build_sfs_command)



def run(vcf_file, k):
    # Step 1: make sure all directories exist
    create_directory(OUTPUT_SFS_DIR)
    create_directory(OUTPUT_MODEL_DIR)
    
    # Step 2: select best fit K  (from estimate pop structure) ✓

    # Step 3: create model file for that K
    modelname = create_model_file(k)

    # Step 4: use that to create SFS with PPP
    build_sfs(vcf_file, modelname)
