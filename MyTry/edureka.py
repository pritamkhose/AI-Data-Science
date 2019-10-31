from sklearn import svm
from sklearn import datasets

iris = datasets.load_iris()
# print(type(iris))
# print(iris.data)
# print(iris.feature_names)
# print(iris.target)
# print(iris.target_names)

x = iris.data[:,2]
y = iris.target


from sklearn.model_selection  import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=4)

model = svm.SVC(kernel='linear')
model.fit(x_train,y_train)
y_predict = model.predict(x_train)

# print(model.score(x_test, y_test))
print(model.score(y_test, y_predict))

