import os


# Step 1: select best fit K  (from estimate pop structure) ✓
# Step 2: create model file for that K
# Step 3: use that to create SFS with PPP

def create_model_file(k):
    # EXAMPLE
    # model_creator.py --model 1Pop --model-pop 1Pop Paniscus --pop-ind Paniscus Pan_paniscus-9731_LB502
    os.system(f"model_creator.py --model {k}Pop")

    return

def run(vcf_file, k):
    os.system(f"vcf_to_sfs.py --vcf {vcf_file}")    