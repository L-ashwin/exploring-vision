import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

def get_object_csv_from_xmls(DIR):
    """
    parse all xml files from given directory return dataframe with a row for each object instance.
    
    xml structure
    root:
        filename
        size
            width
            height
        object
            name
            bndbox
                xmin
                xmax
                ymin
                ymax
    
    returns: dataframe
    """
    annotations = []
    for xml_path in glob.glob(os.path.join(DIR, '*.xml')):
        root = ET.parse(xml_path)

        img_dict = {
            'imgname' : root.find('filename').text,
            #'imgpath' : root.find('path').text, uncomment if 'path' present or modify as per need
            'width'   : root.find('size/width').text,
            'height'  : root.find('size/height').text
        }

        objects  = []
        for obj in root.findall('object'):
            obj_details = {
                'class' : obj.find('name').text, 
                'xmin'  : obj.find('bndbox/xmin').text,
                'xmax'  : obj.find('bndbox/xmax').text,
                'ymin'  : obj.find('bndbox/ymin').text,
                'ymax'  : obj.find('bndbox/ymax').text,
            }
            objects.append(obj_details)
        
        anno_per_img = [{**img_dict, **obj_dict} for obj_dict in objects]
        annotations.extend(anno_per_img)
        
    return pd.DataFrame(annotations)