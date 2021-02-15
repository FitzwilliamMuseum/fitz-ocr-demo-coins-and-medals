#!/usr/bin/python
## Split pdf files into pages
## Daniel Pett 11/2/2021
__author__ = 'portableant'
## Tested on Python 2.7.16
## Usage example
## python3 splitPdf.py -p . -f 1975_1989.pdf -d processed -n 1975_1989_processed -o ocr
## mac osx brew install poplar and echo 'export PATH="/usr/local/opt/qt/bin:$PATH"' >> ~/.zshrc

import argparse
import os
import sys
# pip3 install Pillow
from PIL import Image

# pip3 install pytesseract
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'


# pip3 install PyPDF2
from PyPDF2 import PdfFileWriter, PdfFileReader
# pip3 install pdf2image
from pdf2image import convert_from_path, pdfinfo_from_path
# pip3 install wand
#from wand.image import Image

parser = argparse.ArgumentParser(description='A script for splitting pdf files into pages')
parser.add_argument('-p', '--path', help='The path to the folder to process', required=True)
parser.add_argument('-f', '--file', help='The file to process', required=True)
parser.add_argument('-n', '--name', help='The new file name', required=True)
parser.add_argument('-d', '--destination', help='The processed folder', required=True)
parser.add_argument('-o', '--ocr', help='The ocr folder', required=True)

# Parse arguments

args = parser.parse_args()

path = args.path
print(path)

destination = os.path.join(path,args.destination)
print(destination)

ocrfolder = os.path.join(path,args.ocr)
print(ocrfolder)

pageName = os.path.join(destination,args.name)+'%s.pdf'
print(pageName)

fileName = os.path.join(path,args.file)
print(fileName)

if not os.path.exists(destination):
    os.makedirs(destination)

if not os.path.exists(ocrfolder):
    os.makedirs(ocrfolder)

if not os.path.exists('images'):
    os.makedirs('images')

inputpdf = PdfFileReader(open( fileName, "rb"))

for i in range(inputpdf.numPages):
    output = PdfFileWriter()
    output.addPage(inputpdf.getPage(i))
    with open(pageName % (i+1), "wb") as outputStream:
        output.write(outputStream)

print(destination)
for file in os.listdir(destination):
     print(file)
     filepath = os.path.join(destination,file)
     if file.endswith(".pdf"):
        print(pdfinfo_from_path(filepath)['Pages'])
        img = convert_from_path(filepath)
        imgName = os.path.splitext(file)[0]
        print(imgName)
        jpgName = os.path.join('./images/',imgName + '.jpg')
        for page in img:
          page.save(jpgName, 'JPEG')
          text = pytesseract.image_to_string(Image.open(jpgName), config='psm 4')
          ocrName = os.path.join('./ocr/',imgName + '.txt')
          print(text)
          with open(ocrName, mode = 'w') as f:
            f.write(text)
