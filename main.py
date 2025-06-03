import json
import requests
from tqdm import tqdm
import os
from dotenv import load_dotenv

download_dir = "downloads"
os.makedirs(download_dir, exist_ok=True)

folders_json = "folders.json"

if not os.path.isfile(folders_json):
    raise FileNotFoundError(f"JSON file '{folders_json}' not found.")

with open(folders_json, "r") as file:
    json_data = json.load(file)[0]

folders = json_data.get("Folder", [])
if not folders:
    raise ValueError("No folders found in the JSON file.")

print(f"Found {len(folders)} folders in the JSON file.")

env_file = "local.env"
if not os.path.isfile(env_file):
    raise FileNotFoundError(f"Environment file '{env_file}' not found.")

load_dotenv(env_file)

username = os.getenv("DL_USERNAME")
password = os.getenv("DL_PASSWORD")

print(f"Username {username}, password {len(password) * '*'}.")

for folder in folders:
    folder_name = folder.get("Name")
    print(f"Processing folder: {folder_name}")

    folder_dir = os.path.join(download_dir, folder_name)
    os.makedirs(folder_dir, exist_ok=True)

    folder_files = folder.get("File", [])
    print(f"Found {len(folder_files)} files in folder '{folder_name}'.")

    for folder_file in tqdm(folder_files, desc=f"Downloading files from {folder_name}"):
        video_data = folder_file.get("Data", {})

        video_name = video_data["General"]["Name"]
        video_url = video_data["Url"]["Download"]

        download_path = os.path.join(folder_dir, video_name)
        if os.path.isfile(download_path):
            print(f"File '{video_name}' already exists, skipping download.")
            continue

        try:
            response = requests.get(video_url, auth=(username, password), stream=True)
            response.raise_for_status()  # Raise an error for bad responses

            with open(download_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            print(f"Downloaded '{video_name}' to '{download_path}'")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download '{video_name}': {e}")

    print(f"Completed processing folder: {folder_name}")

print("All folders processed successfully.")
