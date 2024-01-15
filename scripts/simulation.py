# Authors: Y. Park, T. Mocking
# Contact: t.r.mocking@amsterdaumumc.nl
import os
import sys
from argparse import ArgumentParser, RawTextHelpFormatter

# Data
import pandas as pd
import numpy as np
from fcsy import DataFrame

# Simulations
from sklearn.datasets import make_blobs
import random as rd


def parse_args_simulation():
    parser = ArgumentParser(prog = 'python3 simulation.py', 
                            formatter_class = RawTextHelpFormatter)
    # Common variables
    parser.add_argument('-n_samples', dest='n_samples', type=int, default = 100, 
                        help='Number of total samples')
    parser.add_argument('-n_markers', dest='n_markers', type=int, default = 8,
                        help='Number of markers')
    parser.add_argument('-n_cells', dest='n_cells', type=int, default = 2000,
                        help='Number of cells in each sample')
    parser.add_argument('-n_tweaks', dest='n_tweaks', type=int, default = 2,
                        help='Number of channels affected by outlier')
    parser.add_argument('-out', dest='out', type = str, default = 'output.csv',
                       help='Name of the output file')

    # Reference-specific variables
    parser.add_argument('-ref_mean_std', dest='ref_mean_std', type=float, default=0.3,
                        help='Standard deviation of Gaussian center selection (ref)')
    parser.add_argument('-ref_std_range', dest='ref_std_range', type=str, default='0.1,0.2',
                        help='Range of Gaussian width sampling (ref)')
    parser.add_argument('-ref_center_dist', dest='ref_center_dist', type=float, default=3,
                        help='Distance offset between Gaussians (ref)')
    # Outlier-specific variables
    parser.add_argument('-outlier_ratio', dest='outlier_ratio', type=float, default = 0.2, 
                        help='ratio of outlier samples')
    parser.add_argument('-outlier_mean_std', dest='outlier_mean_std', type=float, default=1,
                        help='Standard deviation of Gaussian center selection (outlier)')
    parser.add_argument('-outlier_std_range', dest='outlier_std_range', type=str, default='0.1,0.5',
                        help='Range of Gaussian width sampling (outlier)')
    parser.add_argument('-outlier_center_dist', dest='outlier_center_dist', type=float, default=3,
                        help='Distance offset between Gaussians (outlier)')

    return parser.parse_args()


def simulate_sample(n_markers, n_cells, n_peaks, mean_std, std_range, 
                    center_dist, seed):
    """Creates a dataframe of simulated flow cytometry-like data using Gaussian
    distributions.

    Parameters:
        n_markers (int): Number of markers (columns) to simulate.
        n_cells (int): Number of cells (rows) to simulate.
        n_peaks (list): Peaks to generate per n_marker (1-3).
        mean_std (float): Standard deviation of Gaussian center selection.
        std_range (tuple): Minimum and maximum to use when randomly assigning 
        width of Gaussian distributions.
        center_dist (float): Distance to seperate Gaussians.
        random_state (int): Random state to use in sampling steps.

    Returns:
        pd.DataFrame containing simulated data. 
    """
    # Initialize an empty pandas DataFrame
    simulated_data = DataFrame(index = range(n_cells))
    
    # Define the minimum and maximum values for the Gaussian width sampling
    # Bigger ranges mean wider Gaussians
    std_min = std_range[0]
    std_max = std_range[1]

    for i in range(n_markers):
        if n_peaks[i] ==  1:
            rd.seed(seed)
            center_std = rd.uniform(std_min, std_max)
            centers = [[rd.gauss(0, mean_std)]]
            X, y = make_blobs(n_samples = n_cells, 
                              n_features = 1, 
                              cluster_std = center_std, 
                              centers = centers, 
                              random_state = seed)
        elif n_peaks[i] ==  2:
            rd.seed(seed)
            center_std = [rd.uniform(std_min, std_max) for p in range(n_peaks[i])]
            centers  = [[rd.gauss(0, mean_std)], 
                        [rd.gauss(0 + center_dist, mean_std)]]
            # Randomly assign cells to the positive and negative peak
            # Slightly favors the negative peak to reflect a biological setting
            n_peak1 = int(rd.randrange(0.6 * n_cells, 0.8 * n_cells))
            n_peak2 = n_cells - n_peak1
            X, y = make_blobs(n_samples = [n_peak1, n_peak2], 
                              n_features = 1, 
                              cluster_std = center_std, 
                              centers = centers, 
                              random_state = seed)
        else:
            rd.seed(seed)
            center_std = [rd.uniform(std_min, std_max) for p in range(n_peaks[i])]
            centers = [[rd.gauss(0, mean_std)], 
                       [rd.gauss(0 + center_dist, mean_std)], 
                       [rd.gauss(0 + (2 * center_dist), mean_std)]]
            # Randomly assign cells to three different peaks
            # Slightly favors the negative peak to reflect a biological setting
            n_peak1 = int(rd.randrange(0.6 * n_cells, 0.8 * n_cells))
            n_peak2 = int(rd.randrange(0.1 * n_cells, 0.2 * n_cells))
            n_peak3 = n_cells - n_peak1 - n_peak2
            X, y = make_blobs(n_samples = [n_peak1, n_peak2, n_peak3], 
                              n_features = 1, 
                              cluster_std = center_std, 
                              centers = centers, 
                              random_state = seed)
        # Add simulated data as a column to the dataframe
        simulated_data[str(i)] = pd.DataFrame(X)
        seed += 1
    return simulated_data





