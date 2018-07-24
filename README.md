# CGR_VQSR
## Take CGR parts VCF files and push through VQSR on Biowulf

**USAGE:**

*Clone the repo in the directory where you want the output. Preferablly a clean directory with nothing else in it.*

**On Helix or Biowulf:**

```sh
cd /data/username/desired/output/directory
module load git
git clone https://github.com/ekarlins/CGR_VQSR.git
cd CGR_VQSR
```

*Edit "config.yaml" to give the path to your input vcf parts directories (at the very least). 

**On Biowulf:**

```sh
cd /data/username/desired/output/directory/CGR_VQSR
sbatch --mail-type=BEGIN,TIME_LIMIT_90,END --cpus-per-task=2 --mem=2g --partition=norm --time=10-00:00:00 mainSnake.sh
```

*runtime, etc. for all possible input files has not been tested.  You may need to change the time above or parameters in cluster.json accordingly. If pipeline fails due to going over time, simply resubmit using the same command, after adjusting time in cluster.json.  It will only restart the failed jobs.*
