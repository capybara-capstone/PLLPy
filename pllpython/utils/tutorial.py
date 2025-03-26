import os
import requests
import zipfile
import platform
import tempfile

GITHUB_ZIP_URL = "https://github.com/capybara-capstone/PLLPy/raw/refs/heads/main/pllpython_tutorials.zip"

INSTALL_PATH = os.path.expanduser("./")

if platform.system() in ["Linux", "Darwin"]:  # Darwin = macOS
    ZIP_PATH = os.path.join("/tmp", "pllpython_tutorials.zip")
else:
    ZIP_PATH = os.path.join(tempfile.gettempdir(),
                            "pllpython_tutorials.zip")  # Fallback for other OS


def install_tutorial():
    """Download tutorial ZIP from GitHub, extract it, and clean up the ZIP file."""
    print("Downloading tutorial ZIP from GitHub...")

    try:
        response = requests.get(GITHUB_ZIP_URL, stream=True)
        response.raise_for_status()

        if "text/html" in response.headers.get("Content-Type", ""):
            print("Error: Received an HTML page instead of a ZIP file. Check the URL.")
            return

        with open(ZIP_PATH, "wb") as zip_file:
            for chunk in response.iter_content(chunk_size=8192):
                zip_file.write(chunk)

        print("Extracting tutorial files...")

        os.makedirs(INSTALL_PATH, exist_ok=True)

        with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
            for file_info in zip_ref.infolist():
                if "__MACOSX" not in file_info.filename:
                    zip_ref.extract(file_info, INSTALL_PATH)

        print(f"Tutorial installed in: {INSTALL_PATH}")

        os.remove(ZIP_PATH)
        print("Cleaned up temporary ZIP file.")

    except requests.RequestException as e:
        print(f"Error downloading tutorial: {e}")

    except zipfile.BadZipFile:
        print("Error: The downloaded file is not a valid ZIP file. Check the URL.")

    except Exception as e:
        print(f"Unexpected error: {e}")
