# -*- coding: utf-8 -*-
"""EDA/FA_0928.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZGem3Zq5AJf7AlFKwdHR6rT8yxYUGLd4
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

"""### 가서 유동인구 칼럼 합쳤다고 가정"""

data = pd.read_csv('features_0804_2.csv', index_col=0)
data.head()

# Font
# !sudo apt-get install -y fonts-nanum
# !sudo fc-cache -fv
# !rm ~/.cache/matplotlib -rf

import matplotlib.pyplot as plt
plt.rc('font', family='NanumGothicCoding')
plt.rcParams['axes.unicode_minus'] =False

# 런타임 재시작

# numeric 변수만 추출해서 분포 확인
num_data = data.drop(columns=['branchnm', '동이름', '매출액추정(행정동)'])
num_data.hist(figsize=(20,20))

corr = num_data.corr()
plt.figure(figsize=(20,20))
sns.heatmap(corr, annot=True, cmap='Blues')

"""대부분이 정규분포가 아님 => MinMaxScaler 사용"""

# 필요한 변수만 추출
data = data.drop(['branchnm', '동이름', '매출액추정(행정동)', '매출건수추정(행정동)', 'Latitude', 'Longitude'], axis=1)

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
y = data['에코매장 유무']
X = data.drop('에코매장 유무', axis=1)

col_list = data.columns.tolist()
col_list.remove('에코매장 유무')
X[col_list] = scaler.fit_transform(X[col_list])

X.head()

import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor


# VIF 계산
def calculate_vif(df):
    vif = pd.DataFrame()
    vif["Variable"] = df.columns
    vif["VIF"] = [variance_inflation_factor(df.values, i) for i in range(df.shape[1])]
    return vif

vif_df = calculate_vif(data)


print(vif_df)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

from sklearn.linear_model import LassoCV
import numpy as np

# Fit the Lasso model
lasso = LassoCV(random_state=42).fit(X_train, y_train)
importance = np.abs(lasso.coef_)

# Print R-squared values
r_squared_train = lasso.score(X_train, y_train)
r_squared_test = lasso.score(X_test, y_test)
print(f"R-squared (train): {r_squared_train}")
print(f"R-squared (test): {r_squared_test}")

from sklearn.linear_model import LassoCV
import numpy as np

lasso = LassoCV(random_state=42).fit(X_train, y_train) #alpha설정 안 해도 됨!
importance = np.abs(lasso.coef_)

# 중요도가 0인 변수 제외
feature_columns = data.columns
feature_columns = [col for col in feature_columns if col != '에코매장 유무']
nonzero_importance = importance[importance > 0]
nonzero_features = np.array(feature_columns)[importance > 0]

# 중요도를 기준으로 내림차순 정렬
sorted_indices = np.argsort(nonzero_importance)[::-1]

plt.figure(figsize=(15, 6))
plt.bar(height=nonzero_importance[sorted_indices], x=nonzero_features[sorted_indices])
plt.title("Feature importances via coefficients - Lasso")
plt.xlabel("Features")
plt.ylabel("Absolute Coefficients")
plt.show()

from sklearn.linear_model import RidgeCV

ridge = RidgeCV().fit(X_train, y_train)
importance = np.abs(ridge.coef_)

# 중요도가 0인 변수 제외
nonzero_importance = importance[importance > 0]
nonzero_features = np.array(feature_columns)[importance > 0]

top_n = 10
sorted_indices = np.argsort(nonzero_importance)[::-1]

plt.figure(figsize=(24, 6))
plt.bar(height=nonzero_importance[sorted_indices][:top_n], x=nonzero_features[sorted_indices][:top_n])
plt.title("Feature importances via coefficients - Ridge(Top10)")
plt.xlabel("Features")
plt.ylabel("Absolute Coefficients")
plt.show()

from sklearn.linear_model import ElasticNetCV

# Fit the Elastic Net model
elastic_net = ElasticNetCV(cv=5, random_state=42).fit(X_train, y_train)
importance = np.abs(elastic_net.coef_)

# Exclude features with zero importance
nonzero_importance = importance[importance > 0]
nonzero_features = np.array(feature_columns)[importance > 0]

# Sort features by importance
top_n = 10
sorted_indices = np.argsort(nonzero_importance)[::-1]

# Plot feature importances
plt.figure(figsize=(10, 6))
plt.bar(x=nonzero_features[sorted_indices][:top_n], height=nonzero_importance[sorted_indices][:top_n], color='#00bc70')
plt.title("Feature importances via coefficients - Elastic Net (Top 10)")
plt.xlabel("Features")
plt.ylabel("Absolute Coefficients")
plt.xticks(rotation=45)
plt.show()

# Print R-squared values
r_squared_train = elastic_net.score(X_train, y_train)
r_squared_test = elastic_net.score(X_test, y_test)
print(f"R-squared (train): {r_squared_train}")
print(f"R-squared (test): {r_squared_test}")

"""### 이렇게 변수별 중요도가 나왔다고 가정
- 전체 카페 데이터 프레임은 X_new

"""

X_new = ...  # Your new DataFrame here

# numeric 변수들만 뽑아서 분포 확인 -> 스케일러 종류 지정하기 위함
num_data = X_new.drop(columns=['branchnm', 'Latitude', 'Longitude', ''])

num_data.hist(figsize=(20,20))

# X_new 데이터 스케일링
scaler = StandardScaler() # or MinMaxScaler(적합한 스케일러로 지정)
X_new_scaled = scaler.transform(X_new)

# Calculate scores using non-zero importances as weights
scores_new = np.dot(X_new_scaled[:, importance > 0], nonzero_importance)

# Add the score as a new column to the X_new DataFrame
X_new_with_scores = pd.DataFrame(X_new_scaled, columns=X_new.columns)  # Create DataFrame from scaled data
X_new_with_scores['Score'] = scores_new  # Add the scores as a new column

X_new_with_scores.head(10)

score_result = X_new_with_scores[['branchnm', '']]