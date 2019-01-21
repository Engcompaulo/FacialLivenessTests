from datasets.nuaa import NUAADataset
from datasets.replayattack import ReplayAttackDataset
from liveness.generic import DummyLivenessTest
from liveness.quality.model import QualitySVMModel
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
    dataset = NUAADataset(logging.getLogger("c.o.datasets.nuaa"), "/home/ohmgeek_default/datasets/nuaa/")
    dataset.pre_process()

    imposter_set = dataset.read_dataset("attack")
    client_set = dataset.read_dataset("real")
    # Divide dataset into train, and test (40%, 60%)

    # train_set = np.concatenate((train_set, client_set[:int(client_set.shape[0] / 2)]))

    train_vectors = []
    train_outputs = []
    for imposter_img in imposter_set[: int(imposter_set.shape[0] / 2)]:
        try:
            image = cv2.cvtColor(imposter_img, cv2.COLOR_BGR2GRAY)
            gaussian_image = cv2.GaussianBlur(image,(5,5),0)
            vector = vector_creator.create_vector(image, gaussian_image)
            train_vectors.append(vector)
            train_outputs.append(1.0)
        except:
            logger.error("Error while evaluating image.")

    for client_img in client_set[: int(client_set.shape[0] / 2)]:
        try:
            image = cv2.cvtColor(client_img, cv2.COLOR_BGR2GRAY)
            gaussian_image = cv2.GaussianBlur(image,(5,5),0)
            vector = vector_creator.create_vector(image, gaussian_image)
            train_vectors.append(vector)
            train_outputs.append(0.0)
        except:
            logger.error("Error while evaluating image")
    
    model = QualitySVMModel()
    # Evaluate on testing set
    print("Now training")
    model.train(train_vectors, train_outputs)
    print("Trained.")
    print("")
    print("Now saving")
    model.save()
    print("Saved.")
    print("")
    print("Output Results:")
    print(model.test(train_vectors, train_outputs))

if __name__ == "__main__":
    main()
