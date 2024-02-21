import os
import pandas as pd

output_data_dir_path = "output/data"
population_csv_path = f"{output_data_dir_path}/population_assignment.csv"

def assign_inds_to_pops(admixture_csv_filename):
    # Load CSV data
    df = pd.read_csv(admixture_csv_filename)
    # Assign the population (based on the max proportion val)
    df['Assigned_Pop'] = df.drop(columns=['Sample']).idxmax(axis=1)
    # Optionally, if you want to group by 'Assigned_Pop' and do something with the groups
    # For example, saving the sample names grouped by 'Assigned_Pop' to a new CSV
    result_df = df[['Sample', 'Assigned_Pop']].sort_values(by='Assigned_Pop')
    # Save to CSV
    if not os.path.exists(output_data_dir_path): os.mkdir(output_data_dir_path)
    result_df.to_csv(f"{population_csv_path}", index=False)


def create_model_file(k):
    # Step 1: assign individuals to a population 
    assign_inds_to_pops(f"output/admixture/Admixture-K{k}.csv")
    population_df = pd.read_csv(f"{population_csv_path}")
    print(population_df.tail())
    # TODO create a way to create a big model command with this information use update model commands

    # EXAMPLE
    # model_creator.py --model 1Pop --model-pop 1Pop Paniscus --pop-ind Paniscus Pan_paniscus-9731_LB502
    # os.system(f"model_creator.py --model {k}Pop")

    return

def run(vcf_file, k):
    # Step 1: select best fit K  (from estimate pop structure) ✓
    # Step 2: create model file for that K
    create_model_file(k)
    # Step 3: use that to create SFS with PPP
    # os.system(f"vcf_to_sfs.py --vcf {vcf_file}")    

run("data/hops.vcf", 4)