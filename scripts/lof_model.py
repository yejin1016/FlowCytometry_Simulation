# System
import os
import sys
from argparse import ArgumentParser, RawTextHelpFormatter

# Data
import pandas as pd
import numpy as np

# LOF model
from sklearn.decomposition import PCA
from sklearn.neighbors import LocalOutlierFactor
from sklearn.metrics import roc_auc_score

def parse_args_lof_model():
    parser = ArgumentParser(prog = 'python3 dist_ref_comparison.py', 
                            formatter_class = RawTextHelpFormatter)    
    # Positional
    parser.add_argument('input', type=str,
                        help='A folder name of featured files')
    parser.add_argument('method', choices=['EMD', 'KS', 'stat', 'pb', 'npb'],
                        help='Feature generation method')
    # Optional variables
    parser.add_argument('-pca', dest='pca', type=bool, default = False,
                        help="Optional to perform PCA")
    parser.add_argument('-out', dest='out', type = str, default = 'output.png',
                       help='Name of the output file')
    return parser.parse_args()

def outlier_detection(df, pca = False):
    lof = LocalOutlierFactor(n_neighbors= 5)
    if pca:
        pca = PCA(n_components = 2)
        prepped_df = pd.DataFrame(pca.fit_transform(df.iloc[:, :-2]))
    else:
        prepped_df = df.iloc[:, :-2]
    true_label = [1 if x == "reference" else -1 for x in df["sample_type"]]
    y_pred = lof.fit_predict(prepped_df)

    roc_auc = roc_auc_score(true_label, y_pred)

    return roc_auc

def main():
    args = parse_args_lof_model()

    input_df = args.input
    method = args.method
    pca = args.pca
    out_name = args.out
    
    result = dist_feature_generation(input_df, method, ref_ratio)

    sys.stdout.write("Writing output to {}...\n".format(out_name))

    final_df.to_csv(out_name, index = False)

    sys.stdout.write("Done!\n")

if __name__ == '__main__':
    main()
