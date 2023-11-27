_Coming soon_


# Container 

## Build
To build, do as root `singularity build MPP-pflowenv-fedora38-x86_64-v2.sif  MPP-pflowenv-fedora38-x86_64-v2.def`
Alternatively, to build, do as user `singularity build --fakeroot MPP-pflowenv-fedora38-x86_64-v2.sif  MPP-pflowenv-fedora38-x86_64-v2.def`
`export TMPDIR=$(pwd)/tmp`  might be useful if the default `/tmp` directory is too small
## Run
To run, do  as user  `singularity exec MPP-pflowenv-fedora38-x86_64-v2.sif some_command_I_want`, e.g.
`singularity exec MPP-pflowenv-fedora38-x86_64-v2.sif bash`.

# Data 
https://zenodo.org/records/7699682#.ZFIe_S8RoQ3

https://zenodo.org/records/7699682/files/singleGluonJet_test.root
https://zenodo.org/records/7699682/files/singleQuarkJet_test.root
https://zenodo.org/records/7699682/files/singleQuarkJet_train.root


# Training

Inside the container change the path into `hgflow`.
Then 
  - `export PYTHONPATH=$PYTHONPATH:$(pwd)`
  -  Edit the config file, e.g. `configs/hypergraftest.json`
  -  Get the data: 
     ```
     wget https://zenodo.org/records/7699682/files/singleGluonJet_test.root -O ../data/singleGluonJet_test.root
     wget https://zenodo.org/records/7699682/files/singleQuarkJet_test.root -O ../data/singleQuarkJet_test.root
     wget https://zenodo.org/records/7699682/files/singleQuarkJet_train.root -O ../data/singleQuarkJet_train.root
     ```
  - `python3 train.py configs/hypergraftest.json  1`