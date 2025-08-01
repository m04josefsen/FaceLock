# menu_icon.py
from pystray import Icon, Menu as menu, MenuItem as item
from PIL import Image, ImageDraw

def create_image(width, height, color1, color2):
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle((width // 2, 0, width, height // 2), fill=color2)
    dc.rectangle((0, height // 2, width // 2, height), fill=color2)
    return image

def start_tray():
    tray_icon = Icon(
        'FaceLock',
        icon=create_image(64, 64, 'black', 'white'),
        title='FaceLock'
    )
    tray_icon.run()