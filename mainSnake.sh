#!/bin/bash

module load python/3.5
cd $PWD
mkdir logs
sbcmd="sbatch --cpus-per-task={threads} --mem={cluster.mem}"
sbcmd+=" --time={cluster.time} --partition={cluster.partition}"
sbcmd+=" --out={cluster.out} {cluster.extra}"
snakemake -pr --keep-going --local-cores 1 --jobs 6000 --cluster-config cluster.json --cluster "$sbcmd" --latency-wait 120 all
