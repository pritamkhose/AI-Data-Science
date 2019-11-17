# Run - python 11LR.py

# https://stackoverflow.com/questions/9622163/save-plot-to-image-file-instead-of-displaying-it-using-matplotlib

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns

USAhousing = pd.read_csv('USA_Housing.csv')

# print(USAhousing.head())

# print(USAhousing.info())

# print(USAhousing.describe())

# print(USAhousing.columns)

pp = PdfPages('test.pdf')

sns.pairplot(USAhousing)
plt.title('USAhousing Pair Plot')
# plt.show()
plt.savefig('snspairplot.png')
pp.savefig()
plt.close()

sns.distplot(USAhousing['Price'])
plt.title('USAhousing Price Dist Plot')
# plt.show()
plt.savefig('snsdistplot.png')
pp.savefig()
plt.close()

sns.heatmap(USAhousing.corr())
plt.title('USAhousing heatmap')
# plt.show()
plt.savefig('snsheatmap.png')
pp.savefig()
plt.close()

# Training a Linear Regression Model
X = USAhousing[['Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms',
               'Avg. Area Number of Bedrooms', 'Area Population']]
y = USAhousing['Price']
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=101)

from sklearn.linear_model import LinearRegression
lm = LinearRegression()
lm.fit(X_train,y_train)

# Model Evaluation
print(lm.intercept_)
coeff_df = pd.DataFrame(lm.coef_,X.columns,columns=['Coefficient'])
print(coeff_df)

predictions = lm.predict(X_test)

plt.scatter(y_test,predictions)
plt.title('scatter y_test predictions')
# plt.show()
plt.savefig('predictions.png')
pp.savefig()
plt.close()

sns.distplot((y_test-predictions),bins=50);
plt.title('distplot predictions')
# plt.show()
plt.savefig('predictionsdistplot.png')
pp.savefig()
plt.close()

from sklearn import metrics
print('MAE:', metrics.mean_absolute_error(y_test, predictions))
print('MSE:', metrics.mean_squared_error(y_test, predictions))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, predictions)))

pp.close()