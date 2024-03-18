import pandas as pd
import os

def csv_to_txt(csv_file, txt_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Write to tab-separated text file without headers
    df.to_csv(txt_file, sep='\t', index=False, header=False)


def get_file_extension(file_path):
    return os.path.splitext(file_path)[1]

def change_extension(file_path, new_extension):
    base_name = get_file_base_name(file_path)
    return f"{base_name}.{new_extension}"

def get_file_base_name(file_path):
    # Split the file path into directory, base name, and extension
    directory, base_name = os.path.split(file_path)
    base_name_without_extension = os.path.splitext(base_name)[0]
    return os.path.join(directory, base_name_without_extension)


    
