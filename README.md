# ML (Model learning) Processing

This is a project created to automate some tasks for YOLO object detection models. 
Run a docker app on a video and generate dataset for docker training app. Or run object detection on input folder/webcam/external camera.

_Make sure to checkout [Requirements](https://github.com/luna-nightbyte/ML-process/tree/main?tab=readme-ov-file#requirements)_
## Usage
Simply pull the latest docker [image](https://hub.docker.com/r/lunanightbyte/ml-process/tags?name=latest) from the hub and run with the [compose file](https://github.com/luna-nightbyte/ML-process/blob/main/docker-compose.yml) from this repo.
### Training
Remember to modify [dataset.yaml](https://github.com/luna-nightbyte/ML-process/blob/main/local/dataset.yaml) for your dataset/Session name. 


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

__Experminental__

Optional during object detection to extract the detected object in a spesific frame size. ~Add some value to `PADDING=` In the `docker-compose.yml` file to enable extraction~ Set EXTRACT_BOX=true to enable object exctraction and set your desired output size with `OUTPUT_SIZE=`. The output size can be larger and smaller than the detected object. The frame will be resized while keeping the aspect ratio.
`PADDING=` is intended to be the amount of extra padding around the detected object to extract. But this is not implemented yet. 

This extracted image can then be re-inserted back into the original image using the x.y position saved in a csv file. 

__Docker alternative__
```bash
user@host:/$ docker pull lunanightbyte/ml-process:latest
```

### Demo
<details>
<summary>
Docker compose</summary>

```bash
user@host:/$ git clone https://github.com/luna-nightbyte/ML-process
user@host:/$ cd ./ML-process
user@host:/ML-process$ docker compose up ML-process

[+] Running 1/0
 ✔ Container ml-processor  Recreated                                                                                                                                                                                                                                                                                               0.0s 
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
ml-processor  | Creating new Ultralytics Settings v0.0.6 file ✅ 
ml-processor  | View Ultralytics Settings with 'yolo settings' or at '/root/.config/Ultralytics/settings.json'
ml-processor  | Update Settings with 'yolo settings key=value', i.e. 'yolo settings runs_dir=path/to/dir'. For help see https://docs.ultralytics.com/quickstart/#ultralytics-settings.
ml-processor  | Processing: ./data/input/demo/171044-844787782_tiny.mp4
ml-processor  | Loading model
ml-processor  | GPU Name: NVIDIA GeForce GTX 1660 Ti
ml-processor  | 
ml-processor  | Loaded to GPU!
ml-processor  | Recording saved: ./data/output/demo/171044-844787782_tiny.mp4
ml-processor  | Recording saved: ./data/output/demo/E_171044-844787782_tiny.mp4
ml-processor  | Processing: ./data/input/demo/girl-1867092_1280.jpg
ml-processor  | Saving image to ./data/output/demo/girl-1867092_1280.jpg
ml-processor  | Saving image to ./data/output/demo/girl-1867092_1280.jpg
ml-processor  | Processing: ./data/input/demo/202718-918779955_medium.mp4
ml-processor  | Recording saved: ./data/output/demo/202718-918779955_medium.mp4
ml-processor  | Recording saved: ./data/output/demo/E_202718-918779955_medium.mp4
ml-processor  | Processing: ./data/input/demo/man-3803551_1280.jpg
ml-processor  | Saving image to ./data/output/demo/man-3803551_1280.jpg
ml-processor  | Saving image to ./data/output/demo/man-3803551_1280.jpg
ml-processor  | Processing: ./data/input/demo/171044-844787782_tiny.mp4
ml-processor  | Processing: ./data/input/demo/girl-1867092_1280.jpg
ml-processor  | Processing: ./data/input/demo/202718-918779955_medium.mp4
ml-processor  | Processing: ./data/input/demo/man-3803551_1280.jpg
100%|██████████| 755k/755k [00:00<00:00, 10.3MB/s]
train: Scanning /usr/src/app/datasets/train/demo/train/labels... 2327 images, 0 backgrounds, 0 corrupt: 100%|██████████| 2327/2327 [00:00<00:00, 3589.75it/s]
val: Scanning /usr/src/app/datasets/train/demo/val/labels... 1571 images, 0 backgrounds, 0 corrupt:     100%|██████████| 1571/1571 [00:00<00:00, 2951.12it/s]
        1/2      3.71G     0.4086     0.7891     0.8887          9        640:                          100%|██████████| 146/146 [00:35<00:00,  4.17it/s]
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95):               100%|██████████| 50/50 [00:05<00:00,  8.70it/s]
        2/2      3.73G     0.3184     0.3344     0.8527         15        640:                          100%|██████████| 146/146 [00:34<00:00,  4.19it/s]
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95):               100%|██████████| 50/50 [00:05<00:00,  9.28it/s]
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95):               100%|██████████| 50/50 [00:05<00:00,  9.17it/s]

```
</details>

<details>
<summary>
output files</summary>
  
```
├── datasets
│   ├── annotations
│   │   ├── labelImg
│   │   │   └── demo  [4760 entries exceeds filelimit, not opening dir]
│   │   └── ultralytics
│   │       └── demo
│   │           ├── images  [2380 entries exceeds filelimit, not opening dir]
│   │           └── labels  [2380 entries exceeds filelimit, not opening dir]
│   └── train
│       └── demo
│           ├── train
│           │   ├── images  [2327 entries exceeds filelimit, not opening dir]
│           │   ├── labels  [2327 entries exceeds filelimit, not opening dir]
│           │   └── labels.cache
│           └── val
│               ├── images  [1571 entries exceeds filelimit, not opening dir]
│               ├── labels  [1571 entries exceeds filelimit, not opening dir]
│               └── labels.cache
├── demo
│   ├── 171044-844787782_tiny.mp4
│   ├── 202718-918779955_medium.mp4
│   ├── girl-1867092_1280.jpg
│   └── man-3803551_1280.jpg
├── local
│   ├── demo.pt
│   ├── runs
│   │   └── detect
│   │       └── train
│   │           ├── args.yaml
│   │           ├── confusion_matrix_normalized.png
│   │           ├── confusion_matrix.png
│   │           ├── F1_curve.png
│   │           ├── labels_correlogram.jpg
│   │           ├── labels.jpg
│   │           ├── P_curve.png
│   │           ├── PR_curve.png
│   │           ├── R_curve.png
│   │           ├── results.csv
│   │           ├── results.png
│   │           ├── train_batch0.jpg
│   │           ├── train_batch1.jpg
│   │           ├── train_batch2.jpg
│   │           ├── val_batch0_labels.jpg
│   │           ├── val_batch0_pred.jpg
│   │           ├── val_batch1_labels.jpg
│   │           ├── val_batch1_pred.jpg
│   │           ├── val_batch2_labels.jpg
│   │           ├── val_batch2_pred.jpg
│   │           └── weights
│   │               ├── best.pt
│   │               └── last.pt
├── models
│   ├── classes.txt
│   └── yolo
│       └── model.pt
├── output
│   ├── demo
│   │   ├── 171044-844787782_tiny.mp4
│   │   ├── 202718-918779955_medium.mp4
│   │   ├── E_171044-844787782_tiny.mp4
│   │   ├── E_202718-918779955_medium.mp4
│   │   ├── E_girl-1867092_1280.jpg
│   │   ├── E_man-3803551_1280.jpg
│   │   ├── girl-1867092_1280.jpg
│   │   └── man-3803551_1280.jpg
│   └── file.csv
```
</details>


*Note: Using "demo" as app in docker-compose.yml is only ment as a very simple bare minimum demo so generate all files the various apps will generate.Annotations, Dataset, Trained model and so on. Always verify any auto generated annotations using a software like [LabelImg](https://github.com/HumanSignal/labelImg).*

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

