# https://github.com/ageitgey/face_recognition
# https://beta.deepnote.com/project/dbfd3970-3b24-492d-a0a6-b93e113a1602#%2Fexample.ipynb
# https://github.com/ageitgey/face_recognition/tree/master/examples

# run by python3 FaceRecObamaBulk.py

# from IPython.display import display
# The program we will be finding faces on the example below
# pil_im = Image.open('two_people.jpg')
# display(pil_im)
# pil_im.show() 

# Learning from example

import face_recognition
import numpy as np
# Find faces in pictures
from PIL import Image, ImageDraw
# from IPython.display import display

# This is an example of running face recognition on a single image
# and drawing a box around each person that was identified.

def trainDataImgFacRec (img): 
    # Load a sample picture and learn how to recognize it.
    a_image = face_recognition.load_image_file(img)
    return face_recognition.face_encodings(a_image)[0]

trainData1 = { 'id': 1, 'name': 'Barack Obama', 'image': 'obama.jpg'}
trainData2 = { 'id': 2, 'name': 'Joe Biden', 'image': 'biden.jpg'}
trainData3 = { 'id': 3, 'name': 'Modi', 'image': 'modi.jpg'}

trainDataImg = []
trainDataImg.append(trainData1)
trainDataImg.append(trainData2)
trainDataImg.append(trainData3)


# Create arrays of known face encodings and their names
known_face_names = []
known_face_encodings = []

# # Load a sample picture and learn how to recognize it.
for x in trainDataImg:
    known_face_names.append(x['name'])
    known_face_encodings.append(trainDataImgFacRec(x['image']))


print('Learned encoding done for', len(known_face_encodings), 'images.')

testDataResult = []
showPreview = False # True

def testDataImgFacRec (img): 
    print('testDataImgFacRec Image - ' + img) 
    # Load an image with an unknown face
    unknown_image = face_recognition.load_image_file(img)

    # Find all the faces and face encodings in the unknown image
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    # Convert the image to a PIL-format image so that we can draw on top of it with the Pillow library
    # See http://pillow.readthedocs.io/ for more about PIL/Pillow
    pil_image = Image.fromarray(unknown_image)
    # Create a Pillow ImageDraw Draw instance to draw with
    draw = ImageDraw.Draw(pil_image)

    resultArr = []
    # Loop through each face found in the unknown image
    indexforloop = 0
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = 'Unknown'

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        resultArr.append({'name' : name, 'face_locations': face_locations[indexforloop] }) # 'face_encodings': face_encodings  
        indexforloop = indexforloop + 1

        if showPreview == True:
            # Draw a box around the face using the Pillow module
            draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

            # Draw a label with a name below the face
            text_width, text_height = draw.textsize(name)
            draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
            draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

    testDataResult.append({ 'id': len(testDataResult), 'image': img, 'result' : resultArr})
    
    if showPreview == True:
        # Remove the drawing library from memory as per the Pillow docs
        del draw

        # Display the resulting image
        # display(pil_image)
        pil_image.show() 

# showtime 
testDataImg = [
    'two_people.jpg',
    'modi_gr.jpg',
    'modi-obama.jpg',
    'outfit3.jpg'
]

for x in testDataImg:
  testDataImgFacRec(x)

# print(testDataResult)

import json
print(json.dumps(testDataResult))

resultSaved = {'trainData': trainDataImg, 'testDataResult': testDataResult}

# https://stackoverflow.com/questions/899103/writing-a-list-to-a-file-with-python

with open('result.json', 'w') as f:
    f.write(json.dumps(resultSaved))
    f.close()
    # for item in testDataResult:
    #     f.write("%s\n" % item)

    