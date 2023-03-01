import xml.etree.ElementTree as ET
import glob
import os
import json

#defining a variable
def xml_to_yolo_bbox(bbox, w, h):
    # xmin, ymin, xmax, ymax
    x_center = ((bbox[2] + bbox[0]) / 2) / w
    y_center = ((bbox[3] + bbox[1]) / 2) / h
    width = (bbox[2] - bbox[0]) / w
    height = (bbox[3] - bbox[1]) / h
    return [x_center, y_center, width, height]

#defining a variable
def yolo_to_xml_bbox(bbox, w, h):
    # x_center, y_center width heigth
    w_half_len = (bbox[2] * w) / 2
    h_half_len = (bbox[3] * h) / 2
    xmin = int((bbox[0] * w) - w_half_len)
    ymin = int((bbox[1] * h) - h_half_len)
    xmax = int((bbox[0] * w) + w_half_len)
    ymax = int((bbox[1] * h) + h_half_len)
    return [xmin, ymin, xmax, ymax]

#setting the input and output directory
classes = []
input_dir = "annotations/"
output_dir = "labels/"
image_dir = "images/"
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

#identifying all the xml files in the annotations folder (input directory)    
files = glob.glob(os.path.join(input_dir, '*.xml'))

#loop for all the files in the input folder
for fil in files:
    basename = os.path.basename(fil)
    filename = os.path.splitext(basename)[0]
    if not os.path.exists(os.path.join(image_dir, f"{filename}.jpg")):
        print(f"{filename} image does not exist!")
        continue

    result = []
    
    tree = ET.parse(fil)
    root = tree.getroot()
    width = int(root.find("size").find("width").text)
    height = int(root.find("size").find("height").text)
    
    for obj in root.findall('object'):
        label = obj.find("name").text
        #check for new classes to be appended in the list
        if label not in classes:
            classes.append(label)
        index = classes.index(label)
        pil_bbox = [int(x.text) for x in obj.find("bndbox")]
        yolo_bbox = xml_to_yolo_bbox(pil_bbox, width, height)
        #conversion of the data into string format
        bbox_string = " ".join([str(x) for x in yolo_bbox])
        result.append(f"{index} {bbox_string}")
        
    if result:
        #generation f YOLO text file for each of the xml documents
        with open(os.path.join(output_dir, f"{filename}.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(result))
            
#generation of the class names in a text file for further reference
with open ('classes.txt', 'w', encoding= 'utf8') as f:
    f.write(json.dumps(classes))