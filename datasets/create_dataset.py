import os
import xml.etree.ElementTree as ET
from pathlib import Path
import shutil
import datasets.extra.ultralytics_to_train_folders as to_train

def Create(dir, session_name, labels):
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
    #train_dir = os.path.join(output_dir, 'train')
    #val_dir = os.path.join(output_dir, 'val')



    def parse_xml(xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        verified = root.attrib.get('verified')
        if verified != 'yes':
            print("Not verified!")
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
            print("Found",name)
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
            print("\nOpening", os.path.join(annotations_input_dir, xml_file))
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
    print(f"Processed {len(image_list)} images and annotations.")
    print(f"Dataset saved to {output_dir}")
    print(f"Copying dataset into train folders..")
    to_train.create_dataset_structure(session_name, train_ratio=0.8)
