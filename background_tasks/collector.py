import random
import time
from multiprocessing.synchronize import Event

import keyboard


def collector_background_task(stop_event: Event) -> None:    
    # Give some time before job starts
    time.sleep(3)
    while not stop_event.is_set():
        time.sleep(random.uniform(0.5, 1))
        
        keyboard.press_and_release('"')
        print("COLLECTED")
    exit(0)
#     try:
#         print("COLLECTED STARTED")
#         file = open("D:\\_personal_demos_\\_python_projects_\\pikachuProject\\background_log.txt", "a")
#         file.write("COLLECTED STARTED")
        
#         if(stop_event.is_set()):
#             file.write("COLLECTED AVAILABE")
#         else:
#             file.write("COLLECTED UNAVAIABLE")
        
#         # Give some time before job starts
#         time.sleep(3)
#         while not stop_event.is_set():
#             time.sleep(random.uniform(0.5, 2))
#             # keyboard.press('"')

#             # time.sleep(0.1)
#             # keyboard.release('"')
#             file.write("COLLECTED\n")
#             print("COLLECTED")

#         file.close()
#         print("COLLECTOR EXIT")
#     except Exception as ex:
#         file = open("D:\\_personal_demos_\\_python_projects_\\pikachuProject\\background_log.txt", "a")
#         file.write("EXCEPTION\n")
#         file.write(ex)
#         file.close()
#         print("COLLECTOR EXCEPTION")