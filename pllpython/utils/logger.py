"""Logger Helper Functions

This module provides utility functions to set up logging and save I/O data.
"""
import os
import logging
from time import gmtime, strftime
import numpy as np
# pylint: disable=W1203 disable=W0622


def setup_log(name: str, id: int, settings, csv: bool = True) -> logging:
    """
    Creates and configures a logger instance.

    :param name: Name of the logger.
    :param id: Unique identifier for the log instance.
    :param settings: Configuration object containing logging settings.
    :return: Tuple containing the logger instance and the log file path.
    """
    log = logging.getLogger(f'{name}_{id}')
    log.setLevel(logging.DEBUG)
    file_full = os.path.join(
        settings.log['log_path'],
        f'{settings.name}_{name}_{id}_{strftime("%Y_%m_%d_%H_%M_%S", gmtime())}.log')
    if not os.path.isfile(file_full):
        open(file_full, 'w', encoding='utf-8')

    log.addHandler(logging.FileHandler(filename=file_full, mode='a'))
    log.info(
        f'{"="*10} {strftime("%Y-%m-%d_%H:%M:%S", gmtime())}_{__name__}_{id} {"="*10}')
    log.info(
        f'Settings VCO: {settings.vco}\nLoopFitler: {settings.lf}\nCLK: {settings.clk}\nDivider: {settings.divider}\nLPD: {settings.lpd}')

    if csv:
        file_full = file_full[:-3] + "csv"
        if not os.path.isfile(file_full):
            open(file_full, 'w', encoding='utf-8')

    return log, file_full


def save_io(io_arrays: list[list], headers: list[str], io_file: str):
    """
    Saves I/O data to a CSV file.

    :param io_arrays: List of lists containing data to be saved.
    :param headers: List of column headers for the CSV file.
    :param io_file: Path to the CSV file.
    """
    results = np.asarray(io_arrays)

    np.savetxt(io_file, results.transpose(), delimiter=',', header='')
    with open(io_file, 'r+', encoding='utf-8') as f:
        f.read()
        f.seek(0, 0)
        f.write(f'{" ,".join(headers)}\n')
