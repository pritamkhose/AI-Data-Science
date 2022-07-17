#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 18:15:39 2022

@author: Pritam

pip install PyPDF2

https://stackoverflow.com/questions/61885643/how-to-store-all-the-tables-from-pdf-file-to-excel-sheet-using-python

https://www.geeksforgeeks.org/working-with-pdf-files-in-python/

"""

# importing required modules
import PyPDF2
import tabula
from tabula import read_pdf
import pandas as pd 
from xlwt import Workbook 
 
# # creating a pdf file object
# pdfFileObj = open('SBI.pdf', 'rb')
 
# # creating a pdf reader object
# pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
 
# # printing number of pages in pdf file
# print(pdfReader.numPages)
 
# # creating a page object
# pageObj = pdfReader.getPage(0)
 
# # extracting text from page
# print(pageObj.extractText())
 
# # closing the pdf file object
# pdfFileObj.close()

data = []
#LAB is my pdf file
x = tabula.read_pdf("SBI.pdf", pages='all', multiple_tables=True)
for i in x:    #x values in list []
    print("printing all the table from the sheet", i)
    df = pd.DataFrame(i)
    data.append(df);
    
result = pd.concat(data)

result.to_excel('tables.xlsx', header=True, index = True)