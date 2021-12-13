import numpy as np
import pandas as pd
from sklearn.linear_model import *
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error, f1_score, accuracy_score, r2_score, confusion_matrix

df = pd.read_csv("KboRankingFor20years.csv", encoding='cp949')
df['Team']= df['Team'].replace(['SK','넥센','kt','현대'],['SSG','키움','KT','현대(2008년 해체)'])
HW = df[df['Team'].str.contains('한화')]

X1 = np.array(HW.iloc[:,[2]])
y1 = HW['Winning rate'] 
Rr = Ridge(alpha=1) 
Rr.fit(X, y)

train_y = Rr.predict(X)
train_loss = mean_squared_error(y, train_y)
print('train loss; ', train_loss)


test_X1 = np.array(HW.iloc[:,[2]])
pred_y = Rr.predict(test_X)
test_y1 = HW['Winning rate'] 

test_loss = mean_squared_error(test_y, pred_y)

print('test loss; ', test_loss)

plt.scatter(test_y, pred_y)
plt.plot([0,np.max(pred_y)],[0,np.max(pred_y)], color='red')

r2 = r2_score(test_y, pred_y)
print(r2)
#--------------------------------------
train_df = HW[HW.Year <= 2011]
test_df = HW[HW.Year > 2011]

test_X2 = np.array(test_df.iloc[:,[2]])
test_y2 = test_df['Winning rate'] 

X2 = np.array(train_df.iloc[:,[2]])
y2 = train_df['Winning rate'] 

class_y = [1 if i > HW['Winning rate'].median() else 0 for i in y2]
test_class_y = [1 if i > HW['Winning rate'].median() else 0 for i in test_y2]
print(test_class_y)

clf = LogisticRegression(random_state=0).fit(X2, class_y)

predicted_y = clf.predict(test_X2)
print(predicted_y)

confusion_matrix = confusion_matrix(test_class_y, predicted_y)
print(confusion_matrix)

print(f1_score(test_class_y, predicted_y))
print(accuracy_score(test_class_y, predicted_y))