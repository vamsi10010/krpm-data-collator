"""Program to collect machine data between two timestamps.

This script allows the user to filter machine data (numerical and audio)
between two timestamps specified in the command line. The script will
output the filtered data into a new directory with the same structure.

The script uses the constants to determine the location of the input
data, the names of the individual files, and the output directory.

This script requires that `numpy` and `pandas` be installed within the Python
environment you are running this script in.

This file can also be imported as a module and contains the following
functions:
- `extract_audio` - extracts audio data between two timestamps and returns an array
- `extract_raw` - extracts raw data between two timestamps and returns a dataframe
- `main` - the main function of the script
"""

import pandas as pd
import numpy as np
import argparse
import os

#============================================== CONSTANTS ==============================================#
PREFIX = "231016-231030"                                                    # Prefix for all raw files
RAW = "/mnt/w/krpm/raw/"                                                    # Location of raw files
AUDIO = "/mnt/w/krpm/audio/"                                                # Location of audio files
OUTPUT = "/mnt/w/krpm/output/"                                              # Location of output files
SCHEMA = ["dataitem", "sample", "condition", "event", "device"]             # Schema for raw files
#=======================================================================================================#

def extract_audio(start: pd.Timestamp, end: pd.Timestamp, audio_files: list) -> np.array:
    """Extract audio data between two timestamps.

    Args:
        start : pd.Timestamp
            Start timestamp.
        end : pd.Timestamp
            End timestamp.
        audio_files : list
            List of audio files.

    Returns:
        np.array: Array of audio data.
    """
    return

def extract_raw(start: pd.Timestamp, end: pd.Timestamp, raw_file: str) -> pd.DataFrame:
    """Extract raw data between two timestamps.

    Args:
        start : pd.Timestamp
            Start timestamp.
        end : pd.Timestamp
            End timestamp.
        raw_file : str
            Raw file.

    Returns:
        pd.DataFrame: Dataframe of raw data.
    """
    return

def main():
    return

if __name__ == '__main__':
    main()
