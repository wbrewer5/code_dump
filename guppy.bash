#see what config file is needed based on the flowcell and kit used
guppy_basecaller -print_workflows

#find flowcell and ligation kit used and insert config file to below line after "-c"

guppy_basecaller -i ./*fast5 -s ./guppy_out -c  -x "cuda:0"
