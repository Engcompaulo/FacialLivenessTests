"""
Peak Signal to Noise Ratio
"""
import numpy as np

from app.liveness.quality.metrics.generic import AbstractQualityMetric
from app.liveness.quality.metrics.mse import MeanSquaredErrorMetric


class PeakSignalToNoiseRatioMetric(AbstractQualityMetric):
    def calculate(self, image, blurred_image):
        mse_metric = MeanSquaredErrorMetric(self._logger)

        mse = mse_metric.calculate(image, blurred_image)

        max_image_squared_val = np.squared(image).max()

        psnr = 10 * np.log(max_image_squared_val / mse)

        return psnr