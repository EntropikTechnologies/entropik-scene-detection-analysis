# Entropik Scene Detection Analysis

Repository for entropik-scene-detection-analysis package

## Version Required

* Python 3.9

## To create wheel file

```python setup.py sdist bdist_wheel```

## Installation Instructions - Local System

Create a new virtual environment using :

**Conda** : ```conda create -n "env_name" python=3.9```

**Venv** : ```python3 -m venv /path/to/new/virtual/environment```

### Package

Run the below command for installing the package:
``` pip install wheel_file_name --no-cache-dir```

## Testing the script and package

### Exposed Class

### class ProcessMedia

***def init()***

```
:param media_path:
```

***get_scene_detection_analysis(media_path : str)***

```
This function extracts scene detection analysis from the media file.

Args:
    media_path (str): The path of the directory where the media file is located.
Returns:
    dict - scene_detection_results : A dictionary having results of scenes detected in media with start time , end time and frame number.
```

### Input Arguments

* media_path : The input video file path to be processed for scene detection analysis

### Error Codes

```
ENT-DS-ESDA-01 : The media path or file name is not valid.
ENT-DS-ESDA-02 : Scenes extraction from media is failed.
ENT-DS-ESDA-03 : Scene detection algorithm failed while consolidating the results.
```

### Sample Input

```
from entropik_scene_detection_analysis.main import ProcessMedia
detect_scene = ProcessMedia(media_path)
detect_scene.get_scene_detection_analysis()
```

### Sample Output

```
[{'start_time': 0, 'end_time': 34, 'frame_number': 1}, {'start_time': 34, 'end_time': 3433, 'frame_number': 101}, 
{'start_time': 3433, 'end_time': 12034, 'frame_number': 354}, {'start_time': 12034, 'end_time': 13734, 'frame_number': 404},
{'start_time': 13734, 'end_time': 15807, 'frame_number': 465}, {'start_time': 15807, 'end_time': 16861, 'frame_number': 496}]
```




