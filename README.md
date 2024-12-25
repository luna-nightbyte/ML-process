# ML (Model learning) Processing

This is a project created to automate some tasks for YOLO object detection models. 
Run a docker app on a video and generate dataset for docker training app. Or run object detection on input folder/webcam/external camera. 

Probably possible to tweak to input a video stream from a local ip camera as well.

*Note: Always verify any atuo generated annotations using a software like [LabelImg](https://github.com/HumanSignal/labelImg)*

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
```bash
git clone https://github.com/luna-nightbyte/ML-process
cd ./ML-process
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
      # [ detection | ai_label | continuous | train ]
    - APP_NAME=train

      # --General--
    - SESSION_NAME=test # Any

    - MODEL_PATH=./models/yolo/model.pt # Must be inside 'models/yolo' folder.
    - THRESHOLD=0.5 #  Min: 0.0, Max: 1.0
    - CONSECUTIVE=3 # Usually 2-5
      # --Input--
      # Can be an URL, input file, or '0' for webcam on ubuntu
    - INPUT_DIR=input/test # Must be inside 'input' folder.

      # --TRAINING ONLY--
    - EPOCHS=150 # 100 - 500 ish ish
    - BATCH=4 # 4, 8 , 32, 64, 124 and so on. Higher number require more GPU Vram / Ram

      # --FILE SERVING ONLY-- (Tip: see https://github.com/luna-nightbyte/ML-process/tree/main/golang#serve-video-folder)
    - FILE_SERVER_USER=${username}
    - FILE_SERVER_PASS=${password}

```

### Starting an App
#### Training
Remember to modify [dataset.yaml](https://github.com/luna-nightbyte/ML-process/blob/main/local/dataset.yaml) for your dataset/Session name. 

#### General
Easiest to open up the folder with [Visual Studio Code](https://code.visualstudio.com/)  and work from there.

Simply open a terminal that is in the same folder as `docker-compose.yml`and run `docker-compose up ai`to start any of the applications. 

Newer docker versions uses `docker compose` without `-`in the command. 

The container should now be listed in [Docker Desktop](https://www.docker.com/products/docker-desktop/), and in the sidebar of Visual studio code. You can use either one to start and stop the containers in the future, and simply remove them if they cause issues starting up containers after editing `docker-compose.yml`.


## Original author
- **Luna** [GitHub](https://github.com/luna-nightbyte)

