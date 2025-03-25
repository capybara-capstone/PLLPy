"""Wave comparators

This module provides functions for calculating the normalized mean square error 
(MSE) and cross-correlation between two datasets.
"""

import numpy as np


def mse(data_1: np.ndarray, data_2: np.ndarray) -> float:
    """Calculate the Normalized Mean Square Error (NMSE) between two datasets.

    This function computes the Mean Square Error (MSE) between two input datasets,
    normalizes the MSE by the maximum possible error, and returns the normalized 
    MSE as a percentage.

    :param data_1: First dataset (list or array).
    :param data_2: Second dataset (list or array).
    :return: Normalized Mean Square Error (NMSE) as a percentage.

    :raises ValueError: If the input data arrays have different lengths.

    **Example:**

    .. code-block:: python

        data_1 = [1, 2, 3]
        data_2 = [1, 2, 2]
        result = mse(data_1, data_2)
        print(result)  # Output will be the NMSE percentage.
    """
    if len(data_1) != len(data_2):
        raise ValueError("Input data arrays must have the same length.")

    mse_out = np.mean((np.array(data_1) - np.array(data_2)) ** 2)
    max_possible_error = np.max(
        np.abs(np.array(data_1) - np.array(data_2)))
    normalized_mse = 100 * (1 - mse_out / (max_possible_error ** 2))
    return normalized_mse


def cross_correlation(data_1: np.ndarray, data_2: np.ndarray, mode: str = 'valid') -> float:
    """Calculate the cross-correlation between two datasets.

    This function computes the cross-correlation between two datasets after 
    removing their mean values, and returns the highest correlation value as a 
    percentage.

    :param data_1: First dataset (list or array).
    :param data_2: Second dataset (list or array).
    :param mode: Mode for the cross-correlation computation. 
                 Options are 'full', 'valid', or 'same'. Default is 'valid'.
    :return: Maximum cross-correlation value as a percentage.

    :raises ValueError: If the input data arrays have different lengths.

    **Example:**

    .. code-block:: python

        data_1 = [1, 2, 3]
        data_2 = [3, 2, 1]
        result = cross_correlation(data_1, data_2)
        print(result)  # Output will be the max correlation percentage.
    """
    if len(data_1) != len(data_2):
        raise ValueError("Input data arrays must have the same length.")

    data_1 = np.array(data_1) - np.mean(data_1)
    data_2 = np.array(data_2) - np.mean(data_2)

    correlation = np.correlate(data_1, data_2, mode=mode)

    norm_factor = np.sqrt(np.sum(data_1**2) * np.sum(data_2**2))

    if norm_factor < 1e-10:
        return 0, len(correlation) // 2

    normalized_correlation = correlation / norm_factor
    correlation_percent = 100 * np.max(np.abs(normalized_correlation))

    return correlation_percent
