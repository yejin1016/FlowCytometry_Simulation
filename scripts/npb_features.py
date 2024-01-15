## Loading necessary libraries
# System
import os
import sys
from argparse import ArgumentParser, RawTextHelpFormatter

# Data
import pandas as pd
import numpy as np


def parse_args_npb():
    parser = ArgumentParser(prog = 'python3 npb_features.py', 
                            formatter_class = RawTextHelpFormatter)    
    # Positional
    parser.add_argument('input', type=str,
                        help='a dataframe converted from FCM data or simulated one')
    # Optional variables
    parser.add_argument('-n_bins', dest='n_bins', type=int, default = 10,
                        help='Number of bins')
    parser.add_argument('-out', dest='out', type = str, default = 'npb_features.csv',
                       help='Name of the output file')
    return parser.parse_args()


# Define a function that uses number of bins to apply non-probabilistic binning

def npb_feature_generation(df, n_bins = 10):
    df = pd.read_csv(df)
    marker_cols = df.iloc[:,:-2].columns
    sample_type = dict(zip(df['sample_name'], df['sample_type']))
    results = []  
    
    bin_dic = dict()
    for i in marker_cols:
        bin_dic[i] = list(df[i].quantile([i*(1/n_bins) for i in range(n_bins)]))


    for sample_name in df['sample_name'].unique():
        # Subset the dataframe to data from only this patient
        result_dict = dict()
        sample_data = df[df['sample_name']==sample_name]
        n_cell = len(sample_data)
        for marker in marker_cols:
            counts, edges = np.histogram(sample_data[marker], bins = bin_dic[marker])
            counts = np.append(counts, n_cell - sum(counts))
            counts = counts/n_cell
            for i in range(n_bins):
                result_dict[marker + "_bin_" + str(i + 1)] = counts[i]
        result_dict['sample_name'] = sample_name
        result_dict['sample_type'] = sample_type[sample_name]
        results.append(result_dict)        

    # Build a dataframe from the list of dictionaries
    results = pd.DataFrame(results)
    return results


def main():
    args = parse_args_npb()

    input_df = args.input
    n_bins = args.n_bins
    out_name = args.out
    
    final_df = npb_feature_generation(input_df, n_bins)

    sys.stdout.write("Writing output to {}...\n".format(out_name))

    final_df.to_csv(out_name, index = False)

    sys.stdout.write("Done!\n")

if __name__ == '__main__':
    main()



