import os
import sys
import pandas as pd
import argparse
from data_handling import dataframe_operations
from image_processing import screenshot_utils, data_extraction, ocr_utils

# Determine the base directory of the main.py script
base_dir = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)  # Go up one level from the src directory


def get_full_path(*relative_path_parts):
    """Constructs an absolute path from the base directory and the relative path parts."""
    return os.path.join(base_dir, *relative_path_parts)


def main():
    image_path = get_full_path("screenshots", "single_image", "data.png")
    parser = argparse.ArgumentParser(description="Image Data Extraction and Processing")
    parser.add_argument(
        "--mode",
        choices=["screenshot", "single", "batch", "validate"],
        default="single",
        help="Mode of operation",
    )
    parser.add_argument(
        "--image_path",
        default=image_path,
        help="Path of the image to process. OPTIONAL",
    )
    parser.add_argument(
        "--output_dir", default="output/", help="Directory to save extracted data CSV"
    )
    parser.add_argument(
        "--output_name",
        default="extracted_data.csv",
        help="Name of the output CSV file",
    )
    parser.add_argument(
        "--ranked",
        default="False",
        help="Specify whether the game was ranked or unranked. OPTIONAL",
    )
    args = parser.parse_args()
    print(f"Mode selected: {args.mode}")  # Add this line for debugging
    if args.ranked == "True":
        is_ranked = True
    else:
        is_ranked = False
    if args.mode == "screenshot":
        screenshot_path = get_full_path("screenshots", "single_image", "data.png")
        screenshot_and_extract(screenshot_path, args.output_dir, args.output_name)
    elif args.mode == "single":
        extract_single_image(args.output_dir, args.output_name, args.image_path)
    elif args.mode == "batch":
        batch_extract(args.output_dir, args.output_name, is_ranked)
    elif args.mode == "validate":
        validate_model(args.output_dir)
    else:
        sys.exit()


def save_to_csv(extracted_data, output_dir, output_name):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = os.path.join(output_dir, output_name)
    try:
        existing_data = pd.read_csv(output_path)
        combined_data = pd.concat([existing_data, extracted_data])
    except:
        combined_data = extracted_data
    combined_data.to_csv(output_path, index=False)


def screenshot_and_extract(output_dir, output_name, is_ranked):
    screenshot_utils.screenshot(delay=5)
    extracted_data = dataframe_operations.process_single_image(
        "project/screenshots/single_image/data.png", is_ranked
    )
    save_to_csv(extracted_data, output_dir, output_name)


def extract_single_image(
    output_dir,
    output_name,
    image_path=".../project/screenshots/single_image/",
    is_ranked=False,
):
    extracted_data = dataframe_operations.process_single_image(image_path, is_ranked)
    save_to_csv(extracted_data, output_dir, output_name)


def batch_extract(output_dir, output_name, is_ranked):
    unprocessed_path = get_full_path("screenshots", "unprocessed")
    for filename in os.listdir(unprocessed_path):
        if filename.endswith(".png"):
            image_path = os.path.join(unprocessed_path, filename)
            extracted_data = dataframe_operations.process_single_image(
                image_path, is_ranked
            )
            save_to_csv(extracted_data, output_dir, output_name)


def validate_model(output_dir, is_ranked=True):
    validation_path = get_full_path("screenshots", "validation")
    validation_output_path = get_full_path("validation_output")
    if not os.path.exists(validation_output_path):
        os.makedirs(validation_output_path)

    validation_results = []

    # Retrieve and sort the list of validation files
    validation_files = [f for f in os.listdir(validation_path) if f.endswith(".png")]
    sorted_validation_files = sorted(
        validation_files, key=lambda x: int(x.split("validation")[1].split(".png")[0])
    )

    # Loop through each file in the sorted list
    for filename in sorted_validation_files:
        image_path = os.path.join(validation_path, filename)
        try:
            extracted_data = dataframe_operations.process_single_image(
                image_path, is_ranked
            )
            validation_results.append(extracted_data)
            print(f"Processed {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    # Combine all results into a single DataFrame
    all_results = pd.concat(validation_results)

    # Save the combined results to a CSV in the validation_output folder
    output_file = os.path.join(validation_output_path, "validation_results.csv")
    all_results.to_csv(output_file, index=False)
    print(f"Validation results saved to {output_file}")

    # Read the generated validation results
    validation_results_df = pd.read_csv(output_file)

    # Read the reference data (validate_truth.csv)
    truth_file = os.path.join(validation_output_path, "validation_truth.csv")
    truth_df = pd.read_csv(truth_file)

    # Compare the DataFrames and report discrepancies
    compare_and_report(validation_results_df, truth_df)


def compare_and_report(df1, df2):
    # Assuming both dataframes have the same structure
    if df1.equals(df2):
        print("Validation successful: No discrepancies found.")
    else:
        # Report discrepancies
        # This is a basic example. You might want to customize how you report differences
        differences = df1.compare(df2)
        print("Discrepancies found:")
        print(differences)


if __name__ == "__main__":
    main()
