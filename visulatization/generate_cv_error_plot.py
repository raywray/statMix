import matplotlib.pyplot as plt
import os

FIGURES_DIR = "output/figures"

def create_directory(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def plot_cv_error(cv_error_file):
    # create directories
    create_directory(FIGURES_DIR)

    # Read the data from the file
    with open(cv_error_file, "r") as file:
        data = [line.strip().split() for line in file]

    # Convert strings to integers and floats
    data = [(int(pair[0]), float(pair[1])) for pair in data]

    # Sort the data based on x-values
    data.sort(key=lambda pair: pair[0])

    # Separate the sorted data into x and y values
    x = [pair[0] for pair in data]
    y = [pair[1] for pair in data]

    # Create a line plot
    plt.plot(x, y, marker="o", linestyle="-")

    # Add labels and title
    plt.xlabel("K")
    plt.ylabel("Error")
    plt.title("Cross Validation Error")

    # Set ticks on the x-axis to show each x-value
    plt.xticks(x)

    # Display the plot
    plt.savefig(f"{FIGURES_DIR}/admixture_cv_error_plot.pdf")
