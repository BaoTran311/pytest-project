import os
import subprocess
import time

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.consts import PROJECT_ROOT
from src.utils import logger

# VIDEO_NAME = f"{PROJECT_ROOT}/test_video.mp4"
#
#
# @pytest.fixture(scope="function", autouse=True)
# def record_video():
#     # Remove old video if it exists
#     if os.path.exists(VIDEO_NAME):
#         os.remove(VIDEO_NAME)
#
#     # FFmpeg command to record macOS screen
#     ffmpeg_cmd = [
#         "ffmpeg",
#         "-y",  # Overwrite existing file
#         "-f", "avfoundation",  # macOS screen capture input
#         "-framerate", "15",
#         "-i", "1:none",  # Screen index 1, no audio
#         "-preset", "ultrafast",
#         VIDEO_NAME
#     ]
#
#     print("[Recording started]")
#     process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     time.sleep(2)  # Let FFmpeg warm up
#
#     yield  # <-- Your test runs here
#
#     print("[Stopping recording]")
#     process.terminate()
#     stdout, stderr = process.communicate()
#
#     # Optional: debug output if something fails
#     # if not os.path.exists(VIDEO_NAME):
#     #     print("❌ Video file was not created.")
#     #     print("FFmpeg stderr:\n", stderr.decode())
#     # else:
#     #     print(f"✅ Video saved: {VIDEO_NAME}")
#     #     # Attach to Allure
#     #     with open(VIDEO_NAME, "rb") as f:
#     #         allure.attach(body=f.read(), name="Test Recording", attachment_type=allure.attachment_type.MP4)


def test_example():
    options = Options()
    options.add_argument("--start-fullscreen")
    driver = webdriver.Chrome(options=options)
    logger.info("Steps : Navigate to google")
    driver.get("https://www.google.com/")
    time.sleep(5)
    driver.quit()
