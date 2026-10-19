from pathlib import Path

from PIL import Image, ImageTk

images = []
def process(image_path: Path, size: int) -> ImageTk.PhotoImage:
    global images
    x = Image.open(image_path).resize((size, size))
    images.append(ImageTk.PhotoImage(x))
    return images[-1]