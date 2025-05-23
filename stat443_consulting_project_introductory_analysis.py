# -*- coding: utf-8 -*-
"""STAT443 Consulting Project Introductory Analysis

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1t9842lARefOqhDSF-YfAqvNaOvSqzhvz
"""

# imports

# data analysis
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# preprocessing
from sklearn.preprocessing import StandardScaler

# regression
from sklearn.linear_model import LinearRegression
import statsmodels.formula.api as smf
import statsmodels as models

df = pd.read_csv("/content/TurbineGroup7.csv")
df

df.describe()

corr = df.corr()
corr.style.background_gradient(cmap='coolwarm')

plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='vlag')
plt.show()

# sns.pairplot(df)

plt.scatter(data = df, x = df.CO, y = 'TEY')
plt.title("Plot of CO against TEY")
plt.xlabel("CO")
plt.ylabel("TEY")
plt.show()

fig, axes = plt.subplots(2, 5, figsize=(15,5))
axes = axes.flatten()

for i,col in enumerate(df.columns.drop("CO")):
    sns.scatterplot(data=df, x='CO', y=col, ax=axes[i])
    axes[i].set_xlabel('CO')
    axes[i].set_ylabel(col)
    axes[i].set_title(f"Scatterplot of CO against {col}")

plt.tight_layout()
plt.show()

df_small = df[df['CO'] > 15]
theline = df.iloc[5905:5928]
theline
# 1.11

df_clean = df.drop(df.index[5905:5929])
# sns.pairplot(df_clean)

fig, axes = plt.subplots(2, 5, figsize=(15,5))
axes = axes.flatten()

for i,col in enumerate(df_clean.columns.drop("CO")):
    sns.scatterplot(data=df_clean, x='CO', y=col, ax=axes[i])
    axes[i].set_xlabel('CO')
    axes[i].set_ylabel(col)
    axes[i].set_title(f"Scatterplot of CO against {col}")

plt.tight_layout()
plt.show()

plt.scatter(data = df, x = 'CO', y = 'TAT')

df.CO.hist(bins = 60)

y = df.CO
x = df.drop(['CO', 'NOX'], axis=1)
y_clean = df_clean.CO
x_clean = df_clean.drop(['CO', 'NOX'], axis=1)
x_control = df_clean.drop(['CO','NOX','AT','AH','AP','TEY'], axis=1)

x_clean.columns

ols = smf.ols('CO~GTEP+TIT+TAT+CDP+TEY+AH+AP+AT', data=df_clean).fit()
ols.summary()

scaler = StandardScaler()

df_scaled = scaler.fit_transform(df_clean)
df_scaled = pd.DataFrame(df_scaled, columns=df.columns)
df_scaled

df_scaled.describe()

y_scaled = df_scaled.CO
x_scaled = df_scaled.drop(['CO', 'NOX'], axis=1)

ols_scaled = smf.ols("CO~GTEP+TIT+TAT+CDP+TEY+AH+AP+AT+AFDP", data=df_scaled).fit()
ols_scaled.summary()

df_transformed = df_scaled.copy()
df_transformed['CO'] = df_transformed['CO'] ** 0.35

ols_transformed = smf.ols("CO~GTEP+TIT+TAT+CDP+TEY+AH+AP+AT+AFDP", data=df_transformed).fit()
ols_transformed.summary()

# > 160
# 130 - 136

df_high_yield = df_clean[df_clean.TEY > 160]
df_med_yield = df_clean[(df_clean.TEY >= 130) & (df_clean.TEY <= 136)]

df_high_yield.describe()

df_med_yield.describe()

y_high = df_high_yield.CO
x_high = df_high_yield.drop(['CO', 'NOX'], axis=1)

ols_high = smf.ols("CO~GTEP+TIT+TAT+CDP+TEY+AH+AP+AT", data=df_high_yield).fit()
ols_high.summary()

df_high_scaled = scaler.fit_transform(df_high_yield)
df_high_scaled = pd.DataFrame(df_high_scaled, columns=df_high_yield.columns)
df_high_scaled

ols_high_scaled = smf.ols("CO~GTEP+TIT+TAT+CDP+TEY+AH+AP+AT", data=df_high_scaled).fit()
ols_high_scaled.summary()

df_high_transformed = df_high_scaled.copy()
df_high_transformed['CO'] = df_high_transformed['CO'] ** 0.436

