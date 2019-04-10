from datasets.nuaa import NUAADataset
from datasets.replayattack import ReplayAttackDataset
from datasets.mad import MaskAttackDataset
from liveness.generic import DummyLivenessTest
from liveness.quality.model import QualitySVMModel, QualityLDAModel
from testframework.tests import TestDummyCase
from testframework.runner import TestRunner
from liveness.quality.metrics.factory import metric_factory
from liveness.quality.metric_vector import DefaultMetricVectorCreator
import cv2
import logging
import numpy as np

def main():
    # first, set log level to display everything we want
    # TODO: change this to warn for production.
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    metrics_names = [
        "ad",
        "biqi",
        "gme",
        "gpe",
        "hlfi",
        "jqi",
        "lmse",
        "mams",
        "mas",
        "md",
        "mse",
        "nae",
        "niqe",
        "nxc",
        "psnr",
        "ramd",
        # "rred",
        "sc",
        "sme",
        "snr",
        "spe",
        "ssim",
        "tcd",
        "ted",
        "vifd"
    ]
    metrics = metric_factory(metrics_names, logger)
    vector_creator = DefaultMetricVectorCreator(metrics)

    print("Running test.py")
    dataset = NUAADataset(logging.getLogger("c.o.datasets.nuaa"), "/home/ryan/datasets/nuaa/")
    dataset.pre_process()

    imposter_set = dataset.read_dataset("ImposterRaw") # ImposterRaw
    client_set = dataset.read_dataset("ClientRaw") # ClientRaw
    # Divide dataset into train, and test (40%, 60%)
    train_vectors = []
    train_outputs = []
    for imposter_img in imposter_set[: int(imposter_set.shape[0])]:
        train_vectors.append(imposter_img)
        train_outputs.append(0.0) # 0.0 -> fake

    for client_img in client_set[: int(client_set.shape[0])]:
        train_vectors.append(client_img)
        train_outputs.append(1.0) # 1.0 -> real
    

    model = QualityLDAModel(logging.Logger("lda_model"))
    # Evaluate on testing set
    print("Now training")
    print(len(train_vectors), len(train_outputs))
    model.train(train_vectors, train_outputs)
    print("Trained.")
    print("")
    print("Now saving")
    model.save('lda_model.pkl')
    print("Saved.")

    # Now we train with ReplayAttack
    print("Now load replay attack for testing")
    dataset = ReplayAttackDataset(logging.getLogger("c.o.datasets.replayattack"), "/home/ryan/datasets/replayAttackDB/", mode='test')
    dataset.pre_process()

    imposter_set = dataset.read_dataset("attack") # ImposterRaw
    client_set = dataset.read_dataset("real") # ClientRaw
    train_vectors = []
    train_outputs = []
    for imposter_img in imposter_set[: int(imposter_set.shape[0])]:
        train_vectors.append(imposter_img)
        train_outputs.append(0.0) # 0.0 -> fake

    for client_img in client_set[: int(client_set.shape[0])]:
        train_vectors.append(client_img)
        train_outputs.append(1.0) # 1.0 -> real
    
    print("Get ready to test")
    score = model.test(train_vectors, train_outputs)
    print("testing finished")
    print(score)

if __name__ == "__main__":
    main()
