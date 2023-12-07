"""Program to collect machine data between two timestamps.

This script allows the user to filter machine data (numerical and audio)
between two timestamps specified in the command line. The script will
output the filtered data into a new directory with the same structure.

The script uses the constants to determine the location of the input
data, the names of the individual files, and the output directory.

This script requires that `pandas` and `scipy` to be installed 
within the Python environment you are running this script in.

This file can also be imported as a module and contains the following
functions:
- `extract_audio` - extracts audio data between two timestamps and returns an array
- `extract_raw` - extracts raw data between two timestamps and returns a dataframe
- `time_encoder` - converts a pandas timestamp to a string
- `time_decoder` - converts a file name string to a pandas timestamp
- `main` - the main function of the script
"""

import pandas as pd
import argparse
import os
from scipy.io import wavfile
import re
import math

#================================================= GLOBAL VARS =================================================#
RAW = "/mnt/w/krpm/raw/"                                                    # Location of raw files
AUDIO = "/mnt/w/krpm/audio/"                                                # Location of audio files
OUTPUT = "/mnt/w/krpm/good_1/"                                              # Location of output files
TZ = 'EST'                                                                  # Timezone for timestamps
SENSORS = { "sensor0": [] , "sensor2" : [] }                                # To store files of audio sensors
RAWS = []                                                                   # List of raw files (don't change)
MACHINE = "KR_Mazak1"                                                       # Machine name
#==============================================================================================================#

def time_encoder(time: pd.Timestamp) -> str:
    """Converts a pandas timestamp to a string.

    Args:
        time : pd.Timestamp
            Timestamp to convert.

    Returns:
        str
    """
    
    return time.strftime("%Y%m%d_%H%M%S.%f")

def time_decoder(time: str) -> pd.Timestamp:
    """Converts a string to a pandas timestamp.

    Args:
        time : str
            Timestamp in the format YYYYMMDD_HHMMSS

    Returns:
        pd.Timestamp
    """
    
    return pd.Timestamp(time[0:4] + "-" + time[4:6] + "-" + time[6:8] + " " + time[9:11]
                        + ":" + time[11:13] + ":" + time[13:15] + "." + time[16:], tz=TZ)

def extract_audio(start: pd.Timestamp, end: pd.Timestamp, audio_files: list, out_dir: str) -> None:
    """Extract audio data between two timestamps and write to file.

    Args:
        start : pd.Timestamp
            Start timestamp.
        end : pd.Timestamp
            End timestamp.
        audio_files : list
            List of audio files.
        out_dir : str
            Output directory.

    Returns:
        None
    """
    
    # Find first audio file that contains data
    i = 0
    sensor = re.split('[_.]', audio_files[i])[-2]
    file_start = time_decoder(audio_files[i].split("/")[-1].split("Z")[0])
    while i < len(audio_files) and file_start + pd.Timedelta(30, unit="m") < start:
        i += 1
        file_start = time_decoder(audio_files[i].split("/")[-1].split("Z")[0]) 
    
    if i == len(audio_files):
        print("No audio files found for sensor " + sensor)
        return
    
    # Trim first audio file
    rate, data = wavfile.read(audio_files[i])
    
    # start time + 1/rate * index >= start
    start_index = math.ceil((start - file_start).total_seconds() * rate)
    data = data[start_index:]
    file_start += pd.Timedelta(start_index / rate, unit="s")
    
    # Write to file
    wavfile.write(out_dir + time_encoder(file_start) + "Z_" + MACHINE + "_" + sensor + ".wav", rate, data)
    print("Extracted from " + audio_files[i])
    
    # Middle audio files
    j = i + 1
    file_start = time_decoder(audio_files[j].split("/")[-1].split("Z")[0])
    while j < len(audio_files)and file_start + pd.Timedelta(30, unit="m") < end:
        # Copy file to output directory
        os.system("cp " + audio_files[j] + " " + out_dir)
        print("Extracted from " + audio_files[j])
        j += 1
        file_start = time_decoder(audio_files[j].split("/")[-1].split("Z")[0])
        
    # Trim last audio file
    rate, data = wavfile.read(audio_files[j])
    end_index = math.floor((end - file_start).total_seconds() * rate)
    data = data[:end_index + 1]
    
    # Write to file
    wavfile.write(out_dir + time_encoder(file_start) + "Z_" + MACHINE + "_" + sensor + ".wav", rate, data)
    print("Extracted from " + audio_files[j])
    
    print("Extracted " + str(j - i + 1) + " audio files from " + sensor)
        
    return

