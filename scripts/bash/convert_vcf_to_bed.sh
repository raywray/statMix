#!/bin/bash
vcf_file=$1
output_prefix=$2

plink2 --vcf $vcf_file --make-bed --out $output_prefix --allow-extra-chr
awk '{$1="0";print $0}' $output_prefix.bim > $output_prefix.bim.tmp
mv $output_prefix.bim.tmp output/plink/$output_prefix.bim
mv $output_prefix* output/plink/