ols_high_transformed = smf.ols("CO~GTEP+TIT+TAT+CDP+TEY+AH+AP+AT", data=df_high_transformed).fit()
ols_high_transformed.summary()

ols_med = smf.ols("CO~GTEP+TIT+TAT+CDP+TEY+AH+AP+AT", data=df_med_yield).fit()
ols_med.summary()

df_med_scaled = scaler.fit_transform(df_med_yield)
df_med_scaled = pd.DataFrame(df_med_scaled, columns=df_med_yield.columns)
df_med_scaled

ols_med_scaled = smf.ols("CO~GTEP+TIT+TAT+CDP+TEY+AH+AP+AT", data=df_med_scaled).fit()
ols_med_scaled.summary()

df_med_transformed = df_med_scaled.copy()
df_med_transformed['CO'] = df_med_transformed['CO'] ** 0.506

ols_med_transformed = smf.ols("CO~GTEP+TIT+TAT+CDP+TEY+AH+AP+AT", data=df_med_transformed).fit()
ols_med_transformed.summary()

df.sort_values(by = 'CO', ascending = False).head(10)

"""## Model Selection"""

# imports
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV, KFold

from sklearn.linear_model import Lasso, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor

from sklearn.metrics import mean_squared_error, r2_score

X = df_clean.drop(['CO', 'NOX'], axis=1)
y = df_clean['CO']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=443)

lasso = Lasso()
lasso.fit(X_train, y_train)

# Make predictions
y_pred = lasso.predict(X_test)

# Calculate metrics
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

coef_df = pd.DataFrame({'Feature': X_train.columns, 'Coefficient': lasso.coef_})
print(coef_df)
print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

y_train_pred = lasso.predict(X_train)
train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
print(f"Training RMSE: {train_rmse}")
train_r2 = r2_score(y_train, y_train_pred)
print(f"Training R-squared: {train_r2}")

# Create and train the Ridge model
ridge = Ridge()
ridge.fit(X_train, y_train)

# Make predictions
y_pred = ridge.predict(X_test)

# Calculate metrics
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Create a DataFrame of coefficients with column names
coef_df = pd.DataFrame({'Feature': X_train.columns, 'Coefficient': ridge.coef_})

# Print the DataFrame
print("Ridge Coefficients:")
print(coef_df)
print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

y_train_pred = ridge.predict(X_train)
train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
print(f"Training RMSE: {train_rmse}")
train_r2 = r2_score(y_train, y_train_pred)
print(f"Training R-squared: {train_r2}")

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Make predictions
y_pred = rf_model.predict(X_test)

# Calculate metrics
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
importance_df = pd.DataFrame({'Feature': X_train.columns, 'Importance': rf_model.feature_importances_})
importance_df = importance_df.sort_values(by='Importance', ascending=False)

print("Random Forest Feature Importances:")
print(importance_df)
print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

y_train_pred = rf_model.predict(X_train)
train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
print(f"Training RMSE: {train_rmse}")
train_r2 = r2_score(y_train, y_train_pred)
print(f"Training R-squared: {train_r2}")

sns.barplot(data=importance_df, x='Feature', y='Importance')
plt.xticks(rotation=90)
plt.xlabel('Feature')
plt.ylabel('Coefficient')
plt.title('Random Forest Feature Importances (Overall)')
plt.show()

param_grid = {}

kf = KFold(n_splits=5, shuffle=True, random_state=443)

grid_lm = GridSearchCV(LinearRegression(), param_grid, scoring='r2', cv=kf)
grid_lm.fit(X_train, y_train)

# Lasso CV
grid_lasso = GridSearchCV(lasso, param_grid, scoring='r2', cv=kf)
grid_lasso.fit(X_train, y_train)

# Ridge CV
grid_ridge = GridSearchCV(ridge, param_grid, scoring='r2', cv=kf)
grid_ridge.fit(X_train, y_train)

# Random Forest CV
grid_rf = GridSearchCV(rf_model, param_grid, scoring='r2', cv=kf)
grid_rf.fit(X_train, y_train)

# Best models
best_lm = grid_lm.best_estimator_
best_lasso = grid_lasso.best_estimator_
best_ridge = grid_ridge.best_estimator_
best_rf = grid_rf.best_estimator_

