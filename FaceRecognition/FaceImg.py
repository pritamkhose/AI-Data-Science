# https://face-recognition.readthedocs.io/en/latest/face_recognition.html

import face_recognition
import json
import numpy as np

import urllib.request
import wget
import os
import random


def download_image(url):
    name = random.randrange(1,100)
    fullname = str(name)+".jpg"
    # urllib.request.urlretrieve(url,fullname)   
    # urllib.request.urlretrieve(url, "local-filename.jpg")
    wget.download('/tmp', url)
#download_image("http://site.meishij.net/r/58/25/3568808/a3568808_142682562777944.jpg")

try:
    # Load a picture and learn how to recognize it.
    face_image = face_recognition.load_image_file("outfit3.jpg")

    try:
        face_locations = face_recognition.face_locations(face_image)
        face_landmarks = face_recognition.face_landmarks(face_image)

        arr = np.array(face_image)
        print(json.dumps({
            'result': True,
            'img_width': arr.shape[0],
            'img_hight': arr.shape[1],
            'face_locations': face_locations,
            'face_landmarks': face_landmarks
        }))    
    except:
        print(json.dumps({
            'result': False,
            'error': 'Unable to process image file'
        }))
except:
    print(json.dumps({
        'result': False,
        'error': 'Invalid image file'
    }))
