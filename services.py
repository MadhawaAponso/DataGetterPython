import xml.etree.ElementTree as ET
import os

# GET FILE NAMES
def get_file_names(path):
    if os.path.isdir(path):
        files = os.listdir(path)
        return files
    else:
        print("Error: The provided path is not a directory.")
        return []

# CHECHIKNG WHETHER THERE ARE REPEATING TAGES UNDER A TAG(ARE THERE REPEATING CHILDS UNDER A PARENT)
def has_repeated_immediate_child_tags(root):
    seen_tags = set() 
    for child in root:
        tag_name = child.tag
        if tag_name in seen_tags:
            return True  
        seen_tags.add(tag_name)
    return False  