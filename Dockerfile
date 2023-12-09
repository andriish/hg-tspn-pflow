FROM fedora:38
RUN dnf -y update && yum -y clean all 
RUN    dnf -y install 'dnf-command(config-manager)' 'dnf-command(builddep)' 
RUN    dnf copr enable -y averbyts/HEPrpms 
RUN    dnf copr enable -y rezso/ML && \
    dnf -y config-manager --add-repo=https://developer.download.nvidia.com/compute/cuda/repos/rhel8/x86_64/cuda-rhel8.repo && \
    dnf -y module disable nvidia-driver && \
    dnf -y install fedora-workstation-repositories && \
    dnf -y config-manager --enable rpmfusion-nonfree-nvidia-driver && \
    dnf -y install akmod-nvidia --setopt=install_weak_deps=False  && \
    dnf -y install pytorch onnx --setopt=install_weak_deps=False && \
    dnf -y install pytorch dgl --setopt=install_weak_deps=False && \
    dnf -y install pythia8 pythia8-data lhapdf python-lhapdf expat-devel xerces-c-devel clhep-devel --setopt=install_weak_deps=False && \
    dnf -y install HepMC3-devel HepMC3-search-devel HepMC-devel  && \
    dnf -y install gcc-c++ gcc-gfortran cmake && \
    dnf -y install geant4 geant4-devel geant4-data  root python-root COCOA && \
    dnf -y install python-pip python-uproot4 python-seaborn python-numpy python-pandas gc python-tqdm python-scipy python-simplejson python-pyyaml python-certifi python-rich && \
    dnf -y install python-configobj python-sentry-sdk python-jsonschema python-msgpack python-box python-requests-toolbelt  python-wrapt python-websocket-client && \
    dnf -y install python-dulwich python-wurlitzer python-ipython python3-scikit-learn python-zipp && \
    python3 -m pip install comet-ml pytorch-lightning==1.9.2 icecream vector awkward && \
    yum -y clean all && \
    dnf -y clean all 