# Best scores (R2)
best_score_lm = grid_lm.best_score_
best_score_lasso = grid_lasso.best_score_
best_score_ridge = grid_ridge.best_score_
best_score_rf = grid_rf.best_score_

# Print R2
print(f"Best LM score: {best_score_lm}")
print(f"Best Lasso score: {best_score_lasso}")
print(f"Best Ridge score: {best_score_ridge}")
print(f"Best RF score: {best_score_rf}")

best_rf.get_params()

importance_df = pd.DataFrame({'Feature': X_train.columns, 'Importance': best_rf.feature_importances_})
importance_df = importance_df.sort_values(by='Importance', ascending=False)

print("Random Forest Feature Importances:")
print(importance_df)

sns.barplot(data=importance_df, x='Feature', y='Importance', hue='Feature', legend = False, palette=reversed(sns.dark_palette("#7fd6c3ff", 9)))
plt.xticks(rotation=90)
plt.xlabel('Feature')
plt.ylabel('Coefficient')
plt.title('Random Forest Feature Importances (Overall)')
plt.show()

# Get RMSE from best models

y_pred = best_lm.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"LM RMSE: {rmse}")

y_pred = best_lasso.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"Lasso RMSE: {rmse}")

y_pred = best_ridge.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"Ridge RMSE: {rmse}")

y_pred = best_rf.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"RF RMSE: {rmse}")

# rmse

param_grid = {}

kf = KFold(n_splits=5, shuffle=True, random_state=443)

grid_lm = GridSearchCV(LinearRegression(), param_grid, scoring='neg_mean_squared_error', cv=kf)
grid_lm.fit(X_train, y_train)

# Lasso CV
grid_lasso = GridSearchCV(lasso, param_grid, scoring='neg_mean_squared_error', cv=kf)
grid_lasso.fit(X_train, y_train)

# Ridge CV
grid_ridge = GridSearchCV(ridge, param_grid, scoring='neg_mean_squared_error', cv=kf)
grid_ridge.fit(X_train, y_train)

# Random Forest CV
grid_rf = GridSearchCV(rf_model, param_grid, scoring='neg_mean_squared_error', cv=kf)
grid_rf.fit(X_train, y_train)

# Best models
best_lm = grid_lm.best_estimator_
best_lasso = grid_lasso.best_estimator_
best_ridge = grid_ridge.best_estimator_
best_rf = grid_rf.best_estimator_

# Best scores (R2)
best_score_lm = grid_lm.best_score_
best_score_lasso = grid_lasso.best_score_
best_score_ridge = grid_ridge.best_score_
best_score_rf = grid_rf.best_score_

# Print R2
print(f"Best LM RMSE: {(-best_score_lm)**0.5}")
print(f"Best Lasso RMSE: {(-best_score_lasso)**0.5}")
print(f"Best Ridge RMSE: {(-best_score_ridge)**0.5}")
print(f"Best RF RMSE: {(-best_score_rf)**0.5}")

df_clean.describe()

# predicting based on a pre-existing instance

original_instance = df_clean.iloc[443]

vars_to_adjust = ['AFDP', 'GTEP', 'TIT', 'TAT', 'CDP']

for var_to_adjust in vars_to_adjust:
  linspace_start = df_clean[var_to_adjust].min()
  linspace_stop = df_clean[var_to_adjust].max()
  num_steps = 20

  linspace_values = np.linspace(linspace_start, linspace_stop, num_steps)

  new_observations = []
  for value in linspace_values:
      new_instance = original_instance.copy()
      new_instance[var_to_adjust] = value
      new_observations.append(new_instance)

  new_df = pd.DataFrame(new_observations)
  new_X = new_df.drop(['CO', 'NOX'], axis=1)
  new_y = new_df['CO']

  y_pred = best_rf.predict(new_X)

  plt.plot(linspace_values, y_pred, label='Predicted CO', color='#45818eff')
  plt.scatter(df_clean[var_to_adjust], df_clean['CO'], label='Original Data', alpha=0.3, color='#7fd6c3ff')
  plt.xlabel(var_to_adjust)
  plt.ylabel('Predicted CO')
  plt.title(f"Predicted CO vs {var_to_adjust}")
  plt.show()

"""### Med Yield"""

X_med = df_med_yield.drop(['CO', 'NOX'], axis=1)
y_med = df_med_yield['CO']

