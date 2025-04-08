import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

model = tf.keras.models.load_model('cnn_model.h5')

def preprocess_image(img_path):
    img = Image.open(img_path).convert('L')
    img = img.resize((28, 28))
    img = np.array(img)
    img = img / 255.0
    img = img.reshape(1, 28, 28, 1)
    
    return img

def test_multiple_images(image_folder, actuals):
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg'))]
    correct_predictions = 0
    total_images = len(image_files)
    results = []  
    cols = 6  
    rows = 12  
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 2, rows * 2))
    axes = axes.flatten() 
    for i, img_file in enumerate(image_files):
        img_path = os.path.join(image_folder, img_file)
        img = preprocess_image(img_path)
        predictions = model.predict(img)
        predicted_label = np.argmax(predictions)
        actual = actuals.get(img_file, None)
        is_correct = predicted_label == actual
        if is_correct:
            correct_predictions += 1
        results.append((img_file, actual, predicted_label, is_correct))#cmap=plt.cm.binary
        axes[i].imshow(img.reshape(28, 28))
        axes[i].set_title(f"P: {predicted_label} | A: {actual}", fontsize=8)
        axes[i].axis('off')
    plt.show()
    incorrect_predictaion = total_images - correct_predictions
    labels = [f"True:{correct_predictions}", f"False:{incorrect_predictaion}"]
    counts = [correct_predictions, incorrect_predictaion]
    plt.bar(labels, counts)
    plt.xlabel("Prediction Outcome")
    plt.ylabel("Image Numbers:")
    plt.title("Results:")
    plt.show()


actuals = {
    "img_1.jpg": 2,
    "img_2.jpg": 0,
    "img_3.jpg": 9,
    "img_4.jpg": 0,
    "img_5.jpg": 3,
    "img_6.jpg": 7,
    "img_7.jpg": 0,
    "img_8.jpg": 3,
    "img_9.jpg": 0,
    "img_10.jpg": 3,
    "img_11.jpg": 5,
    "img_12.jpg": 7,
    "img_13.jpg": 4,
    "img_14.jpg": 0,
    "img_15.jpg": 4,
    "img_16.jpg": 3,
    "img_17.jpg": 3,
    "img_18.jpg": 1,
    "img_19.jpg": 9,
    "img_20.jpg": 0,
    "img_21.jpg": 9,
    "img_22.jpg": 1,
    "img_23.jpg": 1,
    "img_24.jpg": 5,
    "img_25.jpg": 7,
    "img_26.jpg": 4,
    "img_27.jpg": 2,
    "img_28.jpg": 7,
    "img_29.jpg": 4,
    "img_30.jpg": 7,
    "img_31.jpg": 7,
    "img_32.jpg": 5,
    "img_33.jpg": 4,
    "img_34.jpg": 2,
    "img_35.jpg": 6,
    "img_36.jpg": 2,
    "img_37.jpg": 5,
    "img_38.jpg": 5,
    "img_39.jpg": 1,
    "img_40.jpg": 6,
    "img_41.jpg": 7,
    "img_42.jpg": 7,
    "img_43.jpg": 4,
    "img_44.jpg": 9,
    "img_45.jpg": 8,
    "img_46.jpg": 7,
    "img_47.jpg": 8,
    "img_48.jpg": 2,
    "img_49.jpg": 6,
    "img_50.jpg": 7,
    "img_51.jpg": 6,
    "img_52.jpg": 8,
    "img_53.jpg": 8,
    "img_54.jpg": 3,
    "img_55.jpg": 8,
    "img_56.jpg": 2,
    "img_57.jpg": 1,
    "img_58.jpg": 2,
    "img_59.jpg": 2,
    "img_60.jpg": 0,
    "img_61.jpg": 4,
    "img_62.jpg": 1,
    "img_63.jpg": 7,
    "img_64.jpg": 0,
    "img_65.jpg": 0,
    "img_66.jpg": 0,
    "img_67.jpg": 1,
    "img_68.jpg": 9,
    "img_69.jpg": 0,
    "img_70.jpg": 1,
    "img_71.jpg": 6,
    "img_72.jpg": 6,
}


image_folder = 'testimages'
test_multiple_images(image_folder, actuals)
