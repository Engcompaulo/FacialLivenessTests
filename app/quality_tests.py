# from metric_vector import DefaultMetricVectorCreator
from liveness.quality.metrics.md import   MaximumDifferenceMetric
from liveness.quality.metrics.mse import  MeanSquaredErrorMetric
from liveness.quality.metrics.nae import  NormalisedAbsoluteErrorMetric
from liveness.quality.metrics.nxc import  NormalisedCrossCorrelationMetric
from liveness.quality.metrics.psnr import PeakSignalToNoiseRatioMetric
from liveness.quality.metrics.sc import   StructuralContentMetric
from liveness.quality.metrics.snr import  SignalToNoiseRatioMetric
from liveness.quality.metrics.ad import   AverageDifferenceMetric
from liveness.quality.metrics.lmse import LaplacianMeanSquaredMetric
from liveness.quality.metrics.gme import  GradientMagnitudeErrorMetric
from liveness.quality.metrics.gpe import  GradientPhaseErrorMetric
from liveness.quality.metrics.sme import  SpectralMagnitudeErrorMetric
from liveness.quality.metrics.spe import  SpectralPhaseErrorMetric
from liveness.quality.metrics.tcd import  TotalCornerDifferenceMetric
from liveness.quality.metrics.gme import GradientMagnitudeErrorMetric
from liveness.quality.metrics.gpe import GradientPhaseErrorMetric
from liveness.quality.metrics.sme import SpectralMagnitudeErrorMetric
from liveness.quality.metrics.spe import SpectralPhaseErrorMetric
from liveness.quality.metrics.tcd import TotalCornerDifferenceMetric
from liveness.quality.metrics.mas import MeanAngleSimilarityMetric
from liveness.quality.metrics.mams import MeanAngleMagnitudeSimilarityMetric
from liveness.quality.metrics.jqi import JPEGQualityIndexMetric
import cv2
import logging
def main():
    logger = logging.getLogger()

    image = cv2.imread('/home/ryan/datasets/nuaa/ClientRaw/0001/0001_00_00_02_2.jpg')

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gaussian_image = cv2.GaussianBlur(image,(5,5),0)

    m = JPEGQualityIndexMetric(logger)
    print(m.calculate(image))


if __name__ == '__main__':
    main()