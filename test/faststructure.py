import os

os.chdir("output/plink")
# ezstructure -K 3 --input=genotypes --output=genotypes_output
os.system("ezstructure -K 4 --input=hops_structure --output=hops_output")

os.system("ezdistruct -K 4 --input=hops_structure --output=testoutput_simple_distruct.svg")