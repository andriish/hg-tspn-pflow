import comet_ml
import torch

import dgl
import dgl.function as fn
from dgl import DGLGraph as DGLGraph

from pytorch_lightning.loggers import CometLogger
from pytorch_lightning import Trainer, profiler
from pytorch_lightning.callbacks import ModelCheckpoint

from dataloader import PflowDataset, collate_graphs

import sys
sys.path.append('./models/')

from models.pflow_model import PflowModel

import glob
import json
import os

import resource
from lightning import PflowLightning

rlimit = resource.getrlimit(resource.RLIMIT_NOFILE)
resource.setrlimit(resource.RLIMIT_NOFILE, (4096, rlimit[1]))

cuda_vis_single_device = '0'
# torch.set_num_threads(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
      print("Usage:  train.py configfile.json [debugflag]")
      sys.exit(1)

    config_path = sys.argv[1]

    if len(sys.argv) >= 3:
        debug_mode = sys.argv[2]
    else:
        debug_mode = '0'

    with open(config_path, 'r') as fp:
         config = json.load(fp)


    ngpus = 1
    os.environ['CUDA_VISIBLE_DEVICES'] = cuda_vis_single_device

    net = PflowLightning(config)

    if config['frozen']:
        checkpoint_path = config['frozen_checkpoint']
        state_dict = torch.load(checkpoint_path)['state_dict']
        net.load_state_dict(state_dict)
        print(f'\nfrozen model loaded from -\n{checkpoint_path}\n')
    print(f"Pytorch version: {torch.__version__}")
    if debug_mode == '1':
        if  config['devicetorun'] =='cuda':
           print("The supported architectures")
           print(torch.cuda.get_arch_list())
           print(torch.cuda.get_device_properties('cuda'))
           
        trainer = Trainer(
            max_epochs = config['num_epochs'],
            #gpus = ngpus,
            accelerator = config['devicetorun'],
            devices = 1,
            default_root_dir = '../rootdir',
            replace_sampler_ddp = False,
            resume_from_checkpoint = config['resume_from_checkpoint'],
        )

    else:
        comet_logger = CometLogger(
            api_key='...',
            save_dir='/home/andriish/Projects/HANSDON/savedir',
            project_name="pflow-hypergraph",
            workspace="...",
            experiment_name=config['name']+'_v'+str(config['version'])
        )

        net.set_comet_exp(comet_logger.experiment)
        comet_logger.experiment.log_asset(config_path,file_name='config')

        all_files = glob.glob('./*.py')+glob.glob('models/*.py')+glob.glob('utility/*.py')
        for fpath in all_files:
            comet_logger.experiment.log_asset(fpath)

        checkpoint_callback = ModelCheckpoint(save_top_k=-1, every_n_epochs=5)

        print('creating trainer')
        trainer = Trainer(
            max_epochs = config['num_epochs'],
            gpus = ngpus,
            default_root_dir = '/storage/agrp/nilotpal/PFlow/experiments/Set2Set/',
            logger = comet_logger,
            callbacks = [checkpoint_callback],
            resume_from_checkpoint = config['resume_from_checkpoint']
        )
    
    if config['parallelization'] == True:
        data_module = PflowDataModule(config)
        trainer.fit(net, data_module)
    else:
        trainer.fit(net)
    sys.exit(0)