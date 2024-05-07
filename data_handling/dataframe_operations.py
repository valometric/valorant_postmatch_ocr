import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from image_processing.ocr_utils import process_kda
from image_processing.data_extraction import (
    extract_ign,
    extract_agents,
    extract_acs,
    extract_kda,
    extract_econ,
    extract_first_bloods,
    extract_plants,
    extract_defuses,
)


def process_single_image(image_path, is_ranked):
    """
    Processes a single image and extracts all relevant game data.

    :param image_path: Path to the image file.
    :return: DataFrame with extracted data for the image.
    """
    try:
        image = cv2.imread(image_path)
        if image is not None:
            # Convert from BGR to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if image is None:
            raise ValueError(f"Image at {image_path} not found or unable to read.")
        resolution_scale = image.shape[1] / 1920  # Adjust based on image width
        image = cv2.resize(image, (1920, 1080))
        # Extract data using each function
        ign_data = extract_ign(image, resolution_scale, is_ranked)
        agent_data = extract_agents(image)
        acs_data = extract_acs(image, resolution_scale, is_ranked)
        kda_data = extract_kda(image, resolution_scale)
        econ_data = extract_econ(image, resolution_scale)
        first_blood_data = extract_first_bloods(image, resolution_scale)
        plants_data = extract_plants(image, resolution_scale)
        defuses_data = extract_defuses(image, resolution_scale)
        k, d, a = process_kda(kda_data)
        # Combine extracted data into a DataFrame
        player_data = np.array(
            [
                ign_data,
                agent_data,
                acs_data,
                k,
                d,
                a,
                econ_data,
                first_blood_data,
                plants_data,
                defuses_data,
            ]
        ).T
        player_col_names = [
            "ign",
            "agent",
            "acs",
            "k",
            "d",
            "a",
            "econ",
            "fb",
            "plants",
            "defuses",
        ]
        return pd.DataFrame(data=player_data, columns=player_col_names)

    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error


def process_image_batch(image_path="data.png", scale_factor=1.0, idx="1"):
    """
    Processes the game image and returns a DataFrame with the data.

    :param image_path: Path to the image file.
    :param scale_factor: The scale factor for image processing.
    :param idx: Index of the image in the batch.
    :return: DataFrame with the extracted data.
    """
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Image at {image_path} not found or unable to read.")
        resolution_scale = (
            image.shape[1] / 1920 * scale_factor
        )  # Adjust based on image width and scale factor
        player_data = np.array(
            [
                extract_ign(image, resolution_scale),
                extract_acs(image, resolution_scale),
                extract_kda(image, resolution_scale),
                extract_econ(image, resolution_scale),
                extract_first_bloods(image, resolution_scale),
                extract_plants(image, resolution_scale),
                extract_defuses(image, resolution_scale),
            ]
        ).T
        player_col_names = ["ign", "acs", "kda", "econ", "fb", "plants", "defuses"]
        dataframe = pd.DataFrame(data=player_data, columns=player_col_names)
        dataframe["image_idx"] = idx  # Add an index column to identify the image
        return dataframe
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error
