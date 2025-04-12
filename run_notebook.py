import os
import json
from kaggle import api

# Set up kaggle API credentials
os.makedirs(os.path.expanduser("~/.kaggle"), exist_ok=True)
with open(os.path.expanduser("~/.kaggle/kaggle.json"), "w") as f:
    f.write(os.environ["KAGGLE_JSON"])
os.chmod(os.path.expanduser("~/.kaggle/kaggle.json"), 0o600)

# Push notebook to Kaggle and run it
NOTEBOOK_FILE = "selenium_on_kaggle.ipynb"
NOTEBOOK_TITLE = "Selenium On Kaggle Daily Run"
NOTEBOOK_SLUG = "selenium-on-kaggle-daily-run"
NOTEBOOK_KERNEL_REF = f"{os.environ['KAGGLE_USERNAME']}/{NOTEBOOK_SLUG}"

# Construct metadata
metadata = {
    "id": NOTEBOOK_KERNEL_REF,
    "title": NOTEBOOK_TITLE,
    "code_file": NOTEBOOK_FILE,
    "language": "python",
    "kernel_type": "notebook",
    "is_private": True
}

with open("kernel-metadata.json", "w") as f:
    json.dump(metadata, f)

# Push and run
api.kernels_push_kernel()
api.kernels_pull(NOTEBOOK_KERNEL_REF, path=".")
api.kernels_output(NOTEBOOK_KERNEL_REF)
