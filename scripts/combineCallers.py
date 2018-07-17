#!/usr/bin/python
import sys
'''
usage: module load python/2.7;python combineCallers.py Caller1 Caller2 CallerN /path/to/Caller1.vcf /path/to/Caller2.vcf... /path/to/CallerN.vcf /path/to/SNP.out.vcf /path/to/INDEL.out.vcf
Caller1.vcf will be used as the line that is kept for the output variant calls.
both /path/to/SNP.out.vcf and /path/to/INDEL.out.vcf will have a variable called "set" added to INFO that says which callers are the variant.
Caller1 Caller2 CallerN will be the name used in "leftAlignSet". So these should be something like "HC", "FB", "UG".
'''

def makeVariantDict(vcfFile):
    variantDict = {}
    with open(vcfFile) as f:
        line = f.readline()
        while not line.startswith('#CHROM'):
            line = f.readline()
        line = f.readline()
        while line != '':
            line_list = line.split()
            (chrom, pos, snp, ref, alt) = line_list[:5]
            variantDict[(chrom, pos, ref, alt)] = 1
            line = f.readline()
    return variantDict



def outputAnnotated(callerList, snpOut, indelOut):
    if len(callerList) % 2 != 0:
        print('list of callers and caller VCF files must match 1 to 1')
        sys.exit(1)
    midpoint = len(callerList)/2
    callers = callerList[:midpoint]
    otherCallers = callers[1:]
    VCFs = callerList[midpoint:]
    inVcf = VCFs[0]
    variantDictList = []
    for vcf in VCFs[1:]:
        variantDictList.append(makeVariantDict(vcf))
    with open(inVcf) as f, open(snpOut, 'w') as outputSnp, open(indelOut, 'w') as outputIndel:
        line = f.readline()
        while not line.startswith('#CHROM'):
            outputSnp.write(line)
            outputIndel.write(line)
            line = f.readline()
        outputSnp.write('##INFO=<ID=leftAlignSet,Number=.,Type=String,Description="list of variant callers that called variant, matched on left align trimmed VCF files">\n')
        outputSnp.write(line)
        outputIndel.write('##INFO=<ID=leftAlignSet,Number=.,Type=String,Description="list of variant callers that called variant, matched on left align trimmed VCF files">\n')
        outputIndel.write(line)
        line = f.readline()
        while line != '':
            callerSet =[callers[0]]
            line_list = line.split()
            (chrom, pos, snp, ref, alt) = line_list[:5]
            isSnp = False
            if len(ref) == len(alt):
                isSnp = True
            for i in range(len(otherCallers)):
                varCaller = otherCallers[i]
                varDict = variantDictList[i]
                if varDict.get((chrom, pos, ref, alt)):
                    callerSet.append(varCaller)
            leftAlignSet = ','.join(sorted(callerSet))
            info = line_list[7]
            line_list[7] = info + ';' + leftAlignSet
            if isSnp:
                outputSnp.write('\t'.join(line_list) + '\n')
            else:
                outputIndel.write('\t'.join(line_list) + '\n')
            line = f.readline()




def main():
    args = sys.argv[1:]
    if len(args) < 4:
        print ("error: usage: module load python/2.7;python combineCallers.py Caller1 Caller2 CallerN /path/to/Caller1.vcf /path/to/Caller2.vcf... /path/to/CallerN.vcf /path/to/SNP.out.vcf /path/to/INDEL.out.vcf")
        sys.exit(1)
    else:
        indelOut = args[-1]
        snpOut = args[-2]
        callerList = args[:-2] 
        outputAnnotated(callerList,snpOut,indelOut)
        


if __name__ == "__main__":
    main()

