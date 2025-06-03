import requests
from tqdm import tqdm
from typing import Tuple, List, Dict, Any
import os

from datetime import datetime
from config import (
    download_dir,
    USERNAME,
    PASSWORD,
    CHUNK_SIZE,
    report_txt_file,
    folders,
)


def is_downloaded(
    file_path: str, remote_size: int, remove_incomplete: bool = True
) -> bool:
    """Check if the file is already downloaded and matches the remote size.
    If the file exists but the size does not match, it will delete the local file if
    `remove_incomplete` is True.

    :param file_path: Path to the local file.
    :type file_path: str
    :param remote_size: Expected size of the remote file in bytes.
    :type remote_size: int
    :param remove_incomplete: Whether to remove the local file if it exists but size does not match.
    :type remove_incomplete: bool
    :return: True if the file is already downloaded and matches the remote size, False otherwise.
    :rtype: bool
    """
    if os.path.isfile(file_path):
        local_size = os.path.getsize(file_path)
        if local_size == remote_size:
            return True
        else:
            print(
                f"File {file_path} exists but size mismatch. "
                f"Local {local_size / (1024 * 1024):.2f} MB, "
                f"Remote {remote_size / (1024 * 1024):.2f} MB. Will delete the local file."
            )
            if remove_incomplete:
                os.remove(file_path)
    return False


def download_file(
    download_url: str, file_name: str, download_path: str, auth: Tuple[str, str]
) -> bool:
    """Download a file from a given URL with basic authentication.

    :param download_url: URL to download the file from.
    :type download_url: str
    :param file_name: Name of the file to save locally.
    :type file_name: str
    :param download_path: Local path where the file will be saved.
    :type download_path: str
    :param auth: Tuple containing username and password for basic authentication.
    :type auth: Tuple[str, str]
    :return: True if the file was downloaded successfully, False otherwise.
    :rtype: bool
    """
    username, password = auth
    response = requests.get(download_url, auth=(username, password), stream=True)
    response.raise_for_status()
    if response.status_code != 200:
        print(
            f"Failed to access URL: {download_url} with status code {response.status_code}."
        )
        return False
    remote_total_size = int(response.headers.get("content-length", 0))
    if is_downloaded(download_path, remote_total_size):
        print(f"File {file_name} already downloaded and verified. Skipping.")
        return True

    try:
        with open(download_path, "wb") as file, tqdm(
            total=remote_total_size,
            unit="B",
            unit_scale=True,
            desc=file_name,
            leave=False,
        ) as progress_bar:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    file.write(chunk)
                    progress_bar.update(len(chunk))

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        video_size = os.path.getsize(download_path)
        with open(report_txt_file, "a") as report_file:
            report_file.write(
                f"{timestamp} | {file_name} | {round(video_size / (1024 * 1024), 2)} MB"
                f"| {download_path}\n"
            )

        return True

    except requests.exceptions.RequestException as e:
        print(f"Failed to download {file_name}: {e}")
        return False


def download_folders(folders: List[Dict[str, Any]]):
    """Iterates over JSON-structured folder data from the API and downloads each video file.

    :param folders: List of folders with video data.
    :type folders: List[Dict[str, Any]]
    """
    for folder in folders:
        folder_name = folder.get("Name")
        folder_dir = os.path.join(download_dir, folder_name)
        os.makedirs(folder_dir, exist_ok=True)

        folder_files = folder.get("File", [])

        for folder_file in tqdm(
            folder_files, desc=f"Downloading files from {folder_name}"
        ):
            video_data = folder_file.get("Data", {})
            video_name = video_data["General"]["Name"]
            video_url = video_data["Url"]["Download"]

            download_path = os.path.join(folder_dir, video_name)

            if not download_file(
                video_url, video_name, download_path, (USERNAME, PASSWORD)
            ):
                print(f"Failed to download {video_name} from {video_url}.")


if __name__ == "__main__":
    try:
        download_folders(folders)
        print("All downloads completed successfully.")
    except Exception as e:
        print(f"An error occurred during the download process: {e}")
