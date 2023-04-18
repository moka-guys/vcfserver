#!/usr/bin/env python

import os
import pysam

class VCFs(dict):
    def __init__(self, configs):
        '''
        create VCF readers from configs

        Args:
            configs (dict): list of vcf configs

        Returns:
            None
        '''
        for config in configs:
            # create reader
            vcf = os.path.join(config['directory'], config['source']['vcf'].split('/')[-1])
            tbi = os.path.join(config['directory'], config['source']['tbi'].split('/')[-1])
            self[config['id']] = pysam.VariantFile(vcf, index_filename=tbi)


    def ids(self):
        return self.keys()

    def fetch_position(self, id, chrom, pos, ref, alt):
        '''
        Fetches positional data from VCF

        Args:
            id (str): name of the VCF file
            chrom (str): chromosome
            pos (int): position
            ref (str): reference allele
            alt (str): alternative allele

        Returns:
            list: list of objects matching the given name

        '''
        vcf = self.get(id)
        if vcf:
            vars = vcf.fetch(contig=chrom, start=pos-1, end=pos+len(ref)-1)
            if vars:
                for record in vars:
                    if record.chrom == chrom and record.pos == int(pos) \
                        and record.ref == ref and record.alts and record.alts[0] == alt:
                        return record
            return None
