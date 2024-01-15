# System
import os
import sys
from argparse import ArgumentParser, RawTextHelpFormatter

# Data
import pandas as pd
import numpy as np

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

def parse_args_visualization():
    parser = ArgumentParser(prog = 'python3 simulation_visualization.py', 
                            formatter_class = RawTextHelpFormatter)    
    # Positional
    parser.add_argument('input', type=str,
                        help='A simulated FCM data')
    parser.add_argument('n_tweaks', type=int,
                        help='Number of channels affected by outliers')    
    # Optional variables
    parser.add_argument('-out', dest='out', type = str, default = 'output.png',
                       help='Name of the output file')
    return parser.parse_args()


def simulation_visualiazation(df, n_tweaks):
    df = pd.read_csv(df)
    marker_cols = df.iloc[:,:-2].columns
    if n_tweaks != 0:
        tweaked_markers = marker_cols[:n_tweaks]
    
    # Create subplot layout based on channel number
    if len(marker_cols) == 8:
        fig, axs = plt.subplots(nrows=3, ncols=3, figsize=(9, 9), layout='constrained')
        axs[2, 2].set_axis_off()
    elif len(marker_cols) == 16:
        fig, axs = plt.subplots(nrows=4, ncols=4, figsize=(12, 12), layout='constrained')

    # Iterate over the axes and plot the i-th plot
    for i, ax in zip(range(len(marker_cols)), np.ravel(axs)):
        # Plot the i-th plot
        if i == 0:
            sns.kdeplot(df[df["sample_type"] == "reference"], x = marker_cols[i], ax = ax, color = "cornflowerblue", linewidth = 1, label = "reference")
            sns.kdeplot(df[df["sample_type"] == "outlier"], x = marker_cols[i], ax = ax, color = "orangered", linewidth = 1, label = "outlier")
        else:
            sns.kdeplot(df[df["sample_type"] == "reference"], x = marker_cols[i], ax = ax, color = "cornflowerblue", linewidth = 1)
            sns.kdeplot(df[df["sample_type"] == "outlier"], x = marker_cols[i], ax = ax, color = "orangered", linewidth = 1)
        if marker_cols[i] in tweaked_markers:
            ax.set_facecolor('lightgray')
    fig.legend(loc = "lower right", bbox_to_anchor = (0.9, 0.2), fontsize = 12)
            
    return fig



def main():
    args = parse_args_visualization()

    input_df = args.input
    n_tweaks = args.n_tweaks
    out_name = args.out
    
    fig = simulation_visualiazation(input_df, n_tweaks)

    sys.stdout.write("Writing output to {}...\n".format(out_name))

    fig.savefig(out_name, dpi=300, bbox_inches='tight')

    sys.stdout.write("Done!\n")

if __name__ == '__main__':
    main()


