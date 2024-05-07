import cv2
import numpy as np
import os
import logging
import pytesseract
import tensorflow as tf
from tensorflow.keras.applications.inception_v3 import preprocess_input  # type: ignore
from .config import *
from data_handling.validation import check_len
import os
import numpy as np
import matplotlib.pyplot as plt

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Get the absolute path of ocr_utils.py
ocr_utils_path = os.path.realpath(__file__)

# Get the directory containing ocr_utils.py
image_processing_dir = os.path.dirname(ocr_utils_path)

# Get the src directory
src_dir = os.path.dirname(image_processing_dir)

model_dir = os.path.join(src_dir, "model", "best_model.keras")

# Setting Tesseract command
# pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

MODEL = tf.keras.models.load_model(model_dir)


def classify_character(image_array, model):

    # Resize the image to the required input size for the model
    img_resized = cv2.resize(image_array, (49, 45))

    # Convert the image to an array format suitable for the model
    img_array = np.expand_dims(img_resized, axis=0)
    img_array = preprocess_input(img_array)
    # Make predictions
    predictions = MODEL.predict(img_array)
    # Return the class with the highest probability
    return index_to_class_label[np.argmax(predictions[0])]


def preprocess_for_ocr(img, is_numeric=False):
    resized = cv2.resize(img, (img.shape[1] * 4, img.shape[0] * 4))
    # Convert to grayscale
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Invert the image if the text is white on a dark background
    inverted = cv2.bitwise_not(blur)
    # Dilate the text if necessary
    kernel = np.ones((1, 1), np.uint8)
    dilated = cv2.dilate(inverted, kernel, iterations=5)
    return dilated


def extract_and_resize(cropped_img, is_numeric=False):
    """
    Resizes the cropped image and extracts text using OCR.
    :param cropped_img: The image to be resized and processed.
    :return: The extracted text.
    """
    # Apply preprocessing for OCR
    processed_img = preprocess_for_ocr(cropped_img)

    custom_config = r"--oem 1 --psm 6"
    if is_numeric:
        custom_config = (
            r"--oem 1 --psm 6 outputbase digits -c tessedit_char_whitelist=0123456789/"
        )
    else:
        custom_config = r"--oem 1 --psm 6"

    try:
        text = pytesseract.image_to_string(processed_img, config=custom_config)
        return text
    except Exception as e:
        logging.critical(f"Critical: Error during OCR extraction: {e}")
        return np.nan


def clean_text(text):
    """
    Cleans the extracted text.
    :param text: The text to be cleaned.
    :return: Cleaned text.
    """
    return text.strip().replace("\n", "")

def process_kda(text):
    """
    Processes the KDA text extracted from the image.
    :param text: The KDA text to be processed.
    :return: Three variables (k,d,a)
    """
    # Split the text by spaces
    k, d, a = [], [], []
    for kda in text:
        parts = kda.split()
        k.append(parts[0])
        d.append(parts[1])
        a.append(parts[2])
        
    # Check if the KDA row is in the correct format
    if len(parts) != 3:
        logging.warning(
            f"Warning: KDA Row should be len 3 but was {len(parts)}: {text}. Manual review recommended."
        )
        parts = [np.nan, np.nan, np.nan]
    return k, d, a


def crop_by_player(
    col_img, resolution_scale=1, is_numeric=False, is_agents=False, is_ranked=False
):
    """
    Crops the column image by each player.
    :param col_img: The column image to be cropped.
    :param resolution_scale: The scale of the image resolution.
    :return: List of texts extracted from each cropped image.
    """
    y_window = 52
    temp_data = []
    try:
        if is_ranked:
            for i in range(10):
                temp_crop = col_img[0 + (y_window * i) : 50 + (y_window * i), :]
                if not is_agents:
                    text = extract_and_resize(temp_crop, is_numeric)
                    temp_data.append(clean_text(text))
                else:
                    agent = classify_character(temp_crop, MODEL)
                    temp_data.append(agent)
        else:
            for i in range(10):
                temp_crop = col_img[5 + (y_window * i) : 50 + (y_window * i), :]
                if not is_agents:
                    text = extract_and_resize(temp_crop, is_numeric)
                    temp_data.append(clean_text(text))
                else:
                    agent = classify_character(temp_crop, MODEL)
                    team = agent.split("_")[-1]
                    agent = agent.split("_")[0]
                    temp_data.append(agent)
    except Exception as e:
        logging.critical(f"Critical: Error during cropping: {e}")
    return temp_data


def process_image_slice(
    image,
    col_start,
    col_end,
    resolution_scale,
    is_numeric=False,
    kda=False,
    is_agents=False,
):
    img_slice = image[COL_HEIGHT_START:COL_HEIGHT_END, col_start:col_end]
    data = crop_by_player(img_slice, resolution_scale, is_numeric, is_agents=is_agents)
    return check_len(data, numerical=is_numeric, kda=kda)