def extract_raw(start: pd.Timestamp, end: pd.Timestamp, raw_file: str, out_dir: str) -> None:
    """Extract raw data between two timestamps and write to file.

    Args:
        start : pd.Timestamp
            Start timestamp.
        end : pd.Timestamp
            End timestamp.
        raw_file : str
            Raw file.
        out_dir : str
            Output directory.

    Returns:
        None
    """
    
    if raw_file.endswith("dataitem.csv") or raw_file.endswith("device.csv"):
        # Copy file to output directory
        os.system("cp " + RAW + raw_file + " " + out_dir)
        print("Copied " + raw_file + " to " + out_dir)
        return
    
    # Read raw file:
    with open(RAW + raw_file, "r") as f:
        header = f.readline()
        cols = re.findall('"([^"]*)"', header)
        
        try:
            col = header.split(",").index("\"timestamp\"")
        except ValueError:
            print("Could not find timestamp column in " + raw_file)
            return
            
        output_data = []
        
        line = f.readline()
        if (len(re.findall('"([^"]*)"', line)) != len(cols)-1):       # there are some lines with "\n" that breaks the line reading
            line += f.readline()
        timestamp = pd.Timestamp(re.findall('"([^"]*)"', line)[col], tz=TZ)
        while timestamp < start:
            line = f.readline()
            if (len(re.findall('"([^"]*)"', line)) != len(cols)-1):
                line += f.readline()
                
            timestamp = pd.Timestamp(re.findall('"([^"]*)"', line)[col], tz=TZ)
            
        while timestamp <= end:
            output_data.append(line)
            line = f.readline()
            if (len(re.findall('"([^"]*)"', line)) != len(cols)-1):       
                line += f.readline()
                
            timestamp = pd.Timestamp(re.findall('"([^"]*)"', line)[col], tz=TZ)
        
    # Write to file
    with open(out_dir + raw_file, "w") as f:
        f.write(header)
        for line in output_data:
            f.write(line)
            
    print("Extracted " + str(len(output_data)) + " lines from " + raw_file)
    
    return

def main():
    
    global RAWS
    global SENSORS
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'start_time',
        type=str,
        help='Start timestamp in the format YYYY-MM-DD HH:MM:SS'
    )
    parser.add_argument(
        'end_time',
        type=str,
        help='End timestamp in the format YYYY-MM-DD HH:MM:SS'
    )
    
    args = parser.parse_args()
    
    # Verify that the start and end timestamps are valid
    try:
        start = pd.Timestamp(args.start_time, tz=TZ)
    except ValueError:
        print("Invalid start timestamp.")
        return
    
    try:
        end = pd.Timestamp(args.end_time, tz=TZ)
    except ValueError:
        print("Invalid end timestamp.")
        return
    
    if start > end:
        print("Start timestamp must be before end timestamp.")
        return
         
    # Verify output directory does not exist
    if os.path.isdir(OUTPUT):
        print("Output directory already exists.")
        return
    
    # Verify raw and audio directories exist
    if not os.path.isdir(RAW):
        print("Raw directory does not exist.")
        return
    else: 
        RAWS = [f for f in os.listdir(RAW)]
        if len(RAWS) == 0:
            print("No raw files found.")
    
    if not os.path.isdir(AUDIO):
        print("Audio directory does not exist.")
        return
    else:
        # Recursively search all for audio files
        for root, dirs, files in os.walk(AUDIO):
            for file in files:
                file_parts = file.split(".")
                if file_parts[-1] == "wav":
                    SENSORS[file_parts[1].split("_")[-1]].append(os.path.join(root, file))
                    
        for sensor in SENSORS:
            if len(SENSORS) == 0:
                print("No audio files found for sensor " + sensor)

    # Create raw and audio directories in output directory
    os.mkdir(OUTPUT)
    os.mkdir(OUTPUT + "raw/")
    os.mkdir(OUTPUT + "audio/")
    for sensor in SENSORS:
        os.mkdir(OUTPUT + "audio/" + sensor + "/")
    
    # Extract raw data
    for file in RAWS:
        extract_raw(start, end, file, OUTPUT + "raw/")
            
    # Extract audio data
    for sensor in SENSORS:
        extract_audio(start, end, sorted(SENSORS[sensor]), OUTPUT + "audio/" + sensor + "/")
    
    return

if __name__ == '__main__':
    main()
