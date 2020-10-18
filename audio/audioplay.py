# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 17:19:54 2020

@author: Pritam

pip install pyttsx3
pip install PyPDF2
"""

import pyttsx3

speaker = pyttsx3.init()
speaker.say("Hi pritam")
speaker.runAndWait()

import PyPDF2
book = open('Clean_Code.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(book)
print(pdfReader.numPages)
pages = pdfReader.getPage(25)
text = pages.extractText()
print(text)
speaker.say(text)
speaker.runAndWait()