X_train_med, X_test_med, y_train_med, y_test_med = train_test_split(X_med, y_med, test_size=0.2, random_state=100)

param_grid = {}

kf = KFold(n_splits=5, shuffle=True, random_state=443)

# LM CV
grid_lm = GridSearchCV(LinearRegression(), param_grid, scoring='r2', cv=kf)
grid_lm.fit(X_train_med, y_train_med)

# Lasso CV
grid_lasso = GridSearchCV(lasso, param_grid, scoring='r2', cv=kf)
grid_lasso.fit(X_train_med, y_train_med)

# Ridge CV
grid_ridge = GridSearchCV(ridge, param_grid, scoring='r2', cv=kf)
grid_ridge.fit(X_train_med, y_train_med)

# Random Forest CV
grid_rf = GridSearchCV(rf_model, param_grid, scoring='r2', cv=kf)
grid_rf.fit(X_train_med, y_train_med)

# Best models
best_lm = grid_lm.best_estimator_
best_lasso = grid_lasso.best_estimator_
best_ridge = grid_ridge.best_estimator_
best_rf = grid_rf.best_estimator_

# Best scores (R2)
best_score_lm = grid_lm.best_score_
best_score_lasso = grid_lasso.best_score_
best_score_ridge = grid_ridge.best_score_
best_score_rf = grid_rf.best_score_

# Print R2
print(f"Best LM score: {best_score_lasso}")
print(f"Best Lasso score: {best_score_lasso}")
print(f"Best Ridge score: {best_score_ridge}")
print(f"Best RF score: {best_score_rf}")

# Get RMSE from best models

y_pred = best_lm.predict(X_test_med)
rmse = np.sqrt(mean_squared_error(y_test_med, y_pred))
print(f"LM RMSE: {rmse}")

y_pred = best_lasso.predict(X_test_med)
rmse = np.sqrt(mean_squared_error(y_test_med, y_pred))
print(f"Lasso RMSE: {rmse}")

y_pred = best_ridge.predict(X_test_med)
rmse = np.sqrt(mean_squared_error(y_test_med, y_pred))
print(f"Rodge RMSE: {rmse}")

y_pred = best_rf.predict(X_test_med)
rmse = np.sqrt(mean_squared_error(y_test_med, y_pred))
print(f"RF RMSE: {rmse}")

lasso = Lasso()
lasso.fit(X_train_med, y_train_med)

# Make predictions
y_pred = lasso.predict(X_test_med)

# Calculate metrics
mse = mean_squared_error(y_test_med, y_pred)
r2 = r2_score(y_test_med, y_pred)

coef_df = pd.DataFrame({'Feature': X_train_med.columns, 'Coefficient': lasso.coef_,})
print(coef_df)
print(lasso.intercept_)
print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

# Create and train the Ridge model
ridge = Ridge()
ridge.fit(X_train_med, y_train_med)

# Make predictions
y_pred = ridge.predict(X_test_med)

# Calculate metrics
mse = mean_squared_error(y_test_med, y_pred)
r2 = r2_score(y_test_med, y_pred)

# Create a DataFrame of coefficients with column names
coef_df = pd.DataFrame({'Feature': X_train_med.columns, 'Coefficient': ridge.coef_})

# Print the DataFrame
print("Ridge Coefficients:")
print(coef_df)
print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train_med, y_train_med)

# Make predictions
y_pred = rf_model.predict(X_test_med)

# Calculate metrics
mse = mean_squared_error(y_test_med, y_pred)
r2 = r2_score(y_test_med, y_pred)
importance_df = pd.DataFrame({'Feature': X_train_med.columns, 'Importance': rf_model.feature_importances_})
importance_df = importance_df.sort_values(by='Importance', ascending=False)

print("Random Forest Feature Importances:")
print(importance_df)
print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

sns.barplot(data=importance_df, x='Feature', y='Importance', palette=reversed(sns.dark_palette("#7fd6c3ff", 9)))
plt.xticks(rotation=90)
plt.xlabel('Feature')
plt.ylabel('Coefficient')
plt.title('Random Forest Feature Importances (Medium Yield)')
plt.show()

X_high = df_high_yield.drop(['CO', 'NOX'], axis=1)
y_high = df_high_yield['CO']

X_train_high, X_test_high, y_train_high, y_test_high = train_test_split(X_high, y_high, test_size=0.2, random_state=100)

