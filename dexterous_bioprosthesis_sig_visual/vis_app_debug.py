"""Wrapper module for launching the signal visualizer with a RawSignals object.

Provides a convenience function for debugging: pass a RawSignals instance
directly to open the visualizer without loading data from a directory.
"""

import multiprocessing
import tkinter as tk


from dexterous_bioprosthesis_2021_raw_datasets.raw_signals.raw_signals import RawSignals
from dexterous_bioprosthesis_2021_raw_datasets.raw_signals.raw_signals_io import read_signals_from_dirs
from dexterous_bioprosthesis_sig_visual.settings import DATAPATH

from dexterous_bioprosthesis_sig_visual.vis_app import RawSignalVisualizer
import os

DEFAULT_DATA_DIR = os.path.join(DATAPATH, "AW_18_06_2024_EMG")


def run_visualizer(raw_signals: RawSignals):
    """Launch the signal visualizer with the given RawSignals dataset.

    Creates a tkinter root window, initializes the visualizer, and loads
    the provided data immediately.

    Args:
        raw_signals: Collection of raw signals to visualize.

    Example::

        from dexterous_bioprosthesis_sig_visual.vis_app_debug import run_visualizer
        run_visualizer(my_raw_signals)
    """
    multiprocessing.freeze_support()

    root = tk.Tk()
    visualizer = RawSignalVisualizer(root)
    visualizer.pack(side="top", fill="both", expand=True)
    visualizer._data_init(raw_signals)
    root.mainloop()


if __name__ == "__main__":
    raw_set = read_signals_from_dirs(
        DEFAULT_DATA_DIR, parallel_options={"backend": "multiprocessing"}
    )["accepted"]
    run_visualizer(raw_set)
