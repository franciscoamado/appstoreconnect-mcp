"""Utility functions for App Store Connect service operations."""
import json


def save_json_data(data, output_filename):
    """Save data to a JSON file with proper formatting."""
    with open(output_filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
