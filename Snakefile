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

CALLERS = ['HC', 'FB', 'UG']

PARTS = []
for vcf in sorted(glob.glob(config['HC_parts_dir'] + '/*.vcf')):
    part = os.path.basename(vcf)[:-4].split('_')[-1]
    PARTS.append(part)

VariantTypes = ['SNP', 'INDEL']



def getStartVcf(wildcards):
    return config[wildcards.caller + '_parts_dir'] + '/variant_part_' + wildcards.part + '.vcf'


include: 'modules/Snakefile_leftAlignTrim'
include: 'modules/Snakefile_add_set'

rule all:
    input:
        expand('{varType}_combined/variants.vcf.gz.tbi', varType = VariantTypes)

