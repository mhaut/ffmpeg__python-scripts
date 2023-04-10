
<div id="top"></div>

<div align="center">


<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/FFmpeg_Logo_new.svg/1920px-FFmpeg_Logo_new.svg.png" style="width:200px;"/>

<h3 align="center">FFMPEG Util scripts and Templates</h3>

<p align="center">
    Simple wrapper Python scripts for FFMPEG.
</p>
</div>



##  2. About The Project

This is a collection of Python scripts to automate simple video editing tasks.

They can be easily chained together for more complex video effects and tasks by simply using a JSON configuration file.

These are all based on PYTHON and FFMPEG.

<p align="right">(<a href="#top">back to top</a>)</p>


###  2.1. Installation

These are the steps to get up and running with this theme.

1. Clone the repo
    ```sh
    git clone https://github.com/mhaut/python__bash-scripts
    ```
2. Either update your $PATH to include this folder or create a link in `/usr/local/bin` to each script.
    ```sh
    PATH=$PATH:$(pwd)
    ```

<p align="right">(<a href="#top">back to top</a>)</p>


##  3. Usage


Current list of scripts and their purposes.

| Script               | Description                                                      |
| -------------------- | ---------------------------------------------------------------- |
| `ff_append.py`        | This will concatenate two videos together and re-encode them     |
| `ff_aspect_ratio.py`  | Changes the container metadata's Display Aspect Ratio (DAR)      |
| `ff_blur.sh`          | Simple blur function using an unsharp mask                       |
| `ff_colour.sh`        | Change brightness, contrast, gamma, saturation of video          |
| `ff_concat.sh`        | Concatenate multiple videos together                             |
| `ff_convert.sh`       | Convert an apple quicktime MOV to MP4 file                        |
| `ff_crop.sh`          | Crop video to specific size                                       |
| `ff_cut.sh`           | Cut video from start time to end time.                           |
| `ff_download.sh`      | Use CURL to download multiple files. Useful for scriptflow.        |
| `ff_flip.sh`           | Horizontally and/or vertically flip the video                     |
| `ff_fps.sh`           | Alter the FPS with changing length of video                      |
| -------------------- | ---------------------------------------------------------------- |

<p align="right">(<a href="#top">back to top</a>)</p>


##  4. Reference Repository
Repository based on: [https://github.com/IORoot/ffmpeg__bash-scripts](https://github.com/IORoot/ffmpeg__bash-scripts)
Author Link: [https://github.com/IORoot](https://github.com/IORoot)

<p align="right">(<a href="#top">back to top</a>)</p>
