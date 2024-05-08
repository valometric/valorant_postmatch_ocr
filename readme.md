# README for Valorant Postmatch Data Extraction

## Overview

This tool extracts the post game information from a 1920x1080 screenshot of the post game screen. This tool handles processing images, extracting data, and performing validation. It utilizes several Python libraries including OpenCV, pandas, and TensorFlow, to process post match screenshots, extract relevant data, and validate the extracted information against expected outcomes. The project is structured to support multiple modes of operation, including handling single images, batches of images, and performing screenshot operations.

## Installation

Before you can run the scripts, you need to set up your Python environment with the required libraries. Here is how you can get started:

1. **Clone the repository** - Obtain the project files by cloning the repo.
2. **Install dependencies** - Install the required Python libraries with:

   ```bash
   pip install opencv-python-headless pandas matplotlib numpy argparse pytesseract tensorflow keras
   ```

## Usage

The main entry point of the program is `main.py`, which you can run with different modes based on your needs:

```bash
python main.py --mode [screenshot|single|batch|validate] [options]
```

### Options
- `--mode` - Specifies the mode of operation: `screenshot`, `single`, `batch`, or `validate`.
- `--image_path` - Path to the image file to process (optional in some modes).
--single: screenshots/single_image
--batch: screenshots/unprocessed
--validate: screenshots/validation
- `--output_dir` - Directory to save the output data CSV file. Default output/.
- `--output_name` - Name of the output CSV file. Default outputdata.csv
- `--ranked` - Indicates whether the game was ranked or unranked (optional). Default: unranked.

### Modes of Operation

1. **Screenshot Mode**: Takes a screenshot and processes it to extract data.
2. **Single Image Mode**: Processes a single image specified by the `--image_path`.
3. **Batch Mode**: Processes a batch of images from a specified directory.
4. **Validate Mode**: Validates processed data against a reference dataset.

## File Structure

- `data_handling/`
  - Contains utilities for dataframe operations and data validation.
- `image_processing/`
  - Includes all image processing functionalities such as OCR and data extraction from images.
- `config.py`
  - Configuration file containing settings and mappings for processing.

## Features

- **Image Processing**: Utilizes OpenCV to handle image manipulations and TensorFlow for applying machine learning models.
- **OCR Capabilities**: Implements Tesseract via pytesseract for optical character recognition to extract text from images.
- **Data Extraction**: Specific functions to extract various game-related data from images.
- **Validation**: Compares extracted data with a reference dataset to ensure accuracy.

## Advanced Configuration

You can adjust various parameters and configurations in `config.py`, such as path settings, image processing resolutions, and mappings for data extraction.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or create issues for bugs and feature requests.

## License

MIT
