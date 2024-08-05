# -*- coding: utf-8 -*-
"""Water_Quality_Prediction_Using_Machine_Learning_Classification_Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1r_7qKeoI4rOrRLOHuXIAkSVk95Wv7E0w

### **Water Quality Prediction Using Machine Learning Classification**

**Context:**

Access to safe drinking-water is essential to health, a basic human right and a component of effective policy for health protection. 
This is important as a health and development issue at a national, regional and local level. 
In some regions, it has been shown that investments in water supply and sanitation can yield a net economic benefit, 
since the reductions in adverse health effects and health care costs outweigh the costs of undertaking the interventions.

---

**Problem Statement:**

The first step to effective healthcare is preventing disease. Widespread access to clean water, sanitation, and hygiene are crucial to ensure this. 
Water quality varies depending on the place and condition of the source of water and the treatment it receives. 
There could be specific contaminants in water resulting in health issues, ranging from gastrointestinal illness, reproductive problems, and neurological disorders. 
Infants, children, pregnant women, the elderly, and those with compromised immune systems may be especially susceptible.

---
**Objective:**

*   To identify the different factors that affect the water potability.
*   To make a model to evaluate water potability using the Water Quality dataset.
---

**Dataset:**

1. ph: pH of 1. water (0 to 14).
2. Hardness: Capacity of water to precipitate soap in mg/L.
3. Solids: Total dissolved solids in ppm.
4. Chloramines: Amount of Chloramines in ppm.
5. Sulfate: Amount of Sulfates dissolved in mg/L.
6. Conductivity: Electrical conductivity of water in μS/cm.
7. Organic_carbon: Amount of organic carbon in ppm.
8. Trihalomethanes: Amount of Trihalomethanes in μg/L.
9. Turbidity: Measure of light emiting property of water in NTU.
10. Potability: Indicates if water is safe for human consumption. Potable -1 and Not potable -0

The dataset contains water quality metrics for 3276 different water bodies.

---

**Importing necessary libraries**
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from io import StringIO

#to scale the data using z-score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

#algorithms to use
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

#Metrics to evaluate the model
from sklearn.metrics import confusion_matrix, classification_report, precision_recall_curve, make_scorer

"""**Importing the CSV Data**"""

orig_url="https://drive.google.com/file/d/1HdaYFPIjNJRqcWuZDrc1QyEdVvgrfLhX/view?usp=sharing"

file_id = orig_url.split('/')[-2]
dwn_url='https://drive.google.com/uc?export=download&id=' + file_id
url = requests.get(dwn_url).text
csv_raw = StringIO(url)
data = pd.read_csv(csv_raw)
data.head()

"""**Printing the Info - DataTypes, Non-Null**"""

#Pulling the information about the data - Data Type, Null Count etc.
data.info()

"""**Unique values**"""

#Identifying the number of unique values available in each columns
data.nunique()

"""**Observations**
- There are 3276 enteries and 10 columns
- There are several missing values for **ph, Sulfate, Trihalomethanes** in the data. So the data needs to be cleaned in order to use it

**Data Summary**
"""

#Pulling statistical Summary of the numerical columns
numerical_columns = ['ph','Hardness','Solids','Chloramines','Sulfate','Conductivity','Organic_carbon','Trihalomethanes','Turbidity']
summary=data[numerical_columns].describe().T
summary.round(2)

"""**Histogram**"""

#Plotting histograms for quantitaive (numerical) variables
data[numerical_columns].hist(figsize=(8,8))
plt.show()

"""**Missing Data Handling**

- Trihalomethanes has very less missing values ~< 5%, so we will delete the rows with missing values
- ph and Sulfate, we will impute the missing values with mean values
"""

#Dropping the rows with missing values for Trihalomethanes
data.dropna(subset=['Trihalomethanes'], how='any', inplace=True)

#Imputing the missing values with mean for ph, Sulfate
mean = data.mean()
data.fillna(mean, inplace=True)

#Pulling data info again to confirm if there are any null values
data.info()

"""**Correlation Matrix for predictor variables**"""

# Checking the correlations
plt.figure(figsize=(16,10))
cmap=sns.diverging_palette(230,20,as_cmap=True)
sns.heatmap(data.corr(),annot=True,fmt=".2f",cmap=cmap)
plt.show()

"""**Observations:**

