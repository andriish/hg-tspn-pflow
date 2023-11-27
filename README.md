_Coming soon_


# Container 

## Build
To build, do as root `singularity build MPP-pflowenv-fedora38-x86_64-v2.sif  MPP-pflowenv-fedora38-x86_64-v2.def`
Alternatively, to build, do as user `singularity build --fakeroot MPP-pflowenv-fedora38-x86_64-v2.sif  MPP-pflowenv-fedora38-x86_64-v2.def`
`export TMPDIR=$(pwd)/tmp`  might be useful if the default `/tmp` directory is too small
## Run
To run, do  as user  `singularity exec MPP-pflowenv-fedora38-x86_64-v2.sif some_command_I_want`, e.g.
`singularity exec MPP-pflowenv-fedora38-x86_64-v2.sif bash`.


# Training

Inside the container change the path into `hgflow`.
Then 
  - `export PYTHONPATH=$PYTHONPATH:$(pwd)`
  -  Edit the config file, e.g. `configs/hypergraftest.json` to adjust the location of the `incidence_dist_0.01_0.99_20bins.npz`
  - `python3 train.py configs/hypergraftest.json  1`