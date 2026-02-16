from .excel_iterator import ExcelIteratorNode
from .image_saver import ImageSaverNode
from .text_saver import TextSaverNode
from .multi_index_controller import MultiIndexController
from .gdrive_saver import GoogleDriveSaver
from .gdrive_logger import GoogleDriveLogger
from .trigger_logic import TriggerLogic
from .auto_queuer import AutoQueuer

NODE_CLASS_MAPPINGS = {
    "ExcelIteratorNode": ExcelIteratorNode,
    "ImageSaverNode": ImageSaverNode,
    "TextSaverNode": TextSaverNode,
    "MultiIndexController": MultiIndexController,
    "GoogleDriveSaver": GoogleDriveSaver,
    "GoogleDriveLogger": GoogleDriveLogger,
    "TriggerLogic": TriggerLogic,
    "AutoQueuer": AutoQueuer
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ExcelIteratorNode": "Excel Prompt Loader",
    "ImageSaverNode": "Save image to folders",
    "TextSaverNode": "Save Text to folders",
    "MultiIndexController": "Index Control",
    "GoogleDriveSaver": "Save to Google Drive",
    "GoogleDriveLogger": "Log Uploads (CSV)",
    "TriggerLogic": "Logic Gate (Trigger)",
    "AutoQueuer": "Auto Queuer (Recursive)"
}
