from collections import Counter
import logging
import pytesseract
import numpy as np
from .ocr_utils import extract_and_resize, clean_text, process_image_slice
from .config import *
from matplotlib import pyplot as plt


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def extract_acs(image, resolution_scale, is_ranked=False) -> list[int]:
    if not is_ranked:
        return process_image_slice(
            image,
            ACS_COL_START,
            UNRANKED_ACS_COL_END,
            resolution_scale,
            is_numeric=True,
        )
    else:
        return process_image_slice(
            image, ACS_COL_START, ACS_COL_END, resolution_scale, is_numeric=True
        )


def extract_ign(image, resolution_scale=1.0, is_ranked=False) -> list[str]:
    if not is_ranked:
        return process_image_slice(
            image, UNRANKED_IGN_COL_START, UNRANKED_IGN_COL_END, resolution_scale
        )
    else:
        return process_image_slice(image, IGN_COL_START, IGN_COL_END, resolution_scale)


def extract_kda(image, resolution_scale=1.0) -> list[list[int]]:
    kda_data = process_image_slice(
        image, KDA_COL_START, KDA_COL_END, resolution_scale, is_numeric=True, kda=True
    )
    for row in kda_data:
        parts = row.split()
        if len(parts) != 3:
            logging.warning(
                f"Warning: KDA Row should be len 3 but was {len(parts)}: {row}. Manual review recommended."
            )
            row = np.nan
    return kda_data


def extract_econ(image, resolution_scale=1.0) -> list[int]:
    return process_image_slice(
        image, ECON_COL_START, ECON_COL_END, resolution_scale, is_numeric=True
    )


def extract_first_bloods(image, resolution_scale=1.0) -> list[int]:
    return process_image_slice(
        image,
        FIRST_BLOODS_COL_START,
        FIRST_BLOODS_COL_END,
        resolution_scale,
        is_numeric=True,
    )


def extract_plants(image, resolution_scale=1.0) -> list[int]:
    return process_image_slice(
        image, PLANTS_COL_START, PLANTS_COL_END, resolution_scale, is_numeric=True
    )


def extract_defuses(image, resolution_scale=1.0) -> list[int]:
    return process_image_slice(
        image, DEFUSES_COL_START, DEFUSES_COL_END, resolution_scale, is_numeric=True
    )


def extract_score(image, resolution_scale):
    result_text = process_image_slice(
        image, SCORE_COL_START, SCORE_COL_END, resolution_scale
    )
    profile_score_text = process_image_slice(
        image, PROFILE_SCORE_COL_START, PROFILE_SCORE_COL_END, resolution_scale
    )
    opponent_score_text = process_image_slice(
        image, OPPONENT_SCORE_COL_START, OPPONENT_SCORE_COL_END, resolution_scale
    )
    return (
        clean_text(opponent_score_text),
        clean_text(profile_score_text),
        clean_text(result_text),
    )


def extract_details(image, resolution_scale):
    date_text = process_image_slice(
        image, DATE_COL_START, DATE_COL_END, resolution_scale
    )
    game_type_text = process_image_slice(
        image, GAME_TYPE_COL_START, GAME_TYPE_COL_END, resolution_scale
    )
    map_text = clean_text(
        process_image_slice(image, MAP_COL_START, MAP_COL_END, resolution_scale)
    ).split()[-1]
    if map_text not in MAPS:
        logging.warning(
            f"Warning: {map_text} was not found in map list. Manual review recommended."
        )
        map_text = np.nan
    duration_text = process_image_slice(
        image, DURATION_COL_START, DURATION_COL_END, resolution_scale
    )
    return (
        clean_text(date_text),
        clean_text(game_type_text),
        map_text,
        clean_text(duration_text),
    )


def extract_agents(image) -> list[str]:
    agent_data = process_image_slice(
        image, AGENT_COL_START, AGENT_COL_END, 1, is_agents=True
    )
    if any(count > 2 for count in Counter(agent_data).values()):
        logging.warning(
            "Warning: Found more than 2 duplicate agents. Manual review recommended."
        )
    return agent_data
