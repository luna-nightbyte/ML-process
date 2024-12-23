import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import cv2
import argparse
# Define paths

#   input_dir = "./annotations/ultralytics/DATASET_NAME/labels_ultralytics"
#   output_dir = "./annotations/ultralytics/DATASET_NAME/labels_labelimg"
#   images_dir = "./annotations/ultralytics/DATASET_NAME/images"
#   class_names = ['class1', 'class2', 'class2']
parser = argparse.ArgumentParser(description="""Copies labelImg annotations into ultralytics annotations. I.e:
    Session = DoggyCat :
        annotations/ultralytics/DoggyCat -> annotations/labelImg/DoggyCat""")
parser.add_argument('session_name', type=str, help="Session name/folder name")
parser.add_argument('class_names', type=list[str], help="Class names. i.e:  [ 'cat', 'dog' ]")

# Extracting the arguments
args = parser.parse_args()
INPUT_DIR = "datasets/annotations/ultralytics/"+args.session_name
OUTPUT_DIR = "datasets/annotations/labelImg/"+args.session_name
# Extracting the arguments
args = parser.parse_args()
LABELS_DIR = f'{INPUT_DIR}/labels'
IMAGES_DIR = f'{INPUT_DIR}/images'
CLASS_NAMES = args.class_names

# Helper function to create XML structure
def create_xml_annotation(image_path, boxes, image_size):
    annotation = ET.Element('annotation')

    # Folder
    folder = ET.SubElement(annotation, 'folder')
    folder.text = os.path.basename(os.path.dirname(image_path))

    # Filename
    filename = ET.SubElement(annotation, 'filename')
    filename.text = os.path.basename(image_path)

    # Path
    path = ET.SubElement(annotation, 'path')
    path.text = image_path

    # Source
    source = ET.SubElement(annotation, 'source')
    database = ET.SubElement(source, 'database')
    database.text = 'Unknown'

    # Size
    size = ET.SubElement(annotation, 'size')
    width = ET.SubElement(size, 'width')
    width.text = str(image_size[0])
    height = ET.SubElement(size, 'height')
    height.text = str(image_size[1])
    depth = ET.SubElement(size, 'depth')
    depth.text = str(image_size[2])

    # Segmented
    segmented = ET.SubElement(annotation, 'segmented')
    segmented.text = '0'

    # Object
    for box in boxes:
        obj = ET.SubElement(annotation, 'object')
        name = ET.SubElement(obj, 'name')
        name.text = box['class_name']
        pose = ET.SubElement(obj, 'pose')
        pose.text = 'Unspecified'
        truncated = ET.SubElement(obj, 'truncated')
        truncated.text = '0'
        difficult = ET.SubElement(obj, 'difficult')
        difficult.text = '0'
        bndbox = ET.SubElement(obj, 'bndbox')
        xmin = ET.SubElement(bndbox, 'xmin')
        xmin.text = str(box['xmin'])
        ymin = ET.SubElement(bndbox, 'ymin')
        ymin.text = str(box['ymin'])
        xmax = ET.SubElement(bndbox, 'xmax')
        xmax.text = str(box['xmax'])
        ymax = ET.SubElement(bndbox, 'ymax')
        ymax.text = str(box['ymax'])

    return annotation

# Function to convert YOLO format to PASCAL VOC format
def yolo_to_pascal_voc(yolo_file, image_file, output_file, class_names):
    image = cv2.imread(image_file)
    h, w, c = image.shape
    boxes = []

    with open(yolo_file, 'r') as f:
        for line in f:
            class_id, x_center, y_center, width, height = map(float, line.strip().split())
            xmin = int((x_center - width / 2) * w)
            xmax = int((x_center + width / 2) * w)
            ymin = int((y_center - height / 2) * h)
            ymax = int((y_center + height / 2) * h)
            box = {
                'class_name': class_names[int(class_id)],
                'xmin': xmin,
                'ymin': ymin,
                'xmax': xmax,
                'ymax': ymax
            }
            boxes.append(box)

    annotation = create_xml_annotation(image_file, boxes, (w, h, c))
    with open(output_file, 'w') as f:
        f.write(minidom.parseString(ET.tostring(annotation)).toprettyxml(indent="    "))

# Main function to process all files
def main(input_dir, images_dir, output_dir,class_names):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for txt_file in os.listdir(input_dir):
        if txt_file.endswith('.txt'):
            base_name = os.path.splitext(txt_file)[0]
            image_file = os.path.join(images_dir, base_name + ".jpg")  # Assuming the image is a .jpg file
            yolo_file = os.path.join(input_dir, txt_file)
            output_file = os.path.join(output_dir, base_name + ".xml")
            yolo_to_pascal_voc(yolo_file, image_file, output_file, class_names)

if __name__ == "__main__":
    main(LABELS_DIR,  IMAGES_DIR, OUTPUT_DIR, CLASS_NAMES)
