"""
  ____  _ _       _
  / __ \| (_)     (_)
 | |  | | |___   ___  __ _
 | |  | | | \ \ / / |/ _` |
 | |__| | | |\ V /| | (_| |
  \____/|_|_| \_/ |_|\__,_|

"""

import os
from PIL import Image
import piexif
import re
import sys


def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


def modifyexif(filename, data, new_file):
    """
    This function instert data into "Software" section of EXIF metadata of a given image
    :param filename: the name of the image to modify
    :param data: the data to insert into the image
    :param new_file: the path of the new image
    :return:
    """
    im = Image.open(filename)
    exif_dict = piexif.load(im.info["exif"])
    # process im and exif_dict...
    exif_dict["0th"][305] = data
    exif_bytes = piexif.dump(exif_dict)
    im.save(new_file, "jpeg", exif=exif_bytes)

def create_chunk_stream(path):
    """
    This function merge all the block and creates a bytestream structured as follows:
    sizeof(chunk1)-->chunck1-->sizeof(chunk2)-->chunk2-->sizeof(chunk3)-->chunk3...
    :param path: the path of the directory that contains the chunks
    :return: the chunk stream
    """
    content = []
    ord_list = os.listdir(path)
    ord_list.sort(key=natural_keys) #sort the chunck files
    print(ord_list)
    for filename in ord_list:
        with open(os.path.join(path, filename), 'r+b') as f:  # open in readonly mode
            content += [bytes([os.path.getsize(os.path.join(path, filename))])+f.read()]
            #print(os.path.getsize(os.path.join(path, filename)),os.path.join(path, filename))
    return b''.join(content)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    chunks_path = sys.argv[1]
    original_image_path = sys.argv[2]
    new_image_path = sys.argv[3]
    chunks = create_chunk_stream(chunks_path)
    modifyexif(original_image_path, chunks, new_image_path)

