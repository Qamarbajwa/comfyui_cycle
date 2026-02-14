from .excel_iterator import ExcelIteratorNode
from .image_saver import ImageSaverNode
from .media_saver import MediaSaverNode

NODE_CLASS_MAPPINGS = {
    "ExcelIteratorNode": ExcelIteratorNode,
    "ImageSaverNode": ImageSaverNode,
    "MediaSaverNode": MediaSaverNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ExcelIteratorNode": "Excel/CSV Iterator",
    "ImageSaverNode": "Custom Image Saver",
    "MediaSaverNode": "Media File Saver (Image/Video)"
}
