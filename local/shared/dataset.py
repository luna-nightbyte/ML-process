import os
import shutil
import random

import xml.etree.ElementTree as ET
from pathlib import Path


def generate_dataset(dir, session_name, labels):
    # Extracting the arguments
     
    class_names = labels
    input_dir = f'{dir}/labelImg/{session_name}'
    output_dir = f'{dir}/ultralytics/{session_name}'

    annotations_output_dir = f'{output_dir}/labels'
    images_output_dir = f'{output_dir}/images'

    try:
        os.listdir(f'{input_dir}/labels')
        annotations_input_dir = f'{input_dir}/labels'
        images_input_dir = f'{input_dir}/images'
    except Exception as e:
        annotations_input_dir = f'{input_dir}'
        images_input_dir = f'{input_dir}'

    os.makedirs(f'{output_dir}/labels', exist_ok=True)
    os.makedirs(f'{output_dir}/images', exist_ok=True)
    
    def parse_xml(xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # verified = root.attrib.get('verified')
        # if verified != 'yes':
            #return None

        filename = root.find('filename').text
        size = root.find('size')
        width = int(size.find('width').text)
        height = int(size.find('height').text)

        objects = []
        save_annotation = False
        for obj in root.iter('object'):
            name = obj.find('name').text
            if name not in class_names:
                print(f"{name} not found in list of classes:\n{class_names}")
                continue
            
            class_id = class_names.index(name)
            bndbox = obj.find('bndbox')
            xmin = int(bndbox.find('xmin').text)
            ymin = int(bndbox.find('ymin').text)
            xmax = int(bndbox.find('xmax').text)
            ymax = int(bndbox.find('ymax').text)

            # Convert to YOLO format
            x_center = (xmin + xmax) / 2 / width
            y_center = (ymin + ymax) / 2 / height
            bbox_width = (xmax - xmin) / width
            bbox_height = (ymax - ymin) / height

            objects.append((class_id, x_center, y_center, bbox_width, bbox_height))

        return filename, objects

    # Process all XML files
    image_list = []
    for xml_file in os.listdir(annotations_input_dir):
        if xml_file.endswith('.xml'):
            
            result = parse_xml(os.path.join(annotations_input_dir, xml_file))
            if result:
                filename, objects = result
                if not objects:
                    print(f"No valid objects found in {os.path.join(annotations_input_dir, xml_file)}")
                    continue
                txt_file = os.path.join(annotations_output_dir, Path(filename).stem + '.txt')
                with open(txt_file, 'w') as f:
                    for obj in objects:
                        f.write(' '.join(map(str, obj)) + '\n')
                try:
                    shutil.copy(os.path.join(images_input_dir, filename), os.path.join(images_output_dir, filename))
                    image_list.append(filename)
                except Exception as e:
                    print(e)
    
    create_dataset_structure(session_name, train_ratio=0.8)
    
def create_dataset_structure(session_name,train_ratio=0.8):
    # Define the paths for the images and labels
    
    INPUT_DIR = f'./datasets/annotations/ultralytics/{session_name}'
    OUTPUT_DIR = f'./datasets/train/{session_name}'
    images_path = os.path.join(INPUT_DIR, 'images')
    labels_path = os.path.join(INPUT_DIR, 'labels')

    # Create train and validate folders for images and labels
    train_images_path = os.path.join(OUTPUT_DIR, 'train', 'images')
    train_labels_path = os.path.join(OUTPUT_DIR, 'train', 'labels')
    val_images_path = os.path.join(OUTPUT_DIR, 'val', 'images')
    val_labels_path = os.path.join(OUTPUT_DIR, 'val', 'labels')

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(train_images_path, exist_ok=True)
    os.makedirs(train_labels_path, exist_ok=True)
    os.makedirs(val_images_path, exist_ok=True)
    os.makedirs(val_labels_path, exist_ok=True)

    # Get list of all images and labels
    images = [f for f in os.listdir(images_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
    labels = [f for f in os.listdir(labels_path) if f.endswith('.txt')]

    # Ensure each image has a corresponding label
    images = [img for img in images if img.replace('.jpg', '.txt').replace('.jpeg', '.txt').replace('.png', '.txt') in labels]

    # Shuffle the images and split into train and validate sets
    random.shuffle(images)
    split_idx = int(len(images) * train_ratio)
    train_images = images[:split_idx]
    val_images = images[split_idx:]

    # Move files to respective folders
    for img in train_images:
        label = img.replace('.jpg', '.txt').replace('.jpeg', '.txt').replace('.png', '.txt')
        shutil.copy(os.path.join(images_path, img), os.path.join(train_images_path, img))
        shutil.copy(os.path.join(labels_path, label), os.path.join(train_labels_path, label))

    for img in val_images:
        label = img.replace('.jpg', '.txt').replace('.jpeg', '.txt').replace('.png', '.txt')
        shutil.copy(os.path.join(images_path, img), os.path.join(val_images_path, img))
        shutil.copy(os.path.join(labels_path, label), os.path.join(val_labels_path, label))
