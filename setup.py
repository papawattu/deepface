import json
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().split("\n")

with open("package_info.json", "r", encoding="utf-8") as f:
    package_info = json.load(f)


# --- Buildpacks/CI opencv fix (post-install) -------------------------------------
# retina-face depends on `opencv-python` (full), which needs GUI system libs (libGL)
# that a headless CI/container image does not have. We want the headless variant
# (opencv-python-headless) which bundles its own libs and needs no GUI deps. Both
# packages write to the shared `cv2/` package dir, and the full one wins by default,
# so `import cv2` fails with "libGL.so.1 not found". After the deps are installed we
# remove the full variant and force-reinstall the headless one so only headless cv2
# remains. Runs as a no-op when full opencv isn't present (e.g. local dev with a
# display). Safe to call repeatedly.
import os
import subprocess
import sys


def _fix_opencv_headless():
    try:
        if os.environ.get("SKIP_OCV_HEADLESS_FIX") == "1":
            return
        # Best-effort; never fail the install if the opencv surgery is impossible.
        for cmd in (
            [sys.executable, "-m", "pip", "uninstall", "-y", "opencv-python"],
            [sys.executable, "-m", "pip", "install", "--force-reinstall", "--no-deps", "opencv-python-headless==4.10.0.84"],
        ):
            try:
                subprocess.check_call(cmd)
            except Exception as e:  # pragma: no cover - best effort
                print(f"[opencv-fix] {cmd} failed: {e}")
    except Exception as e:  # pragma: no cover
        print(f"[opencv-fix] skipped: {e}")


_fix_opencv_headless()
# --------------------------------------------------------------------------------------

setuptools.setup(
    name="deepface",
    version=package_info["version"],
    author="Sefik Ilkin Serengil",
    author_email="serengil@gmail.com",
    description=(
        "A Lightweight Face Recognition and Facial Attribute Analysis Framework"
        " (Age, Gender, Emotion, Race) for Python"
    ),
    data_files=[("", ["README.md", "requirements.txt", "package_info.json"])],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/serengil/deepface",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": ["deepface = deepface.DeepFace:cli"],
    },
    python_requires=">=3.7",
    license="MIT",
    install_requires=requirements,
)
