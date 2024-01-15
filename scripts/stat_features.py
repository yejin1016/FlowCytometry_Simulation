## Loading necessary libraries
# System
import os
import sys
from argparse import ArgumentParser, RawTextHelpFormatter

# Data
import pandas as pd
import numpy as np


def parse_args_stat_features():
    """Parses inputs from commandline and returns them as a Namespace object."""

    parser = ArgumentParser(prog = 'python3 stat_features.py',
        formatter_class = RawTextHelpFormatter, description =
        '  Create a dataframe summarizing fcm data with mean, median, std, and IQR.\n\n'
        '  Example syntax:\n'
        '    python3 stat_features.py input_data.csv \n')
    
    # Positional
    parser.add_argument('input', type=str,
                        help='a dataframe converted from FCM data or simulated one')
                            
    # Optionals
    parser.add_argument('-out', '--output', dest='output', type = str, default = 'stat_feature_output.csv',
                       help='name of the output file \n'
                       'default is set to "stat_feature_output.csv"')

    return parser.parse_args()

# Define a function that extracts mean, median, interquartile-range, and standard deviation of each channel and builds a dataframe

def feature_generation(df):
    df = pd.read_csv(df)
    marker_cols = df.iloc[:,:-2].columns
    sample_type = dict(zip(df['sample_name'], df['sample_type']))
    results = []
    for sample_id in df['sample_name'].unique():
        # Subset the dataframe to data from only this patient
        result_dict = dict()
        sample_data = df[df['sample_name']==sample_id]
        for marker in marker_cols:
            result_dict[marker + '_mean'] = sample_data[marker].mean()
            result_dict[marker + '_median'] = sample_data[marker].median()
            result_dict[marker + '_std'] = sample_data[marker].std()
            result_dict[marker + '_iqr'] = sample_data[marker].quantile(0.75) - sample_data[marker].quantile(0.25)
        result_dict['sample_name'] = sample_id
        result_dict['sample_type'] = sample_type[sample_id]
        results.append(result_dict)
    # Build a dataframe from the list of dictionaries
    results = pd.DataFrame(results)
    return results


def main():
    args = parse_args_stat_features()

    input_df = args.input
    output = args.output
    
    final_df = feature_generation(input_df)

    sys.stdout.write("Writing output to {}...\n".format(output))

    final_df.to_csv(output, index = False)

    sys.stdout.write("Done!\n")

if __name__ == '__main__':
    main()



