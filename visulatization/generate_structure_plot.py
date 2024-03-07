from scipy.cluster.hierarchy import linkage, leaves_list
from scipy.spatial.distance import pdist
from pandas_plink import read_plink
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def create_clustered_plot(bed_prefix, q_file, k):
    (bim, fam, bed) = read_plink(bed_prefix, verbose=False)
    df_q = pd.read_csv(q_file, sep=' ', header=None)
    
    # Setting up the DataFrame
    names = ["pop{}".format(i) for i in range(1, df_q.shape[1]+1)]
    df_q.columns = names
    df_q.insert(0, "Sample", fam["iid"])
    df_q.set_index('Sample', inplace=True)
    
    # Hierarchical Clustering
    Y = pdist(df_q[names].values, metric='euclidean')  # Pairwise distances
    Z = linkage(Y, method='ward')  # Hierarchical clustering
    idx = leaves_list(Z)  # Order of leaves in the hierarchical tree
    
    # Reordering DataFrame according to clustering
    df_q_clustered = df_q.iloc[idx]
    
    # Plotting
    pal = sns.color_palette(
        [
            '#8dd3c7', 
            '#ffffb3', 
            '#bebada', 
            '#fb8072', 
            '#80b1d3', 
            '#fdb462', 
            '#b3de69', 
            '#fccde5', 
            '#d9d9d9',
            '#bc80bd', 
            '#ccebc5', 
            '#ffed6f'
        ]
    )
    ax = df_q_clustered[names].plot.bar(
        stacked=True, 
        figsize=(25,5), 
        width=1, 
        color=pal, 
        edgecolor='black',
        linewidth=0.5
    )
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    ax.set_xlabel("Individuals", fontsize='medium')
    ax.set_ylabel("Ancestry Proportions", fontsize='medium')
    ax.set_xticklabels(df_q_clustered.index, rotation=45, ha='right')
    ax.legend(bbox_to_anchor=(1,1), fontsize='medium', labelspacing=0.5, frameon=False)    
    plt.savefig(f'output/figures/Admixture-K{k}.pdf', bbox_inches='tight')
    df_q_clustered.to_csv(f"output/admixture/Admixture-K{k}.csv", index=True)