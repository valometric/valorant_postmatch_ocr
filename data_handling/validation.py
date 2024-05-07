import numpy as np
import logging


def check_len(data, numerical=False, kda=False):
    """
    Checks and adjusts the length of the data. Fills with np.nan if not meeting the expected length.
    :param data: The data to be checked and adjusted.
    :param numerical: Boolean flag to check if data should be numerical.
    """
    if len(data) != 10:
        logging.critical(
            f"Critical: Data length is not 10. Found length: {len(data)}. Found data: {data}. Adjusting with np.nan. Manual review recommended."
        )
        data += [np.nan] * (10 - len(data))

    if numerical and not kda:
        for i, x in enumerate(data):

            if not isinstance(x, (int, float)) and not x.isdigit():
                logging.critical(
                    f"Critical: Non-numerical value found where an integer was expected: {x}. Replacing with np.nan."
                )
                data[i] = np.nan
            else:
                data[i] = int(data[i])

    return data