def simulate_reference(n_samples, n_markers, n_cells, mean_std, std_range, 
                    center_dist, random_state):
    """Creates a collection of simulated flow cytometry-like data using 
    Gaussian distributions.

    Parameters:
        n_samples: Total number of samples to generate.
        n_markers (int): Number of markers (columns) to simulate.
        n_cells (int): Number of cells (rows) to simulate per sample.
        mean_std (float): Standard deviation of Gaussian center selection.
        std_range (tuple): Minimum and maximum to use when randomly assigning 
        width of Gaussian distributions.
        center_dist (float): Distance to seperate Gaussians.
        random_state (int): Random state to use in sampling steps.
        out_ratio (float): Proportion of outlier samples.
        n_tweak (int): Number of channels showing outliers
        

    Returns:
        pd.DataFrame containing simulated data. 
    """
    # Assign a random number of peaks (1-3) across the markers
    rd.seed(10)
    n_peaks = [rd.randrange(2, 4) for i in range(n_markers)]
    reference_cohort = []

    # Simulate reference samples
    for i in range(n_samples):
        df = simulate_sample(n_markers = n_markers, 
                             n_cells = n_cells,
                             n_peaks = n_peaks, 
                             mean_std = mean_std,
                             std_range = std_range, 
                             center_dist = center_dist,
                             seed = random_state)
        random_state += 100
        df["sample_name"] = "ref_sample_" + str(i+1)
        reference_cohort.append(df)
    reference_cohort = pd.concat(reference_cohort)
    reference_cohort['sample_type'] = 'reference'
    
    return reference_cohort

def simulate_outlier(n_samples, n_markers, n_tweaks, n_cells, mean_std, std_range, 
                    center_dist, random_state):
    # Use the same n_peaks list from the reference
    rd.seed(10)
    n_peaks = [rd.randrange(2, 4) for i in range(n_markers)][:n_tweaks]
    outlier_cohort = []
    
    # Simulate partial outplier samples
    for i in range(n_samples):
        out_df = simulate_sample(n_markers = n_tweaks,
                             n_cells = n_cells,
                             n_peaks = n_peaks[:n_tweaks],
                             mean_std = mean_std,
                             std_range = std_range,
                             center_dist = center_dist,
                             seed = random_state)
        random_state += 100
        outlier_cohort.append(out_df)                              
    outlier_cohort = pd.concat(outlier_cohort)
    
    return outlier_cohort

def merge_ref_out(reference_cohort, outlier_cohort):
    reference_cohort["sample_type"] = "reference"
    reference_cohort.iloc[(len(reference_cohort) - len(outlier_cohort)):,:outlier_cohort.shape[1]] = outlier_cohort
    reference_cohort.iloc[(len(reference_cohort) - len(outlier_cohort)):, -2] = reference_cohort.iloc[(len(reference_cohort) - len(outlier_cohort)):, -2].str.replace("ref","out")
    reference_cohort.iloc[(len(reference_cohort) - len(outlier_cohort)):, -1] = "outlier"    
    return reference_cohort

    

def main():
    args = parse_args_simulation()
    # Common variables
    n_samples = args.n_samples
    n_markers = args.n_markers
    n_cells = args.n_cells
    n_tweaks = args.n_tweaks
    
    # Reference variables
    ref_mean_std = args.ref_mean_std
    ref_std_range = args.ref_std_range
    ref_std_range = [float(i) for i in ref_std_range.split(',')]
    ref_center_dist = args.ref_center_dist

    # Outlier variables
    outlier_ratio = args.outlier_ratio
    outlier_mean_std = args.outlier_mean_std
    outlier_std_range = args.outlier_std_range
    outlier_std_range = [float(i) for i in outlier_std_range.split(',')]
    outlier_center_dist = args.outlier_center_dist

    # Generate reference samples
    ref_cohort = simulate_reference(n_samples = n_samples,
                                 n_markers = n_markers, 
                                 n_cells = n_cells,
                                 mean_std = ref_mean_std,
                                 std_range = ref_std_range, 
                                 center_dist = ref_center_dist,
                                 random_state = 100000)
    
    # Generate outlier portions
    if outlier_ratio > 0.5:
        print("Error: Outlier ratio should be less than or equal to 0.5!")
        quit()
    elif outlier_ratio == 0:
        final = ref_cohort
    else:
        out_cohort = simulate_outlier(n_samples = int(outlier_ratio * n_samples),
                                      n_markers = n_markers,
                                      n_tweaks = n_tweaks,
                                      n_cells = n_cells,
                                      mean_std = outlier_mean_std,
                                      std_range = outlier_std_range,
                                      center_dist = outlier_center_dist,
                                      random_state = 200000)
        final = merge_ref_out(ref_cohort, out_cohort)

    final.to_csv(args.out, index = False)

if __name__ ==  '__main__':
    main()
