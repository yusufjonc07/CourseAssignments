import os
import numpy as np
import cv2
# from sklearn.model_selection import train_test_split # for splitting data into train and test sets
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

# Function to load images from folders
def load_images_from_folder(folder, img_size=(64, 64)):
    X, y = [], []
    class_labels = sorted(os.listdir(folder))  # Get class names
    label_map = {label: idx for idx, label in enumerate(class_labels)}  # Map classes to integers

    for class_name in class_labels:
        class_path = os.path.join(folder, class_name)
        for img_name in os.listdir(class_path):
            img_path = os.path.join(class_path, img_name)
            img = cv2.imread(img_path)
            if img is not None:
                img = cv2.resize(img, img_size)  # Resize image
                img = img.flatten()  # Flatting the image to 1D array
                # https://images.app.goo.gl/MyYKBTBja98eqUtFA
                X.append(img)
                y.append(label_map[class_name])  # Assign label

    return np.array(X), np.array(y)

# Define dataset paths (train and validation folders)
dataset_folder = "/Users/yusufjon/Documents/university-gachon/introduction-to-AI/SVM/content/iris_data_2/data"
train_folder = os.path.join(dataset_folder, "train")
val_folder = os.path.join(dataset_folder, "val")


# Load training and validation data
X_train, y_train = load_images_from_folder(train_folder)
X_val, y_val = load_images_from_folder(val_folder)

# Scale features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_val = scaler.transform(X_val)

# Train an SVM model
svm_classifier = SVC(kernel='linear', C=0.5)


svm_classifier.fit(X_train, y_train)

# Predict and evaluate model on validation set
y_pred = svm_classifier.predict(X_val)
accuracy = accuracy_score(y_val, y_pred)

print(f"SVM Model Accuracy: {accuracy:.2f}%")
print("Classification Report:\n", classification_report(y_val, y_pred))
