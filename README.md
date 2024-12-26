# ML (Model learning) Processing

This is a project created to automate some tasks for YOLO object detection models. 
Run a docker app on a video and generate dataset for docker training app. Or run object detection on input folder/webcam/external camera.

## Prerequisites

Before you begin, make sure your system meets the following requirements:

### Hardware Requirements
- __NVIDIA GPU__: You’ll need an NVIDIA GPU that supports CUDA. Most modern NVIDIA GPUs do, but it’s always a good idea to check the compatibility of your specific model against the CUDA-enabled GPU list.
- __Sufficient GPU Memory__: Deep learning models can be memory-intensive. Ensure your GPU has enough memory to accommodate the models you plan to train.
### Software Requirements
- __Operating System__: A compatible Linux distribution or Windows. This guide primarily focuses on Linux due to its widespread use in deep learning and development environments. Popular distributions include Ubuntu, CentOS, and Debian.
- __NVIDIA Drivers__: The latest NVIDIA drivers compatible with your GPU and intended CUDA version. These drivers are crucial for enabling the GPU to interface with the operating system and software.
- __Docker__: Ensure you have Docker installed. The version of Docker should be compatible with the NVIDIA Container Toolkit. For most users, the latest version of Docker is recommended.
Docker is required to run the containers. You need to install Docker on your machine, which includes Docker Engine and Docker Compose.
Checkout the [docker](https://github.com/luna-nightbyte/ML-process/tree/main/docker) folder for installation instructions.




## Usage

#### Training
Remember to modify [dataset.yaml](https://github.com/luna-nightbyte/ML-process/blob/main/local/dataset.yaml) for your dataset/Session name. 

#### General
Modify docker compose to use your desired application:
```
x-defaults: &default-settings
  environment:
    # Application settings:
      # ----APP NAME---- 
      # [ detection | ai_label | continuous | train | frame_insert ]
    - APP_NAME=detection


services:
  ML-process:
    <<: *default-settings
    container_name: ml-processor
    volumes:
      - PATH/TO/INPUT/FOLDER:/usr/src/app/data/input:ro
```

Optional during object detection to extract the detected object in a spesific frame size. Add some value to `PADDING=` In the `docker-compose.yml` file to enable extraction, and set your desired output size with `OUTPUT_SIZE=`. The output size can be larger and smaller than the detected object. The frame will be resized while keeping the aspect ratio.
`PADDING=` is intended to be the amount of extra padding around the detected object to extract. But this is not implemented yet. 

This extracted image can then be re-inserted back into the original image using the x.y position saved in a csv file. 

*Note: Always verify any atuo generated annotations using a software like [LabelImg](https://github.com/HumanSignal/labelImg)*

```bash
user@host:/$ git clone https://github.com/luna-nightbyte/ML-process
user@host:/$ cd ./ML-process
user@host:/ML-process$ docker compose up ML-process

[+] Running 0/0
 ⠋ Container ml-processor   Created
Attaching to ml-processor
ml-processor  | 
ml-processor  | ==========
ml-processor  | == CUDA ==
ml-processor  | ==========
ml-processor  | 
ml-processor  | CUDA Version 12.1.1
ml-processor  | 
ml-processor  | Container image Copyright (c) 2016-2023, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
ml-processor  | 
ml-processor  | This container image and its contents are governed by the NVIDIA Deep Learning Container License.
ml-processor  | By pulling and using the container, you accept the terms and conditions of this license:
ml-processor  | https://developer.nvidia.com/ngc/nvidia-deep-learning-container-license
ml-processor  | 
ml-processor  | A copy of this license is made available in this container at /NGC-DL-CONTAINER-LICENSE for your convenience.
ml-processor  | 
```

### Settings
The [docker-compoe.yml](https://github.com/luna-nightbyte/ML-process/blob/main/docker-compose.yml) file contains os enviroments that is used inside all of the containers to run each app. 
Edit these to change settings when you run any application:
```
version: '3.8'

x-defaults: &default-settings
  environment:
    # Application settings:
      # ----APP NAME---- 
      # [ detection | ai_label | continuous | train | frame_insert ]
    - APP_NAME=frame_insert

      # --General--
    - SESSION_NAME=test # Any
    - MODEL_PATH=./models/yolo/model.pt # Must be inside 'models/yolo' folder.
    - THRESHOLD=0.5 #  Min: 0.0, Max: 1.0
    - CONSECUTIVE=3 # Usually 2-5

      # --Input--
      # Can be an URL, input file, or '0' for webcam on ubuntu
    - INPUT_DIR=input/INPUT_FOLDER # Must be inside 'input' folder.

      # --Output--
    - OUTPUT_SIZE=128,128 # I.e: 512,512
    - PADDING=50 # Optional padding to extract extra area from the image (As of now this is not implamented properly. But adding any value here will save a image of the detection in the desired output size)
    - SHOW_BOUNDING_BOX=false # Option to draw bounding box on the output frames
    - CSV_FILE_PATH=output/file.csv

      # --TRAINING ONLY--
    - EPOCHS=150 # 100 - 500 ish ish
    - BATCH=4 # 4, 8 , 32, 64, 124 and so on. Higher number require more GPU Vram / Ram

      # --FILE SERVING ONLY-- (Tip: see https://github.com/luna-nightbyte/ML-process/tree/main/golang#serve-video-folder)
    - SERVER_USER=${FILE_SERVER_USER}
    - SERVER_PASS=${FILE_SERVER_PASS}
    
    - FILE_SERVER_PASS=${password}

```
## Original author
- **Luna** [GitHub](https://github.com/luna-nightbyte)

