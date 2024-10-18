class ImageToSearch:
    def __init__(self, id: int, image, path: str, image_height: int, image_width: int) -> None:
        self.id = id
        self.image = image
        self.path = path
        self.image_height = image_height
        self.image_width = image_width