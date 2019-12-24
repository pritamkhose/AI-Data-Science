import glob
import os

trainImageData = []
trainDataFolders = os.listdir('train')
for x in trainDataFolders:
    fileList = os.listdir("train/"+x)
    for y in fileList:
        trainImageData.append({'name' : x, 'image': 'train/' + x + '/' + y})
# print(trainImageData)


import face_recognition
import numpy as np
import json

def trainDataImgFacRec (image): 
    print('Trainig Model for FacRec Image - ' + image) 
    # Load a sample picture and learn how to recognize it.
    a_image = face_recognition.load_image_file(image)
    return face_recognition.face_encodings(a_image)[0]

# Create arrays of known face encodings and their names
known_face_names = []
known_face_encodings = []


# saving model
model_directory = 'model'
model_face_encodings = '%s/model_face_encodings.pkl' % model_directory
model_known_face_names = '%s/known_face_names.pkl' % model_directory
import joblib

if not os.path.exists(model_directory):
    os.makedirs(model_directory)
    # Load a sample picture and learn how to recognize it.
    for x in trainImageData:
        known_face_names.append(x['name'])
        known_face_encodings.append(trainDataImgFacRec(x['image']))
    print('Traning Completed - ', len(known_face_encodings), 'images.')

    # Save Model
    joblib.dump(known_face_encodings, model_face_encodings)
    joblib.dump(known_face_names, model_known_face_names)
        
else:
    known_face_names = joblib.load(model_known_face_names)
    known_face_encodings = joblib.load(model_face_encodings)
    print('Load Traing Model - ', len(known_face_encodings), 'images.')

testDataResult = []
def testDataImgFacRec (img): 
    # Load an image with an unknown face
    unknown_image = face_recognition.load_image_file(img)

    # Find all the faces and face encodings in the unknown image
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

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
    
    testDataResult.append({ 'id': len(testDataResult), 'image': img, 'result' : resultArr})
    with open('HomeResultTemp.json', 'w') as f:
        f.write(json.dumps(testDataResult))
   
# showtime
testImageSet = os.listdir('test')
# print(testDataImgFacRec('test/22.jpg'))
testDataResult = []
for x in testImageSet:
    print( 'Running FacRec on Image - ' + 'test/' +x)
    testDataImgFacRec('test/' +x)

resultSaved = {'trainData': trainImageData, 'testImageSet': testImageSet, 'testDataResult': testDataResult}

with open('HomeResult.json', 'w') as f:
    f.write(json.dumps(resultSaved))
    f.close()
