import os
import random

def remove_unmatched_images(folder_path, extension_img='.jpg', extension_xml='.xml'):
    # Get list of all files in the directory
    files = os.listdir(folder_path)
    
    # Separate image files and xml files
    images = [f for f in files if f.endswith(extension_img)]
    xmls = [f for f in files if f.endswith(extension_xml)]
    
    # Strip extensions to get base filenames
    image_bases = {os.path.splitext(img)[0] for img in images}
    xml_bases = {os.path.splitext(xml)[0] for xml in xmls}
    
    # Find images without a corresponding XML file
    unmatched_images = image_bases - xml_bases
    
    # Calculate how many unmatched images to keep (10% of matched images)
    num_matched_images = len(image_bases.intersection(xml_bases))
    num_to_keep = max(1, int(0.1 * num_matched_images))
    
    # Convert set to list for random sampling
    unmatched_images_list = list(unmatched_images)
    
    # Randomly select images to keep
    images_to_keep = set(random.sample(unmatched_images_list, min(num_to_keep, len(unmatched_images_list))))
    
    # Images to delete
    images_to_delete = unmatched_images - images_to_keep
    
    # Deleting the unmatched images that are not in the keep set
    for image_base in images_to_delete:
        image_path = os.path.join(folder_path, image_base + extension_img)
        os.remove(image_path)
        print(f"Deleted {image_path}")

    print(f"Kept {len(images_to_keep)} unmatched images out of {len(unmatched_images)}")

# Example usage
folder_path = 'output/annotations/annotations_folder'  # Replace with your folder path
remove_unmatched_images(folder_path)
