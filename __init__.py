from .excel_iterator import ExcelIteratorNode
from .image_saver import ImageSaverNode

NODE_CLASS_MAPPINGS = {
    "ExcelIteratorNode": ExcelIteratorNode,
    "ImageSaverNode": ImageSaverNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ExcelIteratorNode": "Excel/CSV Iterator",
    "ImageSaverNode": "Custom Image Saver"
}
