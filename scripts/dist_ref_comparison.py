## Loading necessary libraries
# System
import os
import sys
from argparse import ArgumentParser, RawTextHelpFormatter

# Data
import pandas as pd
import numpy as np

# Distance metrics
from scipy.stats import wasserstein_distance
from scipy.stats import kstest


def parse_args_dist_ref():
    parser = ArgumentParser(prog = 'python3 dist_ref_comparison.py', 
                            formatter_class = RawTextHelpFormatter)    
    # Positional
    parser.add_argument('input', type=str,
                        help='A dataframe converted from FCM data or simulated one')
    parser.add_argument('method', choices=['EMD', 'KS'],
                        help='Distance metric for calculation')
    # Optional variables
    parser.add_argument('-ref_ratio', dest='ref_ratio', type=float, default = 0.2,
                        help="Assign the reference's size as a ratio from the whole dataset")
    parser.add_argument('-out', dest='out', type = str, default = 'dist_featured.csv',
                       help='Name of the output file')
    return parser.parse_args()


# Define a function that uses number of bins to apply non-probabilistic binning

def dist_feature_generation(df, method, ref_ratio):
    df = pd.read_csv(df)
    ref = df.sample(int(ref_ratio * len(df)), random_state = 1)
    marker_cols = df.iloc[:,:-2].columns
    sample_type = dict(zip(df['sample_name'], df['sample_type']))
    results = []
    for sample_id in df['sample_name'].unique():
        result_dict = dict()
        sample_data = df[df['sample_name']==sample_id]
        for marker in marker_cols:
            # Other distance metrics can be added
            if method == "EMD": 
                d = wasserstein_distance(sample_data[marker], ref[marker])
            elif method == "KS":
                d = kstest(sample_data[marker], ref[marker])[0]
            result_dict[marker] = d
        result_dict['sample_name'] = sample_id
        result_dict['sample_type'] = sample_type[sample_id]
        results.append(result_dict)

    # Build a dataframe from the list of dictionaries
    results = pd.DataFrame(results)
    return results


def main():
    args = parse_args_dist_ref()

    input_df = args.input
    method = args.method
    ref_ratio = args.ref_ratio
    out_name = args.out
    
    final_df = dist_feature_generation(input_df, method, ref_ratio)

    sys.stdout.write("Writing output to {}...\n".format(out_name))

    final_df.to_csv(out_name, index = False)

    sys.stdout.write("Done!\n")

if __name__ == '__main__':
    main()



