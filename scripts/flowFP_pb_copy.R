# Record the start time
start_time <- Sys.time()

#Load libraries
library(dplyr)
library(tidyr)
library(flowAssist)
library(flowFP)
library(optparse)


# Call the arguments from terminal
option_list = list(
  make_option(c("-i", "--input"), type="character", default = NULL, help="Input FCM file"),
  make_option(c("-n", "--n_recursion"), type="integer", default=4, help="Number of bins as 2 power of n"),
  # make_option(c("-p", "--params"), action="store", type="character", default=NULL , help="List of parameters to be used on the flowFP model"),
  make_option(c('-o', '--output'), type="character", default="pb_features.csv", help="Output file name")
)

# Parse the command-line arguments
opt_parser = OptionParser(option_list=option_list)
opt = parse_args(opt_parser)

# input csv file as arg1
if(!is.null(opt$input)){
df = read.csv(opt$input)
} else{
  stop("Input file must be supplied.", call.=FALSE)
}

# Access the option values using the option names
n_recursion = opt$n_recursion
output = opt$output

# A function to downsample DataFrame to build a reference
downsample_df_to_fcss_reference = function(df){
  samples = unique(df$sample_name)
  ff = list()
  for(i in samples){
    temp_sample = dplyr::filter(df, sample_name == i) %>% dplyr::select(-sample_name, -sample_type)
    temp_sample = temp_sample[sample(nrow(temp_sample), as.integer(0.2*length(temp_sample))), ]
    temp_ff = DFtoFF(temp_sample)
    ff = append(ff, temp_ff)
  }
  ref = flowSet(ff)
  return(ref)
}

# A function to build flowSet outof simulated data
split_df_to_fcss = function(df){
  samples = unique(df$sample_name)
  ff = list()
  for(i in samples){
    temp_sample = dplyr::filter(df, sample_name == i) %>% dplyr::select(-sample_name, -sample_type)
    temp_ff = DFtoFF(temp_sample)
    ff = append(ff, temp_ff)
  }
  fs = flowSet(ff)
  return(fs)
}

ref = downsample_df_to_fcss_reference(df)
fs = split_df_to_fcss(df)
# fs_downsampled = fs[sample(nrow(fs),as.integer(0.2*length(fs))),]

model = flowFPModel(reformulate(), nRecursions = n_recursion)
call = flowFP(fs, model)
features = counts(call)
features = t(apply(features, 1, function(x) x/sum(x)))
features = data.frame(features)

features$sample_name = unique(df$sample_name)
features$sample_type = df$sample_type[match(features$sample_name, df$sample_name)]


write.table(features, output, row.names = FALSE, sep = ",")

# Record the end time
end_time <- Sys.time()

# Calculate the runtime
runtime <- end_time - start_time

# Print the runtime
cat("Script runtime:", runtime, "\n")
