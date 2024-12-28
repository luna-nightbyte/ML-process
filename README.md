# ML (Model learning) Processing

This is a project created to automate some tasks for YOLO object detection models. 
Run a docker app on a video and generate dataset for docker training app. Or run object detection on input folder/webcam/external camera.

_Make sure to checkout [Requirements](https://github.com/luna-nightbyte/ML-process/tree/main?tab=readme-ov-file#requirements)_
## Usage
Simply pull the latest docker [image](https://hub.docker.com/r/lunanightbyte/ml-process/tags?name=latest) from the hub and run with the [compose file](https://github.com/luna-nightbyte/ML-process/blob/main/docker-compose.yml) from this repo.
#### Training
Remember to modify [dataset.yaml](https://github.com/luna-nightbyte/ML-process/blob/main/local/dataset.yaml) for your dataset/Session name. 

#### General
Modify docker compose to use your desired application:
```docker-compose.yml
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
__Experminental__

Optional during object detection to extract the detected object in a spesific frame size. Add some value to `PADDING=` In the `docker-compose.yml` file to enable extraction, and set your desired output size with `OUTPUT_SIZE=`. The output size can be larger and smaller than the detected object. The frame will be resized while keeping the aspect ratio.
`PADDING=` is intended to be the amount of extra padding around the detected object to extract. But this is not implemented yet. 

This extracted image can then be re-inserted back into the original image using the x.y position saved in a csv file. 

__Docker alternative__
```bash
user@host:/$ docker pull lunanightbyte/ml-process:latest
```

__Bare minimum__
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
ml-processor  | Processing: ./data/input/demo/171044-844787782_tiny.mp4
ml-processor  | Loading model
ml-processor  | GPU Name: NVIDIA GeForce GTX 1660 Ti
ml-processor  | Loaded to GPU!
ml-processor  | Recording saved: ./data/output/demo/171044-844787782_tiny.mp4
ml-processor  | Recording saved: ./data/output/demo/E_171044-844787782_tiny.mp4
ml-processor  | Recording saved: ./data/output/demo/171044-844787782_tiny.mp4
ml-processor  | Recording saved: ./data/output/demo/E_171044-844787782_tiny.mp4
ml-processor  | Processing: ./data/input/demo/girl-1867092_1280.jpg
ml-processor  | Saving image to ./data/output/demo/girl-1867092_1280.jpg
ml-processor  | Saving image to ./data/output/demo/girl-1867092_1280.jpg
ml-processor  | Processing: ./data/input/demo/202718-918779955_medium.mp4
ml-processor  | Recording saved: ./data/output/demo/202718-918779955_medium.mp4
ml-processor  | Recording saved: ./data/output/demo/E_202718-918779955_medium.mp4
ml-processor  | Recording saved: ./data/output/demo/202718-918779955_medium.mp4
ml-processor  | Recording saved: ./data/output/demo/E_202718-918779955_medium.mp4
ml-processor  | Processing: ./data/input/demo/man-3803551_1280.jpg
ml-processor  | Saving image to ./data/output/demo/man-3803551_1280.jpg
ml-processor  | Saving image to ./data/output/demo/man-3803551_1280.jpg
ml-processor exited with code 0
```

*Note: Always verify any atuo generated annotations using a software like [LabelImg](https://github.com/HumanSignal/labelImg)*

### Settings
The [docker-compoe.yml](https://github.com/luna-nightbyte/ML-process/blob/main/docker-compose.yml) file contains os enviroments that is used inside all of the containers to run each app. 
Edit these to change settings when you run any application:
```docker-compose.yml
    # Application settings:
    - APP_NAME=demo   # [ detection | ai_label | continuous | train | frame_insert ]
    - SESSION_NAME=demo       # Any name to identify the session

    # Model and Threshold
    - MODEL_PATH=./models/yolo/model.pt  # Must be inside the 'models/yolo' folder.
    - THRESHOLD=0.5                      # Min: 0.0, Max: 1.0
    - CONSECUTIVE=3                      # Typically 2-5 for stability.

    # Input Settings
    - INPUT_DIR=input/demo       # Must be inside the 'input' folder.

    # Output Settings
    - OUTPUT_SIZE=128,128                # For example: 512,512
    - EXTRACT_BOX=true                   # true/false
    # - PADDING=                         # Optional. Extra padding for image extraction (not fully implemented yet).
    - SHOW_BOUNDING_BOX=false            # Draw bounding boxes on output frames (true/false).
    - CSV_FILE_PATH=output/file.csv      # Path to save the output CSV file.

    # Training-Specific Settings
    - EPOCHS=150                         
    - BATCH=4                            # Valid values: 4, 8, 32, 64, etc. Higher values require more GPU VRAM.
    - MODEL_IMG_SIZE=640
    
    # File Serving Settings
    - SERVER_USER=${FILE_SERVER_USER}    # Username for file server.
    - SERVER_PASS=${FILE_SERVER_PASS}    # Password for file server.
```

## Requirements
### Hardware
- __NVIDIA GPU__: You’ll need an NVIDIA GPU that supports CUDA. Most modern NVIDIA GPUs do, but it’s always a good idea to check the compatibility of your specific model against the CUDA-enabled GPU list.
- __Sufficient GPU Memory__: Deep learning models can be memory-intensive. Ensure your GPU has enough memory to accommodate the models you plan to train.
### Software
- __Operating System__: A compatible Linux distribution or Windows. This guide primarily focuses on Linux due to its widespread use in deep learning and development environments. Popular distributions include Ubuntu, CentOS, and Debian.
- __NVIDIA Drivers__: The latest NVIDIA drivers compatible with your GPU and intended CUDA version. These drivers are crucial for enabling the GPU to interface with the operating system and software.
- __Docker__: Ensure you have Docker installed. The version of Docker should be compatible with the NVIDIA Container Toolkit. For most users, the latest version of Docker is recommended.
Docker is required to run the containers. You need to install Docker on your machine, which includes Docker Engine and Docker Compose.
Checkout the [docker](https://github.com/luna-nightbyte/ML-process/tree/main/docker) folder for installation instructions.


## Original author
- **Luna** [GitHub](https://github.com/luna-nightbyte)

