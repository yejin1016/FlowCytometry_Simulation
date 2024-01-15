# System
import os
import glob
import sys
from argparse import ArgumentParser, RawTextHelpFormatter

# Data
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

def parse_args_simulation_summary():
    parser = ArgumentParser(prog = 'python3 simulation_summary.py', 
                            formatter_class = RawTextHelpFormatter)    
    # Positional
    parser.add_argument('input', type=str,
                        help='The basic simulation file just to obtain filename')
    # Optional variables
    parser.add_argument('-out', dest='out', type = str, default = 'output.png',
                       help='Name of the output file')
    return parser.parse_args()

def plot_summary(df, ax, pca = False):
    if pca:
        scaler = StandardScaler()
        scaled_df = scaler.fit_transform(df.iloc[:,:-2])
        pca = PCA(n_components=2)
        prepped_df = pd.DataFrame(pca.fit_transform(scaled_df))
        prepped_df["sample_type"] = df["sample_type"]
    else:
        prepped_df = df
    fig = sns.scatterplot(prepped_df, x=prepped_df.iloc[:, 0], y=prepped_df.iloc[:, 1], ax = ax, hue = "sample_type")
    return fig

def plot_summaries(n_marker, n_tweaks, distance, outlier_ratio, folders):
    results = []
    files = []
    for folder in folders:
        file = glob.glob(os.path.join(folder, f"*{n_marker}_{n_tweaks}_{distance}_{outlier_ratio}_*.csv"))
        for item in file:
            files.append(item)
    files.sort()        
    fig, axs = plt.subplots(figsize = (10, 10), nrows=3, ncols=3, layout='constrained')
    axs[2, 1].axis('off')
    axs[2, 2].axis('off')

    for i in range(len(files)):
        ax = np.ravel(axs)[i]
        name = files[i][files[i].find(str(outlier_ratio))+len(str(outlier_ratio))+1:].replace("_featured.csv","")
        df = pd.read_csv(files[i])
        figure = plot_summary(df, ax = ax, pca = True)
        ax.set_xlabel("PC1", fontsize = 14)
        ax.set_ylabel("PC2", fontsize = 14)
        ax.set_title(name, fontsize = 18)
        
    handles, labels = axs[0, 0].get_legend_handles_labels()

    for ax in np.ravel(axs):
        ax.legend().remove()
    legend = axs[2, 1].legend(handles, labels, fontsize = 14, bbox_to_anchor = (0.8, 0.8))
        
    return fig


def main():
    args = parse_args_simulation_summary()

    input_file = args.input
    out_name = args.out
    
    n_marker = input_file.split("_")[1].split("/")[-1]
    n_tweaks = input_file.split("_")[2]
    dist = input_file.split("_")[-2]
    out_ratio = input_file.split("_")[-1].replace(".csv","")

    folder_path = "/home/gahacat/BI2021/2022-2023/VUMC/snakemake_outputs/feature_generated/"
    folders = glob.glob(os.path.join(folder_path, "*"))
    
    fig = plot_summaries(n_marker, n_tweaks, dist, out_ratio, folders)
    fig.suptitle('Simulation Summary {}_{}_{}_{}'.format(n_marker, n_tweaks, dist, out_ratio), size = 30)
    plt.savefig(out_name, dpi=300, bbox_inches='tight')
    
    sys.stdout.write("Writing output to {}...\n".format(out_name))
    sys.stdout.write("Done!\n")

if __name__ == '__main__':
    main()


