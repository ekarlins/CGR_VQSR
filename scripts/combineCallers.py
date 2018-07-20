#!/usr/bin/python
import sys
'''
usage: module load python/2.7;python combineCallers.py Caller1 Caller2 CallerN /path/to/Caller1.vcf /path/to/Caller2.vcf... /path/to/CallerN.vcf /path/to/SNP.out.vcf /path/to/INDEL.out.vcf
Caller1.vcf will be used as the line that is kept for the output variant calls.
both /path/to/SNP.out.vcf and /path/to/INDEL.out.vcf will have a variable called "set" added to INFO that says which callers are the variant.
Caller1 Caller2 CallerN will be the name used in "leftAlignSet". So these should be something like "HC", "FB", "UG".
'''


def getHetAd(format, genotypes):
    '''
    (str, list) -> str
    '''
    altSum = 0
    totSum = 0
    gtCol = None
    adCol = None
    format_list = format.split(':')
    for i in range(len(format_list)):
        if format_list[i] == 'GT':
            gtCol = i
        elif format_list[i] == 'AD':
            adCol = i
    if gtCol == None or adCol == None:
        print('FORMAT field incorrect')
        sys.exit(1)
    for geno in genotypes:
        geno_list = geno.split(':')
        gt = geno_list[gtCol]
        ad = geno_list[adCol]
        if gt == '0/1':
            ad_list = ad.split(',')
            refCount = int(ad_list[0])
            altCount = int(ad_list[1])
            altSum += altCount
            totSum += refCount + altCount
    if altSum == 0 or totSum == 0:
        return ''
    else:
        return str(float(altSum)/float(totSum))



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
        outputSnp.write('##INFO=<ID=hetAltAB,Number=1,Type=Float,Description="(ALT AD)/(TOT AD) summed at het sites.">\n')
        outputSnp.write(line)
        outputIndel.write('##INFO=<ID=leftAlignSet,Number=.,Type=String,Description="list of variant callers that called variant, matched on left align trimmed VCF files">\n')
        outputIndel.write('##INFO=<ID=hetAltAB,Number=1,Type=Float,Description="(ALT AD)/(TOT AD) summed at het sites.">\n')
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
            format = line_list[8]
            genotypes = line_list[9:]
            hetAB = getHetAd(format, genotypes)
            info = line_list[7]
            if hetAB == '':
                line_list[7] = info + ';leftAlignSet=' + leftAlignSet
            else:
                line_list[7] = info + ';leftAlignSet=' + leftAlignSet + ';hetAltAB=' + hetAB
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

