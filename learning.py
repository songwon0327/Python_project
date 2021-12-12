import numpy as np
from sklearn.linear_model import *
from sklearn.metrics import mean_squared_error
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

df = pd.read_csv("KboRankingFor20years.csv", encoding='cp949')
df['Team']= df['Team'].replace(['SK','넥센','kt','현대'],['SSG','키움','KT','현대(2008년 해체)'])

X = np.array(df.iloc[:,[1,2]])
y = df['Winning rate'] 
Rr = Ridge(alpha=1) 
Rr.fit(X, y)

train_y = Rr.predict(X)
train_loss = mean_squared_error(y, train_y)
print('train loss; ', train_loss)


test_X = np.array(df.iloc[:,[1,2]])
pred_y = Rr.predict(test_X)
test_y = df['Winning rate'] 

test_loss = mean_squared_error(test_y, pred_y)

print('test loss; ', test_loss)

plt.scatter(test_y, pred_y)
plt.plot([0,np.max(pred_y)],[0,np.max(pred_y)], color='red')

r2 = r2_score(test_y, pred_y)
print(r2)