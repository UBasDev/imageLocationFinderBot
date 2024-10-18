import time
import keyboard
import pyautogui
import cv2
import numpy as np

from classes.image_to_search import ImageToSearch
from helpers.helpers import save_screenshot_to_local

import pygetwindow as gw
import pywinauto

class Application:
    def __init__(self, threshold: float, initial_scale: float, scale_increment_count: int, image_paths: list[str], process_id: int) -> None:
        self.screenshot_np = None
        self.images_paths_to_search: list[str] = image_paths
        self.images_to_search: list[ImageToSearch] = []
        self.is_image_found: bool = False
        self.threshold: float = threshold
        self.initial_scale: float = initial_scale
        self.scale: float = self.initial_scale
        self.scale_increment_count: int = scale_increment_count
        self.process_id: int = process_id
        
    def app_init(self) -> None:
        self.upload_files_to_memory()
    
    def upload_files_to_memory(self):
        for current_index, current_path in enumerate(self.images_paths_to_search):
            self.is_image_found = False
    
            # Step 2: Load the small hat image using OpenCV
            # searched_image = cv2.imread('D:\\_personal_demos_\\_python_projects_\\AIProject4\\sample3.png', cv2.IMREAD_COLOR)  # Searched image with its original colors
            searched_image = cv2.imread(current_path, cv2.IMREAD_GRAYSCALE)  # Searched image as grayscale
            
            if searched_image is None:
                print("Error: Could not load the searched image.")
                exit(1)  # Exit the program if the image cannot be loaded

            # Step 2.1: Get the dimensions of the searched image
            searched_image_height, searched_image_width = searched_image.shape[:2]  # shape returns (height, width, channels)
            print(f"Searched image dimensions: Width = {searched_image_width}, Height = {searched_image_height}")

            self.images_to_search.append(ImageToSearch(current_index, searched_image, current_path, searched_image_height, searched_image_width))
            
    def app_start(self) -> None:
        self.take_screenshot_and_save()
        self.start_matching_images()
            
    def take_screenshot_and_save(self) -> None:
        # Step 1: Take a screenshot
        screenshot = pyautogui.screenshot()
        
        # Convert the screenshot to a numpy array (which OpenCV can process)
        self.screenshot_np = np.array(screenshot)

        # Convert the image to BGR format (required for OpenCV since screenshot is in RGB)
        # screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR) # Screenshot image with its original colors
        self.screenshot_np = cv2.cvtColor(self.screenshot_np, cv2.COLOR_RGB2GRAY) # Screenshot image as grayscale
            
    def start_matching_images(self) -> None:
        for current_index, current_image in enumerate(self.images_to_search):
            self.match_images_based_on_scales(searched_image= current_image.image, searched_image_height= current_image.image_height, searched_image_width=current_image.image_width)
            
            if(self.is_image_found is True): # Görseli zaten bulduysa diğer assetleri kontrol etmesine gerek kalmadı
                break
    
    def match_images_based_on_scales(self, searched_image, searched_image_height, searched_image_width):
        # Set a threshold to decide if the image exists (higher values mean a better match)
        self.scale = self.initial_scale
        
        for _ in range(0, self.scale_increment_count):
            resized_searched_image = cv2.resize(searched_image, None, fx=self.scale, fy=self.scale)
            
            result = cv2.matchTemplate(self.screenshot_np, resized_searched_image, cv2.TM_CCOEFF_NORMED)
    
            locations = np.where(result >= self.threshold)
    
            # Step 4: Check if any matches were found
            if len(locations[0]) > 0:
                print(f"Searched image found in the screenshot with {self.scale} scale!")
                self.is_image_found = True
    
                self.get_coordinates_from_found_location(*locations[::-1], searched_image_height= searched_image_height, searched_image_width= searched_image_width)
                
                break # İlk bulduğu anda scale loopundan çıkıyoruz çünkü diğer scaleleri kontrol etmesine gerek kalmadı
            else:
                print(f"Searched image NOT found in the screenshot with {self.scale} scale.")
    
            self.scale = round(self.scale + 0.1, 1)

    def get_coordinates_from_found_location(self, *locations, searched_image_height, searched_image_width):
        for pt in zip(*locations):  # Switch columns and rows
            
            x, y = int(pt[0]), int(pt[1])
            # Calculate corners
            top_left = (x, y)
            top_right = (x + searched_image_width, y)
            bottom_left = (x, y + searched_image_height)
            bottom_right = (x + searched_image_width, y + searched_image_height)
            # Calculate center
            center = (x + searched_image_width // 2, y + searched_image_height // 2)
            # Print coordinates
            print(f"Top-left corner: {top_left}")
            print(f"Top-right corner: {top_right}")
            print(f"Bottom-left corner: {bottom_left}")
            print(f"Bottom-right corner: {bottom_right}")
            print(f"Center: {center}")
            
            # save_screenshot_to_local(resized_searched_image)
            
            # Move the cursor to the center of the matched area
            app = pywinauto.Application().connect(process= self.process_id)
            
            # Get the list of windows belonging to that application
            windows = gw.getWindowsWithTitle(app.top_window().element_info.name)
            
            if windows:
                # Bring the first window to the foreground
                windows[0].activate()
                
                # keyboard.release('space')
                
                print(f"Switched to the app with PID {self.process_id} successfully.")
                
                time.sleep(0.1)
                pyautogui.moveTo(center[0], center[1])
                
                time.sleep(0.1)
                pyautogui.click()
                
                time.sleep(0.1)
                pyautogui.click()
                
                time.sleep(0.1)
                pyautogui.mouseDown(button='right')
                
                time.sleep(0.1)
                pyautogui.moveTo(center[0] + 100, center[1], duration=0.2)
                
                time.sleep(0.1)
                pyautogui.mouseUp(button='right')
                
                # time.sleep(0.1)
                # keyboard.press('space')
                
                print(f"Cursor moved to the center of the matched image at {center}.")
            else:
                print(f"No window found for PID: {self.process_id}.")
            
            break # Ilk bulduğu locationda location loopundan çıkıyoruz çünkü diğer locationları kontrol etmesine gerek kalmadı