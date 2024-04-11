import os
import re

def extract_cv_errors(admixture_dir_path):
    cv_errors = []

    for filename in os.listdir(admixture_dir_path):
        if filename.endswith(".out"):
            with open(f"{admixture_dir_path}/{filename}", "r") as file:
                for line in file:
                    if "CV" in line:
                        line_elements = line.split()
                        k = re.findall(r"\d+", line_elements[2])[0]
                        cv_error = line_elements[3]
                        cv_errors.append((k, cv_error))
    return cv_errors


def write_cv_errors_to_file(cv_errors, admixture_dir, output_prefix):
    with open(f"{admixture_dir}/{output_prefix}.cv.error", "w") as file:
        for pair in cv_errors:
            file.write(f"{pair[0]} {pair[1]}\n")


def find_least_cv_error(admixture_dir_path, output_prefix):
    cv_errors = extract_cv_errors(admixture_dir_path)
    write_cv_errors_to_file(cv_errors, admixture_dir_path, output_prefix)
