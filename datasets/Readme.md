# ultralytics_to_labelimg.py
# Usage 
### Folder setup
```
ML-process
└── datasets
    ├── annotations
    │   ├── labelImg
    │   │   └── doggycat
    │   │       ├── images
    │   │       │   ├── garden_1.png
    │   │       │   ├── garden_2.png
    │   │       │   ├── garden_3.png
    │   │       │   ├── garden_4.png
    │   │       │   └── garden_5.png
    │   │       └── labels
    │   │           ├── garden_1.xml
    │   │           ├── garden_2.xml
    │   │           ├── garden_3.xml
    │   │           ├── garden_4.xml
    │   │           └── garden_5.xml
    │   └── ultralytics
    └── train
```
### Example 

#### command
```
user@host:/ML-process/datasets$ python3 extra/labelimg_to_ultralytics.py doggycat 'cat,dog'
```
#### output

```
Opening annotations/labelImg/doggycat/labels/garden_1_.xml
Found cat
Opening annotations/labelImg/doggycat/labels/garden_2_.xml
Found dog
Opening annotations/labelImg/doggycat/labels/garden_3_.xml
Found cat

Opening annotations/labelImg/doggycat/labels/garden_4.xml
No valid objects found in annotations/labelImg/test/labels/garden_4.xml

Opening annotations/labelImg/doggycat/labels/garden_5.xml
Not verified!

...........
Processed 5 images and annotations.
Dataset saved to annotations/ultralytics/doggycat
Copying dataset into train folders..
Dataset successfully split into training and validation sets.
```

Results:
```
ai_processing
└── datasets
    ├── annotations
    │   ├── labelImg
    │   │   └── doggycat
    │   │       ├── images
    │   │       │   ├── garden_1.png
    │   │       │   ├── garden_2.png
    │   │       │   ├── garden_3.png
    │   │       │   ├── garden_4.png
    │   │       │   └── garden_5.png
    │   │       └── labels
    │   │           ├── garden_1.xml
    │   │           ├── garden_2.xml
    │   │           ├── garden_3.xml
    │   │           ├── garden_4.xml
    │   │           └── garden_5.xml
    │   └── ultralytics
    │       └── doggycat
    │           ├── images
    │           │   ├── garden_1_output.png
    │           │   ├── garden_2_output.png
    │           │   └── garden_3_output.png
    │           └── labels
    │               ├── garden_1_output.txt
    │               ├── garden_2_output.txt
    │               └── garden_3_output.txt
    └── train
        └── doggycat
            └── train
            │   ├── images
            │   │   └── garden_1_output.png
            │   │   └── garden_3_output.png
            │   └── labels
            │       └── garden_1_output.txt
            │       └── garden_3_output.txt
            └── val
                ├── images
                │   └── garden_2_output.png
                └── labels
                    └── garden_2_output.txt
```
