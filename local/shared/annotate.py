import xml.etree.ElementTree as ET
import os
import cv2

def save(image_name, image, bbox, label, full_output_path):
    
    if not os.path.exists(full_output_path.replace("/"+image_name,"")):
        os.makedirs(full_output_path.replace("/"+image_name,""))

    # Extract image name and extension
    # Save image
    image_save_path = full_output_path
    try:
        cv2.imwrite(image_save_path, image)
    except Exception as e:
        print(f"Failed to write {image_save_path} !\n{e}")
        return  
    try:
        # Create or load XML annotation
        xml_save_path = full_output_path.replace(os.path.splitext(image_name)[1],".xml")
        
        if os.path.exists(xml_save_path):
            tree = ET.parse(xml_save_path)
            root = tree.getroot()
        else:
            annotation = ET.Element("annotation")
            
            folder = ET.SubElement(annotation, "folder")
            folder.text = full_output_path.replace("/"+image_name,"")
            
            filename = ET.SubElement(annotation, "filename")
            filename.text = image_name
            
            path = ET.SubElement(annotation, "path")
            path.text = image_save_path
            
            source = ET.SubElement(annotation, "source")
            database = ET.SubElement(source, "database")
            database.text = "Unknown"
            
            size = ET.SubElement(annotation, "size")
            width = ET.SubElement(size, "width")
            height = ET.SubElement(size, "height")
            depth = ET.SubElement(size, "depth")
            
            height.text = str(image.shape[0])
            width.text = str(image.shape[1])
            depth.text = str(image.shape[2])
            
            segmented = ET.SubElement(annotation, "segmented")
            segmented.text = "0"
            
            root = annotation
        
        # Add object annotation
        obj = ET.SubElement(root, "object")
        name = ET.SubElement(obj, "name")
        name.text = label
        pose = ET.SubElement(obj, "pose")
        pose.text = "Unspecified"
        
        truncated = ET.SubElement(obj, "truncated")
        truncated.text = "0"
        
        difficult = ET.SubElement(obj, "difficult")
        difficult.text = "0"
        
        bndbox = ET.SubElement(obj, "bndbox")
        xmin = ET.SubElement(bndbox, "xmin")
        ymin = ET.SubElement(bndbox, "ymin")
        xmax = ET.SubElement(bndbox, "xmax")
        ymax = ET.SubElement(bndbox, "ymax")
        
        xmin.text = str(bbox[0])
        ymin.text = str(bbox[1])
        xmax.text = str(bbox[2])
        ymax.text = str(bbox[3])
        
        # Write the updated tree back to the file
        tree = ET.ElementTree(root)
        try:
            tree.write(xml_save_path)
        except Exception as e:
            print("Error saving:",e)
    except:
        return
    
    return image_save_path, xml_save_path

