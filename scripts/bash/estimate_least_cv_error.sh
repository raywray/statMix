#!/bin/bash
admixture_dir_path=$1
output_prefix=$2

cd $admixture_dir_path
grep "CV" *out | awk '{print $3,$4}' | sed -e 's/(//;s/)//;s/://;s/K=//'  > $output_prefix.cv.error
grep "CV" *out | awk '{print $3,$4}' | cut -c 4,7-20 > $output_prefix.cv.error
awk '/CV/ {print $3,$4}' *out | cut -c 4,7-20 > $output_prefix.cv.error