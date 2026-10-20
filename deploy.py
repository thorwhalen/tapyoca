"""Manual build-and-upload helper. Importing this module has no side effects.

Run it explicitly (``python deploy.py``) to build and upload to PyPI.
"""

import shutil
import subprocess
import sys
from pathlib import Path

BUILD_COMMAND = (sys.executable, "setup.py", "sdist", "bdist_wheel")
DIST_DIR = Path("dist")
UPLOAD_COMMAND = (sys.executable, "-m", "twine", "upload", "dist/*")


def main():
    # TODO: Both of these are python. Change to use python objects directly.
    # Stale files left in dist/ would be uploaded alongside (or instead of) the new build.
    shutil.rmtree(DIST_DIR, ignore_errors=True)

    print("--------------------------- setup_output ---------------------------")
    subprocess.run(BUILD_COMMAND, check=True)

    print("--------------------------- upload_output ---------------------------")
    subprocess.run(UPLOAD_COMMAND, check=True)


if __name__ == "__main__":
    main()