**Weak Correlations:**
Most of the correlations are weak, as indicated by values close to 0. For example, pH has very low correlations with other variables.
Turbidity shows weak correlations with other variables.

**Negative Correlations:**
The only notable negative correlation is between Solids and Sulfate that too week(approximately -0.14). This suggests that higher sulfate levels are associated with lower solids concentration.

**Interpretation:**
These correlations provide insights into how the predictor variables relate to each other. Since no variables have strong correlation(>0.7) we donot need to check for outliers.

**Separating the independent variables (X) and the dependent variable (Y)**
"""

#Creating Independent and Dependent variables
Y= data.Potability
x= data.drop(columns = ['Potability'])

"""**Scaling the data**"""

scaler = StandardScaler()

scaled_data = scaler.fit_transform(x)

# Create a new DataFrame with scaled data
scaled_x = pd.DataFrame(scaled_data, columns=x.columns)
scaled_x.head()

"""**Splitting the data into 70% train and 30% test set**


"""

#Splitting data for train and test
x_train,x_test,Y_train,Y_test=train_test_split(scaled_x,Y,test_size=0.3,random_state=1,stratify=Y)

"""**Metrics**"""

def metrics_score(actual, predicted):
    print(classification_report(actual, predicted))
    cm = confusion_matrix(actual, predicted)
    plt.figure(figsize=(8,5))
    sns.heatmap(cm, annot=True,  fmt='.2f', xticklabels=['Not Potable', 'Potable'], yticklabels=['Not Potable', 'Potable'])
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.show()

"""# **Model 1: Decision Tree Classifier**"""

#building decision tree
dtc = DecisionTreeClassifier(random_state=1)

#fitting decision tree
dtc = dtc.fit(x_train,Y_train)

#predict the response for test
Y_pred = dtc.predict(x_test)

"""**Evaluating the Model on training data**"""

#checking model performace of training data
Y_pred_train_port = dtc.predict(x_train)
metrics_score(Y_train, Y_pred_train_port)

"""**Evaluating the Model on testing data**"""

Y_pred_test_port = dtc.predict(x_test)
metrics_score(Y_test, Y_pred_test_port)

"""**Observations**

- Achieving a classification rate of 58% indicates a decent level of accuracy.
- However, there is room for improvement by fine-tuning the parameters within the decision tree algorithm.

Upon reviewing the confusion matrix for the training data, it becomes evident that the model's accuracy is lower on the test dataset compared to the training dataset. This inconsistency implies potential overfitting, wherein the model performs well on the training data but struggles to generalize to new, unseen data. To mitigate this overfitting issue, we can employ techniques for hyperparameter tuning.

**Hyperparameter Tuning**
"""

# Define the parameter grid for hyperparameter tuning
param_grid = {
    'criterion': ['gini', 'entropy'],  # Criterion for splitting: Gini impurity or information gain (entropy)
    'splitter': ['best', 'random'],  # Strategy for choosing the split: best or random
    'max_depth': [3, 5, 7, 10],  # Maximum depth of the tree
    'min_samples_split': [2, 5, 10],  # Minimum number of samples required to split an internal node
    'min_samples_leaf': [1, 2, 4]  # Minimum number of samples required to be at a leaf node
}

# Create a decision tree classifier object
dt_classifier = DecisionTreeClassifier(class_weight={0: 0.95, 1: 0.05}, random_state=1)

# Create GridSearchCV object
gsearch = GridSearchCV(dt_classifier, param_grid, cv=5, scoring='accuracy')

# Perform grid search on training data
gsearch.fit(x_train, Y_train)

# Get the best parameters and best score
best_params = gsearch.best_params_
print("Best Parameters:", best_params)

# Train Decision Tree Classifer with the best hyperparameters
best_dt_model = gsearch.best_estimator_
best_dt_model.fit(x_train, Y_train)

# Checking performance on the test dataset
print("Performance on Test Data:")
Y_pred_test_best = best_dt_model.predict(x_test)
metrics_score(Y_test, Y_pred_test_best)

"""**Observations**


*   After hyperparameter tuning the model now demonstrates an overall accuracy of 64%,  which was initially 58%
*   The classifier achieved high recall (0.95) for non-potable instances but struggled with low recall (0.16) for potable instances, indicating a need for improved identification of the latter class.
*   Additionally, precision values of 0.64 for non-potable and 0.66 for potable suggest some false positives in both predictions, calling for refinements to enhance accuracy.

**Feature Importance**
"""

