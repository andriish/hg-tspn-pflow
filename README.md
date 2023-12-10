_Coming soon_


# Container 

## Build

# Build on the local host from scratch
To build, do as root `singularity build MPP-pflowenv-fedora38-x86_64-v2.sif  containers/MPP-pflowenv-fedora38-x86_64-v2.def`
Alternatively, to build, do as user `singularity build --fakeroot MPP-pflowenv-fedora38-x86_64-v2.sif  containers/MPP-pflowenv-fedora38-x86_64-v2.def`
`export TMPDIR=$(pwd)/tmp`  might be useful if the default `/tmp` directory is too small
It is recommended to get the latest version of the container.

# Build from the github repository

Instead of the local image, one can use the GitHub Docker image in Singularity, i.e.
`singularity exec docker::/ghcr.io/andriish/hg-tspn-pflow:latest sh` will download the Docker image fromGithub and convert it to singularity.

## Run
To run, do  as user  `singularity exec -B $(pwd):$(pwd) MPP-pflowenv-fedora38-x86_64-v2.sif some_command_I_want`, e.g.

`singularity exec -B $(pwd):$(pwd) MPP-pflowenv-fedora38-x86_64-v2.sif bash`.

# Data 
https://zenodo.org/records/7699682#.ZFIe_S8RoQ3

https://zenodo.org/records/7699682/files/singleGluonJet_test.root
https://zenodo.org/records/7699682/files/singleQuarkJet_test.root
https://zenodo.org/records/7699682/files/singleQuarkJet_train.root

  -  Get the data: 
     ```
     mkdir -p data
     cd data
     wget https://zenodo.org/records/7699682/files/singleGluonJet_test.root -O ../data/singleGluonJet_test.root
     wget https://zenodo.org/records/7699682/files/singleQuarkJet_test.root -O ../data/singleQuarkJet_test.root
     wget https://zenodo.org/records/7699682/files/singleQuarkJet_train.root -O ../data/singleQuarkJet_train.root
     ```


## Training
Please note that as of now all the sxripts are path-sensitive and will not work if executed from wrong directory.

Inside the container change the path into `hgflow`.
Then 
  - `export PYTHONPATH=$PYTHONPATH:$(pwd)`
  -  Edit the config file, e.g. `configs/hypergraftest.json` to adjust the location of the data

The training is doen in two phases.
To run the first phase:

  - `python3 train.py configs/hypergraphtest.json  1`
  
The results will be stored in the directory called something like `rootdir/lightning_logs/version_13/checkpoints/`
To run the second phase:
  - Edit the `configs/hypergraphtest_part2.json` to provide the location of the results from the first phase.
  - `python3 train.py configs/hypergraphtest_part2.json  1`
  
The results will be stored in the directory called something like `rootdir/lightning_logs/version_14/checkpoints/`
Those are the final results.
 
# Training on Raven

Understand that the things like 
  - `module load singularity`  
will not work and build the container somewhere else.
Upload the container via ssh.

## Using the results

To use the results inside the container change the path into `hgflow`.
Then 
  - `export PYTHONPATH=$PYTHONPATH:$(pwd)`
  - Adjust the output path in the eval.py around line 65.
  - Adjust the number of events in eval.py -- REDUCE_DS variable around line 27.
  - `python3 eval.py configs/hypergraphtest_part2.json  /the/path/to/the/saved/final/results/of/step2/training/savedfile.ctx`




  