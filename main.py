import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from module import download_dataset, organize_dataset, create_model, plot_training, evaluate_model

# Step 1: Download Dataset from Kaggle
kaggle_json_path = "../kaggle.json"  # kaggle.json path outside the project folder
if not os.path.exists("data/annotations"):  # simple check if already extracted
    download_dataset(kaggle_json_path)

# Step 2: Preprocessing dataset
base_dir = "dataset"

organize_dataset()

img_height, img_width = 224, 224
batch_size = 32

train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)
train_gen = train_datagen.flow_from_directory(
    base_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',
    subset='training'
)

val_gen = train_datagen.flow_from_directory(
    base_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',
    subset='validation'
)

test_datagen = ImageDataGenerator(rescale=1./255)
test_gen = test_datagen.flow_from_directory(
    base_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=False
)

# Step 3: Creating CNN Model
model = create_model(input_shape=(img_height, img_width, 3), num_classes=3)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Step 4: Training model
history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=10
)

# Step 5: Save model
if not os.path.exists("models"):
    os.makedirs("models")
model.save("models/mask_detector.h5")

# Step 6: Evaluation & Visualization
if not os.path.exists("visualizations"):
    os.makedirs("visualizations")
plot_training(history)
evaluate_model(model, test_gen)

# Step 7: Summary
loss, acc = model.evaluate(test_gen)
print(f"Test Loss: {loss:.4f}, Test Accuracy: {acc:.4f}")
