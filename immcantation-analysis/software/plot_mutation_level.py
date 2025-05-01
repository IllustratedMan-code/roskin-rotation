import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



dfs = {
    "mpaach": pd.read_csv("/data/RoskinLab/team/david/roskin-rotation/immcantation-analysis/mpaach_mut_level.csv"),
    "hhc": pd.read_csv("/data/RoskinLab/team/david/roskin-rotation/immcantation-analysis/hhc_mut_level.csv"),
    "chavi": pd.read_csv("/data/RoskinLab/team/david/roskin-rotation/immcantation-analysis/chavi_mut_level.csv")
}

def boxplot(df, title, var="mutation_level"):
    fig, ax = plt.subplots()
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    sns.stripplot(x="isotype", y=f"{var}.median.mean", data=df, ax=ax)
    sns.boxplot(x="isotype", y=f"{var}.median.mean", data=df, ax=ax, color=(1, 1, 1, 0))
    ax.set_title(title)
    fig.tight_layout()
    return fig


def facet_box(dfs, title, var="mutation_level"):
    labeled_dfs = []
    for k,v in dfs.items():
        v["cohort_label"] = k
        labeled_dfs.append(v)
    df = pd.concat(labeled_dfs)
    isotypes = df["isotype"].unique()
    facet_grid = sns.FacetGrid(df, col="isotype", col_wrap=3, sharex=False, sharey=False)
    facet_grid.map_dataframe(sns.stripplot, x="cohort_label", y=f"{var}.median.mean")
    facet_grid.map_dataframe(sns.boxplot, x="cohort_label", y=f"{var}.median.mean", color=(1, 1, 1, 0))
    plt.suptitle(title)
    plt.tight_layout()
    return facet_grid
           


boxplot(dfs["chavi"], "HIV healthy controls").savefig("chavi_boxplot.svg")
boxplot(dfs["mpaach"], "mpaach healthy controls").savefig("mpaach_boxplot.svg")
boxplot(dfs["hhc"], "human healthy controls").savefig("hhc_boxplot.svg")
boxplot(dfs["chavi"], "HIV healthy controls", var="junction_length").savefig("chavi_boxplot_junction.svg")
boxplot(dfs["mpaach"], "mpaach healthy controls", var="junction_length").savefig("mpaach_boxplot_junction.svg")
boxplot(dfs["hhc"], "human healthy controls", var="junction_length").savefig("hhc_boxplot_junction.svg")

mutation = facet_box(dfs, "Mutation Frequency")
mutation.savefig("facetgrid_mutation.svg")
mutation.savefig("facetgrid_mutation.svg")

junction = facet_box(dfs, "Junction Length", var="junction_length")
junction.savefig("facetgrid_junction.png")
junction.savefig("facetgrid_junction.svg")
