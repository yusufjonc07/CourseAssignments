# IMPORTING NECESSARY LIBRARIES

import numpy as np # -> HELPS WITH FILE AND DIRECTORY OPERATIONS
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


#==============================================================================================================
# =========>>>>>> Loading Iris dataset <<<<<<======== (4 features, 3 classes)

iris = datasets.load_iris()
# https://images.app.goo.gl/6BuqKh34ztz2cxkV8
# https://images.app.goo.gl/JdgP7T8szSBTLbsf9

X, y = iris.data, iris.target  # Features and labels

# Split into training and testing sets (80% train, 20% test)
# https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html#
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardizing features for SVM and KNN (some models require normalization)
# https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html#
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

#==============================================================================================================
# ======> Function to train and evaluate models  <==========

def train_and_evaluate(model, X_train, X_test, y_train, y_test, model_name):
    model.fit(X_train, y_train)  # Train model
    y_pred = model.predict(X_test)  # Make predictions
    accuracy = accuracy_score(y_test, y_pred)

    # print(f"\n{model_name} Results:")
    # print(f"Accuracy: {accuracy:.4f}")
    # print("Classification Report:\n", classification_report(y_test, y_pred))
    # print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

#================================================================================================================

# 1. K-Nearest Neighbors (KNN)
knn = KNeighborsClassifier(n_neighbors=5)
train_and_evaluate(knn, X_train_scaled, X_test_scaled, y_train, y_test, "K-Nearest Neighbors (KNN)")


# 2. Decision Tree
dt = DecisionTreeClassifier(criterion="gini", max_depth=4, random_state=42)
train_and_evaluate(dt, X_train, X_test, y_train, y_test, "Decision Tree")


# 3. Random Forest
rf = RandomForestClassifier(n_estimators=100, random_state=42)
train_and_evaluate(rf, X_train, X_test, y_train, y_test, "Random Forest")


# 4. Support Vector Machine (SVM)
svm = SVC(kernel='linear', C=1.0, random_state=42)
train_and_evaluate(svm, X_train_scaled, X_test_scaled, y_train, y_test, "Support Vector Machine (SVM)")

#===============================================================================================================
# Visualizing Decision Boundaries (for only 2 features to keep it simple)

def plot_decision_boundary(model, X, y, title):
    h = .02  # Step size in the mesh
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))

    # Predict class labels for grid points
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    # Plot decision boundary
    plt.contourf(xx, yy, Z, alpha=0.3)
    plt.scatter(X[:, 0], X[:, 1], c=y, edgecolor='k', marker='o')
    plt.xlabel(iris.feature_names[0])
    plt.ylabel(iris.feature_names[1])
    plt.title(title)
    plt.show()

#===============================================================================================================
# Train models on only 2 features for visualization
X_train_2D, X_test_2D = X_train[:, :2], X_test[:, :2]


knn = KNeighborsClassifier(n_neighbors=5).fit(X_train_2D, y_train)
plot_decision_boundary(knn, X_train_2D, y_train, "KNN Decision Boundary")

dt = DecisionTreeClassifier(max_depth=4, random_state=42).fit(X_train_2D, y_train)
plot_decision_boundary(dt, X_train_2D, y_train, "Decision Tree Decision Boundary")

rf = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_train_2D, y_train)
plot_decision_boundary(rf, X_train_2D, y_train, "Random Forest Decision Boundary")

svm = SVC(kernel='linear', C=1.0, random_state=42).fit(X_train_2D, y_train)
plot_decision_boundary(svm, X_train_2D, y_train, "SVM Decision Boundary")
