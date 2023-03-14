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
pip install pandas
```

Note that the above step is only needed when you initially set up the environment. You can skip the above step after the intial setup (see https://rcc-uchicago.github.io/user-guide/midway23/software/apps_and_envs/python/ if you want to learn more about setting up conda environment in midway3)

After the environment is set up, you can run ResMem either by submitting a sbatch job or by running an interactive job.

An example sbatch might look like this:

(if you are using a GPU)
```
#!/bin/sh

#SBATCH --job-name=resmem_gpu
#SBATCH --output=resmem_gpu.out
#SBATCH --error=resmem_gpu.err
#SBATCH --account=pi-[group]
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --constraint=rtx6000   # constraint job runs on rtx6000
#SBATCH --ntasks-per-node=1 # num cores to drive each gpu
#SBATCH --cpus-per-task=1   # set this to the desired number of threads
#SBATCH --mem=16GB

# LOAD MODULES
module load python/anaconda-2022.05
source activate /path/to/environment

# DO COMPUTE WORK
python resmem_folder_gpu.py --loc /path/to/image/files --output_dir /path/where/you/want/the/output/filename.csv
```

(if you are using a CPU)
```
#!/bin/sh

#SBATCH --job-name=resmem_cpu
#SBATCH --output=resmem_cpu.out
#SBATCH --error=resmem_cpu.err
#SBATCH --account=pi-[group]
#SBATCH --partition=caslake
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=16GB

# LOAD MODULES
module load python/anaconda-2022.05
source activate /path/to/environment

# DO COMPUTE WORK
python resmem_folder_cpu.py --loc /path/to/image/files --output_dir /path/where/you/want/the/output/filename.csv
```

When using and sinteractive job, you could use the following command (you should get on a compute node before running this command; see https://rcc-uchicago.github.io/user-guide/midway23/midway_submitting_jobs/#interactive-jobs if you are not familiar):

(if you are using a GPU)
```
module load python/anaconda-2022.05
source activate /path/to/environment
python resmem_folder_gpu.py --loc /path/to/image/files --output_dir /path/where/you/want/the/output/filename.csv
```

(if you are using a CPU)
```
module load python/anaconda-2022.05
source activate /path/to/environment
python resmem_folder_cpu.py --loc /path/to/image/files --output_dir /path/where/you/want/the/output/filename.csv
```

The above commands will run ResMem on all the images in the folder `/path/to/image/files` and save the output to `/path/where/you/want/the/output/filename.csv`. The output file will have two columns: `img_name` and `resmem_pred`. The `img_name` column contains the name of the image file and the `resmem_pred` column contains the ResMem prediction for memorability for the corresponding image.

The decision between using a GPU or a CPU is a bit tricky. The GPU runs much faster - when I tested it on 1,100 720x540 images, the GPU took around 14 seconds while the CPU took around 342 seconds. But there are much more CPU nodes (caslake partition) than GPU nodes (gpu partition) in midway3, so getting a GPU node from the slurm scheduler will take much longer than getting a CPU node.