import os
import cv2
import numpy as np
import joblib  # For saving/loading model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
from sklearn.decomposition import PCA

# Function to load images from folders
def load_images_from_folder(folder, img_size=(64, 64)):
    X, y = [], []
    class_labels = sorted(os.listdir(folder))  # Get class names
    label_map = {label: idx for idx, label in enumerate(class_labels)}  # Map classes to integers

    for class_name in class_labels:
        class_path = os.path.join(folder, class_name)
        if not os.path.isdir(class_path):
            continue  # Skip non-folder files

        for img_name in os.listdir(class_path):
            img_path = os.path.join(class_path, img_name)
            img = cv2.imread(img_path)
            if img is not None:
                img = cv2.resize(img, img_size)  # Resize image
                img = img.flatten()  # Flatten image to 1D array
                X.append(img)
                y.append(label_map[class_name])  # Assign label

    return np.array(X), np.array(y), label_map

# Define dataset paths
dataset_folder = "/content/iris_data_2/data"
train_folder = os.path.join(dataset_folder, "train")
val_folder = os.path.join(dataset_folder, "val")

# Load training and validation data
X_train, y_train, label_map = load_images_from_folder(train_folder)
X_val, y_val, _ = load_images_from_folder(val_folder)

# Scale features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_val = scaler.transform(X_val)

# Dimensionality reduction to speed up training
pca = PCA(n_components=1)  # Reduce features while keeping most variance
X_train = pca.fit_transform(X_train)
X_val = pca.transform(X_val)

# Train SVM in a loop (simulating multiple epochs)
best_accuracy = 0
final_model = None

for epoch in range(1, 3):
    print(f"Epoch {epoch}/3:")

    svm_classifier = SVC(kernel='linear', C=0.5)
    svm_classifier.fit(X_train, y_train)

    # Evaluate model
    y_pred = svm_classifier.predict(X_val)
    accuracy = accuracy_score(y_val, y_pred) * 100
    print(f"Accuracy: {accuracy:.2f}%")

    # Save best model
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        final_model = svm_classifier

# Save final model and preprocessing steps
joblib.dump(final_model, "svm_model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(pca, "pca.pkl")
joblib.dump(label_map, "label_map.pkl")

print("\n✅ Training completed! Best model saved as 'svm_model.pkl'")