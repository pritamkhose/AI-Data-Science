# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 12:16:17 2021

@author: Pritam

pip install pytesseract
pip install Pillow

https://www.geeksforgeeks.org/python-convert-image-to-text-and-then-to-speech/
https://pypi.org/project/pytesseract/

tesseract installer
https://github.com/UB-Mannheim/tesseract/wiki

"""

import pytesseract
from PIL import Image
import os

# # If you don't have tesseract executable in your PATH, include the following:
# # pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

imgList = []
imgTextList = ''
for x in os.listdir():
    if x.endswith(".jpg"):
        # Prints only text file present in My Folder
        imgList.append(x)
        print(x)
        # Simple image to string
        img_txt = pytesseract.image_to_string(Image.open(x), lang = 'eng', config='--oem 3 --psm 6')
        # imgTextList.append({x,img_txt})
        imgTextList = imgTextList + x +"\n" + img_txt +"\n**---------------**\n" 

file1 = open("output.txt","w")
# \n is placed to indicate EOL (End of Line)
file1.write("AWS \n**---------------**\n\n")
file1.writelines(imgTextList)
file1.close() #to change file access modes

# x = '20170101055325.jpg'
# img_txt = pytesseract.image_to_string(Image.open(x), lang = 'eng', config='--oem 3 --psm 6')
# print(img_txt)
 