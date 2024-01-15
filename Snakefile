###################################
#### Snakemake pipeline Flow Cytometry Data ####
###################################
# N_MARKERS = [8, 16]
N_MARKERS = [8]
# N_TWEAKS = [1, 2, 3]
N_TWEAKS = [1]
# OUTLIER_CENTER_DISTANCES = [3.8, 4.6, 5.4]
OUTLIER_CENTER_DISTANCES = [10]

# OUTLIER_RATIO = [0.05, 0.2]
OUTLIER_RATIO = [0.8]

N_BINS = [10, 20]
N_RECURSIONS = [4, 5]
DIST_METRIC = ["EMD", "KS"]



configfile: "config/config.yaml"

rule all:
        input:
#                 expand(config["output_folder"]+"/simulated/{n_marker}_{n_tweaks}_{outlier_center_dist}_{outlier_ratio}.csv",
#                 n_marker=N_MARKERS, n_tweaks = N_TWEAKS, outlier_center_dist=OUTLIER_CENTER_DISTANCES,
#                 outlier_ratio=OUTLIER_RATIO),
                expand(config["output_folder"] + "/simulated/plots/{n_marker}_{n_tweaks}_{outlier_center_dist}_{outlier_ratio}.png",
                n_marker=N_MARKERS, n_tweaks = N_TWEAKS, outlier_center_dist=OUTLIER_CENTER_DISTANCES,
                outlier_ratio=OUTLIER_RATIO),
                expand(config["output_folder"]+"/feature_generated/stat_feature/{n_marker}_{n_tweaks}_{outlier_center_dist}_{outlier_ratio}_stat_featured.csv",
                n_marker=N_MARKERS, n_tweaks = N_TWEAKS, outlier_center_dist=OUTLIER_CENTER_DISTANCES,
                outlier_ratio=OUTLIER_RATIO),
                expand(config["output_folder"]+"/feature_generated/npb{n_bins}_feature/{n_marker}_{n_tweaks}_{outlier_center_dist}_{outlier_ratio}_npb{n_bins}_featured.csv",
                n_marker=N_MARKERS, n_tweaks = N_TWEAKS, outlier_center_dist=OUTLIER_CENTER_DISTANCES,
                outlier_ratio=OUTLIER_RATIO, n_bins=N_BINS),
                expand(config["output_folder"]+"/feature_generated/pb{n_recursion}_feature/{n_marker}_{n_tweaks}_{outlier_center_dist}_{outlier_ratio}_pb{n_recursion}_featured.csv",
                n_marker=N_MARKERS, n_tweaks = N_TWEAKS, outlier_center_dist=OUTLIER_CENTER_DISTANCES,
                outlier_ratio=OUTLIER_RATIO, n_recursion=N_RECURSIONS),
                expand(config["output_folder"]+"/feature_generated/dist_{dist_metric}_feature/{n_marker}_{n_tweaks}_{outlier_center_dist}_{outlier_ratio}_{dist_metric}_featured.csv", n_marker=N_MARKERS, n_tweaks = N_TWEAKS, outlier_center_dist=OUTLIER_CENTER_DISTANCES,
                outlier_ratio=OUTLIER_RATIO, dist_metric=DIST_METRIC),
                expand(config["output_folder"] + "/simulated/summary/{n_marker}_{n_tweaks}_{outlier_center_dist}_{outlier_ratio}_summary.png", n_marker=N_MARKERS, n_tweaks = N_TWEAKS, outlier_center_dist=OUTLIER_CENTER_DISTANCES, outlier_ratio=OUTLIER_RATIO)


rule simulate_data:
        output:
                config["output_folder"] + "/simulated/{n_marker}_{n_tweaks}_{outlier_center_dist}_{outlier_ratio}.csv"
        shell:
                "python3 scripts/simulation.py -out {output} -n_samples 1000 -n_marker {wildcards.n_marker} -n_tweaks {wildcards.n_tweaks} -outlier_center_dist {wildcards.outlier_center_dist} -outlier_ratio {wildcards.outlier_ratio}"

rule simulation_visualizaion:
        input:
                config["output_folder"] + "/simulated/{n_marker}_{n_tweaks}_{outlier_center_dist}_{outlier_ratio}.csv"
        output:
                config["output_folder"] + "/simulated/plots/{n_marker}_{n_tweaks}_{outlier_center_dist}_{outlier_ratio}.png"
        shell:
                "python3 scripts/simulation_visualization.py {input} {wildcards.n_tweaks} -out {output}"

rule stat_feature:
        input:
                config["output_folder"] + "/simulated/{n_marker}_{n_tweaks}_{outlier_center_dist}_{outlier_ratio}.csv"
        output:
                config["output_folder"]+"/feature_generated/stat_feature/{n_marker}_{n_tweaks}_{outlier_center_dist}_{outlier_ratio}_stat_featured.csv"
        shell:
                "python3 scripts/stat_features.py {input} -out {output}"

rule npb_feature:
        input:
                config["output_folder"] + "/simulated/{n_marker}_{n_tweaks}_{outlier_center_dist}_{outlier_ratio}.csv"
        output:
                config["output_folder"]+"/feature_generated/npb{n_bins}_feature/{n_marker}_{n_tweaks}_{outlier_center_dist}_{outlier_ratio}_npb{n_bins}_featured.csv"
        shell:
                "python3 scripts/npb_features.py {input} -n_bins {wildcards.n_bins} -out {output}"

rule pb_feature:
        input:
                config["output_folder"] + "/simulated/{n_marker}_{n_tweaks}_{outlier_center_dist}_{outlier_ratio}.csv"
        output:
                config["output_folder"]+"/feature_generated/pb{n_recursion}_feature/{n_marker}_{n_tweaks}_{outlier_center_dist}_{outlier_ratio}_pb{n_recursion}_featured.csv"
        shell:
                "Rscript scripts/flowFP_pb.R -i {input} -n {wildcards.n_recursion} -o {output} "

rule dist_feature:
        input:
                config["output_folder"]+"/simulated/{n_marker}_{n_tweaks}_{outlier_center_dist}_{outlier_ratio}.csv"
        output:
                config["output_folder"]+"/feature_generated/dist_{dist_metric}_feature/{n_marker}_{n_tweaks}_{outlier_center_dist}_{outlier_ratio}_{dist_metric}_featured.csv"
        shell:
                "python3 scripts/dist_ref_comparison.py {input} {wildcards.dist_metric} -out {output}"
                
rule simulation_summary:
        input:
                config["output_folder"] + "/simulated/{n_marker}_{n_tweaks}_{outlier_center_dist}_{outlier_ratio}.csv"
        output:
                config["output_folder"] + "/simulated/summary/{n_marker}_{n_tweaks}_{outlier_center_dist}_{outlier_ratio}_summary.png"
        shell:
                "python3 scripts/simulation_summary.py {input} -out {output}"  
        
