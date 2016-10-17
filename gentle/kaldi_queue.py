from Queue import Queue

from . import standard_kaldi
from . import config

def build(nthreads=4, hclg_path=None):

    if hclg_path is None: hclg_path = config.resources.full_hclg_path

    kaldi_queue = Queue()
    for i in range(nthreads):
        kaldi_queue.put(standard_kaldi.Kaldi(
            config.resources.nnet_gpu_path,
            hclg_path,
            config.resources.proto_langdir,
            config.arate)
        )
    return kaldi_queue
