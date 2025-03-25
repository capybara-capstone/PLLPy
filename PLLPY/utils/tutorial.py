import os
import requests

GITHUB_FILE_URL = "https://raw.githubusercontent.com/capybara-capstone/PLLPy/refs/heads/main/run_sim.py"

INSTALL_PATH = os.path.expanduser("./pllpy_tutorial")
TUTORIAL_FILENAME = "run_sim.py"


def install_tutorial():
    """Download the tutorial file from GitHub and save it locally."""
    os.makedirs(INSTALL_PATH, exist_ok=True)
    tutorial_path = os.path.join(INSTALL_PATH, TUTORIAL_FILENAME)

    print("Downloading tutorial file from GitHub...")
    try:
        response = requests.get(GITHUB_FILE_URL, stream=True)
        response.raise_for_status()

        with open(tutorial_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Tutorial installed at: {tutorial_path}")

    except requests.RequestException as e:
        print(f"Error downloading tutorial: {e}")
