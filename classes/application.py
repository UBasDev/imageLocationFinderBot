import atexit
import concurrent.futures
import math
from multiprocessing.synchronize import Event
import signal
import time
import concurrent
from typing import Any
import keyboard
import pyautogui
import cv2
import numpy as np
from classes.image_to_search import ImageToSearch
from constants.constants import POTION_USE_COUNT_AFTER_REVIVED
from graceful_shutdown.graceful_shutdown_cleaners import cleanup, signal_handler
from helpers.helpers import save_screenshot_to_local

import pygetwindow as gw
import pywinauto

class Application:
    def __init__(self, threshold: float, initial_scale: float, scale_increment_count: int, image_paths: list[str], process_id: int, stop_event: Event) -> None:
        self.screenshot_np = None
        self.images_paths_to_search: list[str] = image_paths
        self.images_to_search: list[ImageToSearch] = []
        self.is_image_found: bool = False
        self.threshold: float = threshold
        self.initial_scale: float = initial_scale
        self.scale: float = self.initial_scale
        self.scale_increment_count: int = scale_increment_count
        self.process_id: int = process_id
        self.click_shortest_to_center_coord: tuple[int, int] = tuple[0, 0]
        self.stop_event: Event = stop_event
        self.selected_window: Any = None
        
    def app_init(self) -> None:
        self.upload_files_to_memory()
    
    def register_graceful_shutdown(self) -> None:
        # Register cleanup and signal handlers
        atexit.register(lambda: cleanup(self.stop_event))  # Register cleanup function to be called at exit
        signal.signal(signal.SIGINT, lambda sig, frame: signal_handler(sig, frame, self.stop_event))  # Handle Ctrl+C
        signal.signal(signal.SIGTERM, lambda sig, frame: signal_handler(sig, frame, self.stop_event))  # Handle termination signal
    
    def upload_files_to_memory(self):
        for current_index, current_path in enumerate(self.images_paths_to_search):
    
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
    
    def start_background_tasks(self) -> None:
        pass
        # Schedule tasks as parallel with different CPUs
        # with concurrent.futures.ProcessPoolExecutor(max_workers=1) as executor:
        #     executor.submit(collector_background_task, self.stop_event)
    
    def register_listeners(self) -> None:
        pass
            
    def switch_to_window(self) -> None:
        # Move the cursor to the center of the matched area
        app = pywinauto.Application().connect(process= self.process_id)
        
        # Get the list of windows belonging to that application
        selected_window = gw.getWindowsWithTitle(app.top_window().element_info.name)
        
        # Bring the first window to the foreground
        selected_window[0].activate()
        
        print(f"Switched to the app with PID {self.process_id} successfully.")
        
        self.selected_window = selected_window[0]
        
        # TODO keyboard.press('x')
            
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
        self.is_image_found = False
        for current_index, current_image in enumerate(self.images_to_search):
            self.match_images_based_on_scales(searched_image= current_image.image, searched_image_height= current_image.image_height, searched_image_width=current_image.image_width, searched_image_index= current_index)
            
            if(self.is_image_found is True): # Görseli zaten bulduysa diğer assetleri kontrol etmesine gerek kalmadı
                break
    
    def match_images_based_on_scales(self, searched_image, searched_image_height: int, searched_image_width: int, searched_image_index: int):
        # Set a threshold to decide if the image exists (higher values mean a better match)
        self.scale = self.initial_scale
        
        for _ in range(0, self.scale_increment_count):
            resized_searched_image = cv2.resize(searched_image, None, fx=self.scale, fy=self.scale)
            
            result = cv2.matchTemplate(self.screenshot_np, resized_searched_image, cv2.TM_CCOEFF_NORMED)
    
            locations = np.where(result >= self.threshold)
    
            # Step 4: Check if any matches were found
            if len(locations[0]) > 0:
                self.is_image_found = True
                
                print(f"Searched image found in the screenshot with {self.scale} scale!")
    
                self.get_coordinates_from_found_location(*locations[::-1], searched_image_height= searched_image_height, searched_image_width= searched_image_width, searched_image_index= searched_image_index)
                
                break # İlk bulduğu anda scale loopundan çıkıyoruz çünkü diğer scaleleri kontrol etmesine gerek kalmadı
            else:
                print(f"Searched {searched_image_index+1}. image NOT found in the screenshot with {self.scale} scale.")
    
            self.scale = round(self.scale + 0.1, 1)

    def get_coordinates_from_found_location(self, *locations, searched_image_height: int, searched_image_width: int, searched_image_index: int):
        
        self.get_closest_coordinate_to_center(*locations, searched_image_height= searched_image_height, searched_image_width= searched_image_width)
        
        if self.selected_window != None:
            # keyboard.release('space')
            
            if searched_image_index == 0: # If character is dead
                self.bot_action_when_character_is_dead()
                
            elif searched_image_index == 1: # If character is alive and focused on target
                self.bot_action_when_character_is_alive_and_focused()
                    
            else: # If character is alive and but not focused
                self.bot_action_when_character_is_alive_and_not_focused()
                
            time.sleep(0.1)
            keyboard.press_and_release('2') # Use poison skill
            
            time.sleep(0.1)
            keyboard.press_and_release('e')
            
            print(f"Cursor moved to the center of the matched image at {self.click_shortest_to_center_coord}.")
        else:
            print(f"No window found for PID: {self.process_id}.")
    
    def bot_action_when_character_is_dead(self):
        pyautogui.moveTo(self.click_shortest_to_center_coord[0], self.click_shortest_to_center_coord[1])
                
        time.sleep(0.1)
        pyautogui.moveRel(20, 0, duration=0.1)
        
        time.sleep(0.1)
        pyautogui.click() # Clicking to revive
        
        for _ in range(POTION_USE_COUNT_AFTER_REVIVED): # Use potions
            time.sleep(0.1)
            keyboard.press_and_release('1')
        
        time.sleep(2) #Rest some to heal up
    
    def bot_action_when_character_is_alive_and_focused(self):
        for _ in range(1):
            time.sleep(0.1)
            keyboard.press_and_release('space')
    
    def bot_action_when_character_is_alive_and_not_focused(self):
        pyautogui.moveTo(self.click_shortest_to_center_coord[0], self.click_shortest_to_center_coord[1])
                
        time.sleep(0.1)
        pyautogui.click()
    
    def get_closest_coordinate_to_center(self, *locations, searched_image_height: int, searched_image_width: int):
        target_x_coord: int = 960
        target_y_coord: int = 560
        found_shortest_distance: int = 0
        for pt in zip(*locations):
            x: int = int(pt[0])
            y: int = int(pt[1])
            # Calculate center
            center: tuple[int, int] = (x + searched_image_width // 2, y + searched_image_height // 2)
            
            current_found_distance: int = int(math.sqrt((center[0] - target_x_coord)**2 + (center[1] - target_y_coord)**2))
            
            if(found_shortest_distance > current_found_distance or found_shortest_distance == 0):
                found_shortest_distance = current_found_distance
                self.click_shortest_to_center_coord = center
                
            