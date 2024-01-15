from argparse import ArgumentParser, RawTextHelpFormatter


#########################
### UTILITY FUNCTIONS ###
#########################
# Define default variables for functions
# simulation_sm.py is updated

def parse_args_simulation():
    """Parses inputs from commandline and returns them as a Namespace object."""

    parser = ArgumentParser(prog = 'python3 simulation_sm.py',
        formatter_class = RawTextHelpFormatter, description =
        '  Create a simulated FCM data as a .csv output.\n\n'
        '  Example syntax:\n'
        '    python3 simulation_sm.py -ns 100 -pstd 0.5 \n')
                            
    # Optionals
    parser.add_argument('-ns', '--n_sample', dest='n_sample', type=int, default = 100,
                        help='number of samples')
    parser.add_argument('-nm', '--n_marker', dest='n_marker', type=int, default = 8,
                        help='number of markers')
    parser.add_argument('-nc', '--n_cells', dest='n_cells', type=int, default = 2000,
                        help='number of cells in each sample')
    parser.add_argument('-pstd', '--peak_std', dest='peak_std', type=float, default = 0.2,
                        help='basic standard deviation of peaks')
    parser.add_argument('-c', '--center', dest='center', type=int, default = 1,
                        help='center of the first peak')
    parser.add_argument('-d', '--distance', dest='distance', type=int, default = 3,
                       help='average distance between multiple peaks')
    parser.add_argument('-mp', '--max_peak', dest='max_peak', type=int, default = 3,
                       help='maximum peak number \n'
                       'each marker will have random number of peaks within the max peak range')
    parser.add_argument('-rr', '--ref_ratio', dest='ref_ratio', type = float, default = 0.8,
                       help='ratio of reference and novelties in the simulated data')
    parser.add_argument('-on', '--out_name', dest='out_name', type = str, default = 'simulation_output.csv',
                       help='name of the output file \n'
                       'default is set to "simulation_output.csv"')

    return parser.parse_args()

def parse_args_stat_features():
    """Parses inputs from commandline and returns them as a Namespace object."""

    parser = ArgumentParser(prog = 'python3 feature_generation.py',
        formatter_class = RawTextHelpFormatter, description =
        '  Create a dataframe summarizing fcm data with mean, median, std, and IQR.\n\n'
        '  Example syntax:\n'
        '    python3 feature_generation.py \n')
    
    # Positional
    parser.add_argument('input', type=str,
                        help='a dataframe converted from FCM data or simulated one')
                            
    # Optionals
    parser.add_argument('-on', '--out_name', dest='out_name', type = str, default = 'feature_generation_output.csv',
                       help='name of the output file \n'
                       'default is set to "feature_generation_output.csv"')

    return parser.parse_args()

def parse_args_outlier_detection():
    """Parses inputs from commandline and returns them as a Namespace object."""

    parser = ArgumentParser(prog = 'python3 outlier_detection.py',
        formatter_class = RawTextHelpFormatter, description =
        '  Perform outlier detection on the feature generated data.\n\n'
        '  Example syntax:\n'
        '    python3 outlier_detection.py feature_generated.csv lof PCA \n')

    # Positionals
    parser.add_argument('input', dest='input', type=str,
                        help='input file in csv format')
    parser.add_argument('algorithm', dest='algorithm', type=str, choices = ['lof', 'isoforest'],
                        help='input file in csv format')
    
    # Optionals
    parser.add_argument('-decom', '--decomposition', dest='decom', type=str, choices = ["PCA"], default = None,
                        help='method for decomposition')

    parser.add_argument('-on', '--out_name', dest='out_name', type = str, default = 'simulation_output.csv',
                       help='name of the output file \n'
                       'default is set to "simulation_output.csv"')

    return parser.parse_args()
