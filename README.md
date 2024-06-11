# statMix
The statMix package is intended to be used to reduce compuational knowledge and time for population genetic analyses. It uses several elements from the PPP pipeline (*Webb et al., 2021*) and VCFtools (*Danecek et al., 2011*). The idea is that all the user has to do is provide a vcf file, select which analyses they would like to perform, and hit play -- the software will do everything else. 

## How to use
### Install statMix
1. Clone this repo onto your machine:
`git clone https://github.com/raywray/statMix.git`
2. Install all necessary conda packages and create a conda environment (will need to have [anaconda](https://docs.anaconda.com/free/anaconda/install/) or [minicoda](https://docs.anaconda.com/free/miniconda/miniconda-install/) installed prior) with the following command: 
`conda env create -f environment.yml`
3. Activate the conda environment: `conda activate stat_mix_env`

### Use statMix
All statMix needs is a vcf file of your population(s) and your choice of summary statistics to run.

- `hwe`: Calculates Hardy Weinberg Equilibrium
- `pop_structure`: Runs a full population structure analysis using admixture and creates plots
- `sfs`: Generates SFS based on the population structure results
- `generic_stats`: Calculates all 'generic' stats: 
    - tajima's D
    - windowed weir Fst
    - weir Fst
    - site pi
    - site pi per population (from population structure analysis)
    - windowed pi
    - windowed pi per population (from population structure analysis)
    - Fit
    - Fis
    - allele frequency
- `fsc`: Generates SFS compatible for fastsimcoal analyses
- `pixy`: Calculates statistics (pi, Fst, dxy) using pixy
- `ima`: Runs an IMa3 analysis (**NOTE**: unfinished)
- `f_stats`: Calculates Eigenstrat F statistics (**NOTE**: unfinished)

(**NOTE:** in order to run `sfs`, `generic_stats`, `fsc`, `ima` or `pixy`, you **MUST** have `pop_structure` too). See `python3 statmix.py --help` for more information.

#### Example Usage
`python3 statmix.py --vcf tigers.vcf --out-prefix tigers --analyses hwe pop_structure sfs generic_stats fsc`

## Output
All results/visualizations can be found in respective subfolders of the `output` directory




