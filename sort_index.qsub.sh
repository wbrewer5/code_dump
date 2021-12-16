#!/bin/bash
#PBS -S /bin/bash
#PBS -l partition=monster,nodes=1:ppn=24,walltime=1:00:00
#PBS -n
#PBS -A ACF-UTK0011
#PBS -M wbrewer5@vols.utk.edu
#PBS -m abe
#PBS -o /lustre/haven/user/wbrewer5/macrosiphum/samtools/log/
#PBS -e /lustre/haven/user/wbrewer5/macrosiphum/samtools/error/
#PBS -N macrosiphum_samtools_sort_index


module load samtools

#sort .sam file by start of chromosome, creating .bam file
#samtools sort /lustre/haven/user/wbrewer5/macrosiphum/samtools/macrosiphum.sam -o /lustre/haven/user/wbrewer5/macrosiphum/samtools/macrosiphum.sorted.bam

#index sorted .bam file, creating .bai output 
samtools index -b /lustre/haven/user/wbrewer5/macrosiphum/samtools/macrosiphum.sorted.bam 
