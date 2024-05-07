import cv2
import pyautogui
import time
import numpy as np
import os


def screenshot(delay=5):
    """
    Takes a screenshot after a specified delay.

    :param delay: Time in seconds before taking the screenshot.
    """
    while delay > 0:
        print(delay)
        time.sleep(1)
        delay -= 1
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image, cv2.COLOR_RGB2BGR))
    image_path = os.path.join("projects/screenshots/single_image/data.png", "data.png")
    cv2.imwrite(image_path, image)
