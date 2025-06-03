import os
import json

from dotenv import load_dotenv

CHUNK_SIZE = 65536

agent_directory = "/home/stanislav_soldatov/kanal75/agent"
cwd = "/home/stanislav_soldatov/kanal75/k75downloader"

report_txt_file = os.path.join(cwd, "report.txt")

download_dir = os.path.join(agent_directory, "downloads")
print(f"Download directory: {download_dir}")
os.makedirs(download_dir, exist_ok=True)

folders_json = os.path.join(cwd, "folders.json")

if not os.path.isfile(folders_json):
    raise FileNotFoundError(f"JSON file '{folders_json}' not found.")

with open(folders_json, "r") as file:
    json_data = json.load(file)[0]

folders = json_data.get("Folder", [])
if not folders:
    raise ValueError("No folders found in the JSON file.")

print(f"Found {len(folders)} folders in the JSON file.")

env_file = os.path.join(cwd, "local.env")
if not os.path.isfile(env_file):
    raise FileNotFoundError(f"Environment file '{env_file}' not found.")

load_dotenv(env_file)

USERNAME = os.getenv("DL_USERNAME")
PASSWORD = os.getenv("DL_PASSWORD")

print(f"Username {USERNAME}, password {len(PASSWORD) * '*'}.")
