import time
from classes.application import Application

image_paths = [
    'D:\\_personal_demos_\\_python_projects_\\pikachuProject\\assets\\sample1.png',
            'D:\\_personal_demos_\\_python_projects_\\pikachuProject\\assets\\sample2.png',
            'D:\\_personal_demos_\\_python_projects_\\pikachuProject\\assets\\sample3.png',
            'D:\\_personal_demos_\\_python_projects_\\pikachuProject\\assets\\sample4.png',
            'D:\\_personal_demos_\\_python_projects_\\pikachuProject\\assets\\sample5.png',
            'D:\\_personal_demos_\\_python_projects_\\pikachuProject\\assets\\sample6.png',
            'D:\\_personal_demos_\\_python_projects_\\pikachuProject\\assets\\sample7.png'
]
time.sleep(3)
print("APP STARTED")
app = Application(threshold=0.7, initial_scale=0.8, scale_increment_count=4, image_paths=image_paths, process_id=2404)
app.app_init()
for i in range(500):
    app.app_start()
    time.sleep(0.3)