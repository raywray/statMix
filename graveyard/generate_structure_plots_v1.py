import pandas as pd
import seaborn as sns
from pandas_plink import read_plink

def sort_df_by_pops(df):
    temp_dfs = []
    for pop in sorted(df['assignment'].unique()):
        temp = df.loc[df['assignment'] == pop].sort_values(by=[pop], ascending=False)
        temp_dfs.append(temp)
    return pd.concat(temp_dfs)

def sort_df_by_pops_nocat(df):
    temp_dfs = []
    for pop in sorted(df['assignment'].unique()):
        temp = df.loc[df['assignment'] == pop].sort_values(by=[pop], ascending=False)
        temp_dfs.append(temp)
    return temp_dfs

def create_plot(bed_prefix, q_file):
    (bin, fam, bed) = read_plink(bed_prefix, verbose=False)

    df_q = pd.read_csv(q_file, sep=' ', header=None)

    names = ["pop{}".format(i) for i in range(1, df_q.shape[1]+1)]
    df_q.columns = names
    df_q.insert(0, "Sample", fam["iid"])
    df_q.set_index('Sample', inplace=True)
    print(df_q)

    df_q['assignment'] = df_q.idxmax(axis=1)
    pal = sns.color_palette(['#ef8a62','#92c5de','#fddbc7','#0571b0']) # TODO make this dynamic

    df_sorted_q = sort_df_by_pops(df_q)
    ax = df_sorted_q.plot.bar(stacked=True, 
                          figsize=(25,5), 
                          width=1,
                          color=pal, 
                          fontsize='x-small',
                          edgecolor='black', 
                          linewidth=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_xticklabels(df_sorted_q.index, rotation=45, ha='right')
    ax.legend(bbox_to_anchor=(1,1), fontsize='medium', labelspacing=0.5, frameon=False)
    ax.figure.savefig('Admixture-K4-Perfection.pdf', bbox_inches='tight')

    sub_dfs = sort_df_by_pops_nocat(df_q)
    df_custom_sort = pd.concat([sub_dfs[2], sub_dfs[1], sub_dfs[3], sub_dfs[0]])
    ax = df_custom_sort.plot.bar(stacked=True, 
                             figsize=(25,5), 
                             width=1,
                             color=pal, 
                             fontsize='x-small',
                             edgecolor='black', 
                             linewidth=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_xticklabels(df_sorted_q.index, rotation=45, ha='right')
    ax.legend(bbox_to_anchor=(1,1), fontsize='medium', labelspacing=0.5, frameon=False)
    ax.figure.savefig('Admixture-K4-Perfection2.pdf', bbox_inches='tight')


bed_prefix = "output/plink/hops_structure"
q_file = "output/admixture/hops_structure.4.Q"
create_plot(bed_prefix, q_file)