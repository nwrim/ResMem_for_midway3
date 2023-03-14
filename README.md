# ResMem_for_midway3

This repo is to set up ResMem to be used in UChicago's High Performance Computing cluser, Midway3.

First we need to set up a conda environment. This can be done by running the following command (replace `/path/to/environment` with the path to the directory where you want to store the environment):

```
module load python/anaconda-2022.05
conda create --prefix=/path/to/environment python=3.9
source activate /path/to/environment
```

Then we install ResMem using PIP using the following command:

```
pip install resmem
```

Note that the above step is only needed when you initially set up the environment. You can skip the above step after the intial setup (see https://rcc-uchicago.github.io/user-guide/midway23/software/apps_and_envs/python/ if you want to learn more about setting up conda environment in midway3)

gpu 14.092345476150513
cpu 342.0627851486206 