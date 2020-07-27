""" utilities
"""
import os
import json
from shutil import copyfile

def read_json(file_path):
    """ read a file as a string
    """
    assert os.path.isfile(file_path)
    with open(file_path) as file_obj:
        json_dct = json.load(file_obj)
    return json_dct


def write_json(json_dct, file_path):
    """ write a string to a file
    """
    copyfile(file_path, '_'.join([file_path,'backup']))
    with open(file_path, 'w') as file_obj:
        json.dump(json_dct, file_obj, ensure_ascii=False, indent=4)
        