# Get the feature importances from the decision tree model
importances = best_dt_model.feature_importances_

# Get the names of the features
columns = x_train.columns

# Create a DataFrame to store feature importances along with feature names
importance_df = pd.DataFrame(importances, index=columns, columns=['Importance'])

# Sort the DataFrame by importance values in descending order
importance_df = importance_df.sort_values(by='Importance', ascending=False)

# Plot the feature importances
plt.figure(figsize=(8, 6))
sns.barplot(x=importance_df.Importance, y=importance_df.index)
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.title('Decision Tree Feature Importance')
plt.show()

"""**Observations**

*   Chloramines, pH, Sulfate are the top determining factor in the model's decisions and Organic_carbon being the least.​
*   The feature importance suggests that model relies on multiple factors rather than a single dominant one

# **Model 2: Logistic Regression**
"""

# Define the cost matrix
C_FP = 1  # Cost of false positives
C_FN = 10  # Cost of false negatives

# Define custom cost-sensitive loss function
def cost_sensitive_loss(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    cost = cm[0, 1] * C_FP + cm[1, 0] * C_FN  # Cost of false positives + Cost of false negatives
    return cost

# Create a logistic regression model object with cost-sensitive learning
lg_cost_sensitive = LogisticRegression(class_weight='balanced', solver='liblinear')
# 'class_weight' parameter is set to 'balanced' to automatically adjust class weights inversely proportional to class frequencies
# 'solver' parameter is set to 'liblinear' for small datasets

# Fitting the model
lg_cost_sensitive.fit(x_train, Y_train)

# Checking the performance on the training data
print("Performance on Training Data:")
Y_pred_train_cost_sensitive = lg_cost_sensitive.predict(x_train)
metrics_score(Y_train, Y_pred_train_cost_sensitive)

# Checking the performance on the test dataset
print("Performance on Test Data:")
Y_pred_test_cost_sensitive = lg_cost_sensitive.predict(x_test)
metrics_score(Y_test, Y_pred_test_cost_sensitive)

"""**Observations**

*   The precision, recall, and f1-score are nearly identical for classes 0 and 1 between training and testing datasets, indicating the model's predictions are stable across both.
*   The model's consistent performance on both the training and test data implies that it is generalizing well, without signs of overfitting

**Feature Importance**
"""

# Get the coefficients (importances) from the logistic regression model
importances = lg_cost_sensitive.coef_[0]

# Get the names of the features
columns = x_train.columns

importance_df=pd.DataFrame(importances,index=columns,columns=['Importance']).sort_values(by='Importance',ascending=False)

# Plot the feature importances
plt.figure(figsize=(8,6))
sns.barplot(x=importance_df.Importance,y=importance_df.index)
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.title('Logistic Regression Feature Importance')
plt.show()

"""**Observations**

*   The features have varying levels of importance, with some having positive importance and others appearing to have negative importance
*   Positive and negative values for feature importance signify the respective direct and inverse influences that the features have on the predicted outcome, as per the logistic regression analysis

**Precision Recall Curve**
"""

# Printing the coefficients of logistic regression
cols=x.columns

coef_lg=lg_cost_sensitive.coef_

pd.DataFrame(coef_lg,columns=cols).T.sort_values(by=0,ascending=False)

Y_scores_lg=lg_cost_sensitive.predict_proba(x_train) #predict_proba gives the probability of each observation belonging to each class


precisions_lg, recalls_lg, thresholds_lg = precision_recall_curve(Y_train, Y_scores_lg[:,1])

#Plot values of precisions, recalls, and thresholds
plt.figure(figsize=(10,7))
plt.plot(thresholds_lg, precisions_lg[:-1], 'b--', label='Precision')
plt.plot(thresholds_lg, recalls_lg[:-1], 'g--', label = 'Recall')
plt.xlabel('Threshold')
plt.legend(loc='upper left')
plt.ylim([0,1])
plt.show()

"""**Observation**

- This threshold value of 0.51 serves as the point of balance between precision and recall, indicating the trade-off between these two metrics.

- It's the point where the classifier achieves a reasonable balance between making correct positive predictions (precision) and capturing true positive instances (recall).

# **Model 3: K Nearest Neighbors**
"""

param_grid = {
    'n_neighbors': [1, 3, 5, 7, 9, 11, 15]  # Specify the range of values for the number of neighbors (k)
}

knn_classifier = KNeighborsClassifier() # Instantiate a K-Nearest Neighbors classifier object

# Create a GridSearchCV object with 5-fold cross-validation and accuracy scoring
gridsearch = GridSearchCV(knn_classifier, param_grid, cv=5, scoring='accuracy')

# Perform grid search on training data
gridsearch.fit(x_train, Y_train)

# Get the best parameters selected by grid search
best_params = gridsearch.best_params_

print("Best Parameters:", best_params)

# Instantiate a K-Nearest Neighbors classifier with the best hyperparameters
best_dt_model = gridsearch.best_estimator_

# Train the K-Nearest Neighbors classifier with the best hyperparameters on the training data
best_dt_model.fit(x_train, Y_train)

# Evaluate the performance of the best model on the training dataset
print("Performance on Training Data:")
Y_pred_train = best_dt_model.predict(x_train)
metrics_score(Y_train, Y_pred_train)

# Evaluate the performance of the best model on the test dataset
print("Performance on Test Data:")
Y_pred_test_best = best_dt_model.predict(x_test)
metrics_score(Y_test, Y_pred_test_best)

"""**Observations**

*   KNN model achieved an accuracy of 64% on the test data.
*   For class 0, the precision is 66% and the recall is 84%. For class 1, the precision is 57% and the recall is 33%. This indicates that the model is better at identifying class 0 instances compared to class 1 instances.

In summary, while the model shows relatively good performance for class 0 with higher precision and recall, it struggles more with class 1, especially in terms of recall. This suggests that there might be imbalances in the dataset or the features might not be sufficiently capturing the patterns for class 1 instances.

# **Model 4: Standard Vector Classifier**
"""

# Instantiate the SVM model
svm_model = SVC(random_state=1)

#Fitting the SVM model
svm_model.fit(x_train,Y_train)

# Checking the performance on the training data
print("Performance on Training Data:")
Y_pred_train_svm = svm_model.predict(x_train)
metrics_score(Y_train, Y_pred_train_svm)

#checking model performace of test data
print("Performance on Test Data:")
Y_pred_test_svm = svm_model.predict(x_test)
metrics_score(Y_test, Y_pred_test_svm)

"""**Observations**


*   Despite the low recall for class 1 the SVM model demonstartes a better balance between precision and recall for class 0 which heavily influences the overall metrics due to the larger support for class 0.
*   Precision for class 1 is the highest with the SVM model at 71%.
*   SVM model appers to be the most effective model overall.

# **Model 5: Random Forest Classifier**
"""

rf_clf = RandomForestClassifier(n_estimators=100,max_depth=3,min_samples_leaf = 10)
rf_clf.fit(x_train,Y_train)
Y_pred = rf_clf.predict(x_test)

#checking model performace of training data
print("Performance on Training Data:")
Y_pred_train_dt = rf_clf.predict(x_train)
metrics_score(Y_train, Y_pred_train_dt)

#checking model performace of test data
print("Performance on Test Data:")
Y_pred_test_dt = rf_clf.predict(x_test)
metrics_score(Y_test, Y_pred_test_dt)

"""**Observations**

*   Random Forest Model is highly precise for class 1 but with very low recall,leading to a poor f1-score for this class
*   Overall accuracy is moderate at 64% but this figure doesnt reflect the performance disparity between classes

**Feature Importance**
"""

feature_importances = rf_clf.feature_importances_

# Create a DataFrame to display feature importances
importances_df = pd.DataFrame({'Feature': x_train.columns, 'Importance': feature_importances})

# Sort the DataFrame by importance in descending order
importances_df = importances_df.sort_values(by='Importance', ascending=False)

# Display the sorted feature importances
plt.figure(figsize=(8,6))
sns.barplot(x=importance_df.Importance,y=importance_df.index)
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.title('Random Forest Feature Importance')
plt.show()

"""**Observations**

*   The less significant roles of ph and Hardness point to their reduced influence in the model's outcome.
*   The feature Turbidity stands out with the highest importance indicating it is the most significant predictor in the random forest model for this dataset.


"""
