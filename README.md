# K75 Downloader

This script is used to download the video files from client storage used the provided credentials.

# How to use

1. Clone the repository:

```bash
git clone https://github.com/supervisely-ecosystem/k75downloader.git
```

2. Create a virtual environment and install the dependencies:

```bash
cd k75downloader
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
pip install -r requirements.txt
```

3. Create a `local.env` file with the following content:

```env
DL_USERNAME="***********" # Insert correct username.
DL_PASSWORD="***********" # Insert correct password.
```

4. Put the `folders.json` file which contains the list of folders and files.

5. Run the script:

```bash
python main.py
```

# Output

The video files will be downloaded to the `downloads` directory, maintaining the folder structure from the `folders.json` file.

# How to launch detached process

If you need to connect to the remote machine via SSH and run the script in the background, you can use the following command:

```bash
nohup /home/stanislav_soldatov/kanal75/k75downloader/.venv/bin/python /home/stanislav_soldatov/kanal75/k75downloader/main.py > output.log 2>&1 &
```

Replace the path to the Python interpreter and the script with your actual paths.

To check the output, you can use:

```bash
tail -f output.log
```