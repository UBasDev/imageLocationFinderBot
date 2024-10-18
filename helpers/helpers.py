from datetime import datetime
import uuid
import cv2

def save_screenshot_to_local(screenshot_np):
    current_date = datetime.now().strftime("%Y_%m_%d")  # Format: YYYY_MM_DD
    random_guid = str(uuid.uuid4())  # Generate a random GUID
    screenshot_file_path = f"D:\\_personal_demos_\\_python_projects_\\AIProject4\\SS_{current_date}_{random_guid}.png"

    cv2.imwrite(screenshot_file_path, screenshot_np)
    print(f"Screenshot saved as {screenshot_file_path}.")