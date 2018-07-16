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

vcf = config['vcf']
size_file = config['size']
chunk_size = int(config['chunk'])

tabVcf = pysam.TabixFile(vcf)
CHROMOSOMES = tabVcf.contigs
tabVcf.close()

chromEndDict = {}
with open(size_file) as f:
    for line in f:
        line_list = line.split()
        chrom = line_list[0]
        end = int(line_list[1])
        chromEndDict[chrom] = end

CHUNKS = []
for chrom in CHROMOSOMES:
    if not chrom.startswith('chr'):
        chrom = 'chr' + chrom
    if not chromEndDict.get(chrom):
        print('Chromsome ' + chrom + ' not in size file.')
        sys.exit(1)
    chromEnd = chromEndDict[chrom]
    if config['small_vcf'] != 'NO':
        CHUNKS.append('.'.join([chrom, '0', str(chromEnd)]))
    else:
        for i in range(0, chromEnd, chunk_size):
            start = str(i)
            end = str(i + chunk_size)
            CHUNKS.append('.'.join([chrom, start, end]))


include: 'modules/Snakefile_splitVcf'
include: 'modules/Snakefile_avinput'
include: 'modules/Snakefile_InterVar'
include: 'modules/Snakefile_annotate'

rule all:
    input:
        'InterVar_bed/build.intervar.bed.gz.tbi',
        'variants_InterVar_annotated.vcf.gz.tbi'

