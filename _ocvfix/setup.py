"""Local helper package: force opencv-python-headless after all deps are installed.

retina-face depends on opencv-python (full), which needs GUI system libs (libGL)
not present in a headless CI/container image. Both opencv variants share the cv2/
package dir and the full one wins, so 'import cv2' fails. This package's setup()
removes the full variant and force-reinstalls the headless one. Installed as a
path dependency (last) from requirements.txt so it runs after the other deps.
"""
import os
import subprocess
import sys

if os.environ.get("SKIP_OCV_HEADLESS_FIX") != "1":
    for cmd in (
        [sys.executable, "-m", "pip", "uninstall", "-y", "opencv-python"],
        [sys.executable, "-m", "pip", "install", "--force-reinstall", "--no-deps",
         "opencv-python-headless==4.10.0.84"],
    ):
        try:
            subprocess.check_call(cmd)
        except Exception as e:
            print(f"[ocvfix] {cmd} failed: {e}")

from setuptools import setup
setup(name="_ocvfix", version="0.0.0", py_modules=[], description="force opencv headless")
