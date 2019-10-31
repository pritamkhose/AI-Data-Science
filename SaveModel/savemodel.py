# https://www.geeksforgeeks.org/saving-a-machine-learning-model/

from sklearn.neighbors import KNeighborsClassifier as KNN
import numpy as np
from sklearn.model_selection import train_test_split

# Load dataset
from sklearn.datasets import load_iris
iris = load_iris()
X = iris.data
y = iris.target

# Split dataset into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,random_state=2018)

# import KNeighborsClassifier model
knn = KNN(n_neighbors=3)

# Train model
knn.fit(X_train, y_train)

print('------------ knn predictions ------------')
print(knn.predict(X_test))

import pickle 
# Save the trained model as a pickle string. 
saved_model = pickle.dumps(knn) 
  
# Load the pickled model 
knn_from_pickle = pickle.loads(saved_model) 
print('------------Use the loaded pickled model to make predictions ------------')
print(knn_from_pickle.predict(X_test))


# pip install joblib
# from sklearn.externals import joblib 
import joblib

# Save the model as a pickle in a file 
#joblib.dump(knn_from_pickle, './SaveModel/knn_model.pkl') 

# Load the model from the file 
knn_from_joblib = joblib.load('./SaveModel/knn_model.pkl') 

# Use the loaded model to make predictions 
knn_from_joblib.predict(X_test) 

print('------------ Pickled model as a file using joblib to make predictions ------------')
print(knn_from_joblib.predict(X_test))

# https://youtu.be/KfnhNlD8WZI