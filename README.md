# krpm-data-collator
Program to collect machine data between timestamps.

## Usage
```
python3 collator.py <start_time> <end_time>
```
where start_time and end_time are in the format `"YYYY-MM-DD HH:MM:SS"`.

The program will collect raw data and audio data between the two timestamps and store them in the
output directory specified in the file.

## Example
Running the program:
```
$ python3 collator.py "2023-10-19 12:58:09.000001" "2023-10-19 13:42:17"
Extracted 31 lines from 231016-231030_condition.csv
Copied 231016-231030_dataitem.csv to /mnt/w/krpm/scrap_1/raw/
Copied 231016-231030_device.csv to /mnt/w/krpm/scrap_1/raw/
Extracted 516 lines from 231016-231030_event.csv
Extracted 45385 lines from 231016-231030_sample.csv
Extracted from /mnt/w/krpm/audio/20231019_123007.558246Z_KR_Mazak1_sensor0.wav
Extracted from /mnt/w/krpm/audio/20231019_130007.794685Z_KR_Mazak1_sensor0.wav
Extracted from /mnt/w/krpm/audio/20231019_133008.084873Z_KR_Mazak1_sensor0.wav
Extracted 3 audio files from sensor0
Extracted from /mnt/w/krpm/audio/20231019_123010.119161Z_KR_Mazak1_sensor2.wav
Extracted from /mnt/w/krpm/audio/20231019_130010.357999Z_KR_Mazak1_sensor2.wav
Extracted from /mnt/w/krpm/audio/20231019_133010.707861Z_KR_Mazak1_sensor2.wav
Extracted 3 audio files from sensor2
```
Output from the program:
```
$ tree /mnt/w/krpm/scrap_1
/mnt/w/krpm/scrap_1
├── audio
│   ├── sensor0
│   │   ├── 20231019_125809.000016Z_KR_Mazak1_sensor0.wav
│   │   ├── 20231019_130007.794685Z_KR_Mazak1_sensor0.wav
│   │   └── 20231019_133008.084873Z_KR_Mazak1_sensor0.wav
│   └── sensor2
│       ├── 20231019_125809.000015Z_KR_Mazak1_sensor2.wav
│       ├── 20231019_130010.357999Z_KR_Mazak1_sensor2.wav
│       └── 20231019_133010.707861Z_KR_Mazak1_sensor2.wav
└── raw
    ├── 231016-231030_condition.csv
    ├── 231016-231030_dataitem.csv
    ├── 231016-231030_device.csv
    ├── 231016-231030_event.csv
    └── 231016-231030_sample.csv

4 directories, 11 files
```

## Known Issues
- The program will not work if the timestamps correspond to a single audio file (< 30 minutes) (I will implement this soon).