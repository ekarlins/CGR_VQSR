#!/usr/bin/python


'''
This is to run a SnakeMake to add InterVar annotation to a VCF file
'''

import glob
import sys
import os
import pysam
import shutil
from snakemake.utils import R

configfile: "config.yaml"

PARTS = []
for vcf in sorted(glob.glob(config['HC_parts_dir']) + '/*.vcf'):
    part = os.path.basename(vcf)[:-4].split('_')[-1]
    PARTS.append(part)

include: 'modules/Snakefile_leftAlignTrim'

rule all:
    input:
        'variants_VQSR_input.vcf.gz.tbi'

