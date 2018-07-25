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
GiabSampleDict = config['giab_sample_dict']


def getStartVcf(wildcards):
    return config[wildcards.caller + '_parts_dir'] + '/variant_part_' + wildcards.part + '.vcf'

def getGiabVcf(wildcards):
    return config['giab_vcf_dir'] + '/' + wildcards.giabSamp + '.vcf.gz'

def getGiabBed(wildcards):
    return config['giab_bed_dir'] + '/'+ wildcards.giabSamp + '.hg19.bed'


include: 'modules/Snakefile_leftAlignTrim'
include: 'modules/Snakefile_add_set'
include: 'modules/Snakefile_giab'

rule all:
    input:
        expand('{varType}_combined/variants.vcf.gz.tbi', varType = VariantTypes),
        expand('GiabFP_{varType}_final/variants.vcf.gz', varType = VariantTypes)

