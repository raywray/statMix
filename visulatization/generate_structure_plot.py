import seaborn as sns
import pandas as pd
import os

FIGURES_DIR = "output/figures"

def create_directory(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def sort_df_by_pops_nocat(df):
    temp_dfs = []
    pop_sizes = {}
    for pop in sorted(df["Assigned_Pop"].unique()):
        temp = df.loc[df["Assigned_Pop"] == pop].sort_values(by=[pop], ascending=False)
        temp_dfs.append(temp)
        pop_sizes[pop] = len(temp)
    return temp_dfs, pop_sizes


def sort_df_by_pops(df):
    temp_dfs = []
    for pop in sorted(df["Assigned_Pop"].unique()):
        temp = df.loc[df["Assigned_Pop"] == pop].sort_values(by=[pop], ascending=False)
        temp_dfs.append(temp)
    return pd.concat(temp_dfs)


def sort_data(proportions, k):
    sub_dfs, pop_sizes = sort_df_by_pops_nocat(proportions)
    df_sorted_q = sort_df_by_pops(proportions)

    # Order the sub_dfs based on population sizes
    sorted_sub_dfs = sorted(
        sub_dfs, key=lambda x: pop_sizes[x["Assigned_Pop"].iloc[0]], reverse=True
    )

    # Combine the sorted data frames into a single data frame
    df_custom_sort = pd.DataFrame()
    for df in sorted_sub_dfs:
        df_custom_sort = df_custom_sort.append(df, ignore_index=True)

    df_sorted_q.to_csv(f"output/admixture/Admixture-K{k}.csv", index=True)
    return df_sorted_q, df_custom_sort


def get_color_palette():
    return sns.color_palette(
        [
            "#8dd3c7",
            "#ffffb3",
            "#bebada",
            "#fb8072",
            "#80b1d3",
            "#fdb462",
            "#b3de69",
            "#fccde5",
            "#d9d9d9",
            "#bc80bd",
            "#ccebc5",
            "#ffed6f",
        ]
    )


def plot(df_custom_sort, df_sorted_q, k):
    # Get colors
    pal = get_color_palette()

    # Generate Plot
    ax = df_custom_sort.plot.bar(
        stacked=True,
        figsize=(25, 5),
        width=1,
        color=pal,
        fontsize="x-small",
        edgecolor="black",
        linewidth=0.5,
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.set_xticklabels(df_sorted_q.index, rotation=45, ha="right")
    ax.legend(bbox_to_anchor=(1, 1), fontsize="medium", labelspacing=0.5, frameon=False)

    # Save plot as a pdf
    ax.figure.savefig(f"{FIGURES_DIR}/Admixture-K{k}.pdf", bbox_inches="tight")


def create_plots(q_file, label_file, k):
    # create dirs
    create_directory(FIGURES_DIR)

    # Organize data into a dataframe
    # find individuals names
    labels = pd.read_table(label_file, header=None)
    individuals = labels[0]

    # get admixture results
    proportions = pd.read_csv(q_file, sep=" ", header=None)
    names = ["pop{}".format(i) for i in range(1, proportions.shape[1] + 1)]

    # combine individuals' names with admixutre results
    proportions.columns = names
    proportions.insert(0, "Sample", individuals)
    proportions.set_index("Sample", inplace=True)
    proportions["Assigned_Pop"] = proportions.idxmax(axis=1)

    # Sort data
    df_sorted_q, df_custom_sort = sort_data(proportions, k)

    # Plot
    plot(df_custom_sort, df_sorted_q, k)

