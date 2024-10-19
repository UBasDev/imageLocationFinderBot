import multiprocessing
import random
import time

import concurrent

import keyboard
from classes.application import Application

image_paths = [
    'D:\\_personal_demos_\\_python_projects_\\pikachuProject\\assets\\sample1.png',
    'D:\\_personal_demos_\\_python_projects_\\pikachuProject\\assets\\sample17.png',
            # 'D:\\_personal_demos_\\_python_projects_\\pikachuProject\\assets\\sample2.png',
            'D:\\_personal_demos_\\_python_projects_\\pikachuProject\\assets\\sample3.png',
            'D:\\_personal_demos_\\_python_projects_\\pikachuProject\\assets\\sample4.png',
            'D:\\_personal_demos_\\_python_projects_\\pikachuProject\\assets\\sample5.png',
            'D:\\_personal_demos_\\_python_projects_\\pikachuProject\\assets\\sample6.png',
            'D:\\_personal_demos_\\_python_projects_\\pikachuProject\\assets\\sample7.png',
            'D:\\_personal_demos_\\_python_projects_\\pikachuProject\\assets\\sample8.png',
            'D:\\_personal_demos_\\_python_projects_\\pikachuProject\\assets\\sample9.png',
            'D:\\_personal_demos_\\_python_projects_\\pikachuProject\\assets\\sample10.png',
            'D:\\_personal_demos_\\_python_projects_\\pikachuProject\\assets\\sample11.png',
            'D:\\_personal_demos_\\_python_projects_\\pikachuProject\\assets\\sample12.png',
            'D:\\_personal_demos_\\_python_projects_\\pikachuProject\\assets\\sample13.png',
            'D:\\_personal_demos_\\_python_projects_\\pikachuProject\\assets\\sample14.png',
            'D:\\_personal_demos_\\_python_projects_\\pikachuProject\\assets\\sample15.png',
            'D:\\_personal_demos_\\_python_projects_\\pikachuProject\\assets\\sample16.png'
]

# Give some time before app starts
time.sleep(1)
print("APP STARTED")

if __name__ == '__main__': # This will only run in the main process
    with multiprocessing.Manager() as manager:
        global_stop_event = multiprocessing.Event()
        
        app = Application(threshold=0.7, initial_scale=1, scale_increment_count=1, image_paths=image_paths, process_id=14672, stop_event= global_stop_event)

        app.app_init()
        app.register_graceful_shutdown()
        app.register_listeners()
        app.switch_to_window()
        
        try:
            for i in range(500):
                app.app_start()
                time.sleep(random.uniform(0.2, 0.5))                    
        except Exception as ex:
            global_stop_event.set()