import json
from shutil import copyfile
import glob
import os

# testImageSet = os.listdir('test')
# print(testImageSet)

testDataResult = []


def copyTestfile(image, name):
    if not os.path.exists('test/' + name):
        os.makedirs('test/' + name)

    denst = str(image).split('/', -1)
    denstpath = denst[0] + '/' + name + '/' + denst[1]
    # print(image, denstpath)
    copyfile(image, denstpath)


with open('HomeResult.json') as json_file:
    data = json.load(json_file)
# print(data['testDataResult'])
for x in data['testDataResult']:
    # print(x['image'], len(x['result']))
    if len(x['result']) == 1:
        for y in x['result']:
            # print(y['name'])
            if y['name'] != 'Unknown':
                copyTestfile(x['image'], y['name'])  # len(x['result']),
    elif len(x['result']) > 1:
        floderName = ''
        for y in x['result']:
            # print(y['name'])'
            if y['name'] != 'Unknown':
                floderName = floderName + y['name'] + '_'
        # print(x['image'], ' = ' , len(x['result']), ' --> ', floderName)
        copyTestfile(x['image'], floderName[:-1])
