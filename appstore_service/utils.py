import json

def save_json_data(data, output_filename):
    with open(output_filename, "w") as file:
        json.dump(data, file, indent=4) 