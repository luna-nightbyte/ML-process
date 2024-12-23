import os
import shutil
import random
import argparse

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

    print("Dataset successfully split into training and validation sets.")

# Example usage  # Change this to your dataset path
# create_dataset_structure()