param_grid = {}

kf = KFold(n_splits=5, shuffle=True, random_state=443)

# Lasso CV
grid_lasso = GridSearchCV(lasso, param_grid, scoring='r2', cv=kf)
grid_lasso.fit(X_train_high, y_train_high)

# Ridge CV
grid_ridge = GridSearchCV(ridge, param_grid, scoring='r2', cv=kf)
grid_ridge.fit(X_train_high, y_train_high)

# Random Forest CV
grid_rf = GridSearchCV(rf_model, param_grid, scoring='r2', cv=kf)
grid_rf.fit(X_train_high, y_train_high)

# Best models
best_lm = grid_lm.best_estimator_
best_lasso = grid_lasso.best_estimator_
best_ridge = grid_ridge.best_estimator_
best_rf = grid_rf.best_estimator_

# Best scores (R2)
best_score_lm = grid_lm.best_score_
best_score_lasso = grid_lasso.best_score_
best_score_ridge = grid_ridge.best_score_
best_score_rf = grid_rf.best_score_

# Print R2
print(f"Best LM score: {best_score_lm}")
print(f"Best Lasso score: {best_score_lasso}")
print(f"Best Ridge score: {best_score_ridge}")
print(f"Best RF score: {best_score_rf}")

# Get RMSE from best models

y_pred = best_lm.predict(X_test_high)
rmse = np.sqrt(mean_squared_error(y_test_high, y_pred))
print(f"LM RMSE: {rmse}")

y_pred = best_lasso.predict(X_test_high)
rmse = np.sqrt(mean_squared_error(y_test_high, y_pred))
print(f"Lasso RMSE: {rmse}")

y_pred = best_ridge.predict(X_test_high)
rmse = np.sqrt(mean_squared_error(y_test_high, y_pred))
print(f"Ridge RMSE: {rmse}")

y_pred = best_rf.predict(X_test_high)
rmse = np.sqrt(mean_squared_error(y_test_high, y_pred))
print(f"RF RMSE: {rmse}")

importance_df = pd.DataFrame({'Feature': X_train.columns, 'Importance': best_rf.feature_importances_})
importance_df = importance_df.sort_values(by='Importance', ascending=False)

print("Random Forest Feature Importances:")
print(importance_df)

sns.barplot(data=importance_df, x='Feature', y='Importance', hue='Feature', legend = False, palette=reversed(sns.dark_palette("#7fd6c3ff", 9)))
plt.xticks(rotation=90)
plt.xlabel('Feature')
plt.ylabel('Coefficient')
plt.title('Random Forest Feature Importances (High Yield)')
plt.show()

lasso = Lasso()
lasso.fit(X_train_high, y_train_high)

# Make predictions
y_pred = lasso.predict(X_test_high)

# Calculate metrics
mse = mean_squared_error(y_test_high, y_pred)
r2 = r2_score(y_test_high, y_pred)

coef_df = pd.DataFrame({'Feature': X_train_high.columns, 'Coefficient': lasso.coef_})
print(coef_df)
print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

# Create and train the Ridge model
ridge = Ridge()
ridge.fit(X_train_high, y_train_high)

# Make predictions
y_pred = ridge.predict(X_test_high)

# Calculate metrics
mse = mean_squared_error(y_test_high, y_pred)
r2 = r2_score(y_test_high, y_pred)

# Create a DataFrame of coefficients with column names
coef_df = pd.DataFrame({'Feature': X_train_high.columns, 'Coefficient': ridge.coef_})

# Print the DataFrame
print("Ridge Coefficients:")
print(coef_df)
print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train_high, y_train_high)

# Make predictions
y_pred = rf_model.predict(X_test_high)

# Calculate metrics
mse = mean_squared_error(y_test_high, y_pred)
r2 = r2_score(y_test_high, y_pred)
importance_df = pd.DataFrame({'Feature': X_train_high.columns, 'Importance': rf_model.feature_importances_})
importance_df = importance_df.sort_values(by='Importance', ascending=False)

print("Random Forest Feature Importances:")
print(importance_df)
print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

sns.barplot(data=importance_df, x='Feature', y='Importance')
plt.xticks(rotation=90)
plt.xlabel('Feature')
plt.ylabel('Coefficient')
plt.title('Random Forest Feature Importances (High Yield)')
plt.show()



"""### Quantifying?"""

