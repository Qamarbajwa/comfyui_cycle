from .excel_iterator import ExcelIteratorNode
from .image_saver import ImageSaverNode
from .media_saver import MediaSaverNode
from .trigger_logic import TriggerLogic
from .auto_queuer import AutoQueuer

NODE_CLASS_MAPPINGS = {
    "ExcelIteratorNode": ExcelIteratorNode,
    "ImageSaverNode": ImageSaverNode,
    "MediaSaverNode": MediaSaverNode,
    "TriggerLogic": TriggerLogic,
    "AutoQueuer": AutoQueuer
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ExcelIteratorNode": "Excel/CSV Iterator",
    "ImageSaverNode": "Custom Image Saver",
    "MediaSaverNode": "Media File Saver (Image/Video)",
    "TriggerLogic": "Logic Gate (Trigger)",
    "AutoQueuer": "Auto Queuer (Recursive)"
}
