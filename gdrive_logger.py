import os
import datetime

class GoogleDriveLogger:
    """
    Logs Google Drive upload details (URL, Time, Prefix) to a local CSV file.
    Useful for keeping a record of generated assets.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "drive_url": ("STRING", {"forceInput": True}), # Connect from GoogleDriveSaver
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
                "log_path": ("STRING", {"default": "upload_log.csv"}),
            },
        }

    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("log_entry", )
    FUNCTION = "log_upload"
    OUTPUT_NODE = True
    CATEGORY = "automation 101"

    def log_upload(self, drive_url, filename_prefix, log_path):
        # 1. Get Timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 2. Format Log Entry
        # CSV Format: Timestamp, Prefix, URL
        entry = f"{timestamp},{filename_prefix},{drive_url}"
        
        # 3. Write to File
        # Handle relative path
        if not os.path.isabs(log_path):
            # Default to node folder or output? 
            # Let's default to ComfyUI base or output folder to be visible.
            # But users might want it in the node folder.
            # Let's use the 'output' folder if possible, or just relative to CWD (Comfy root).
            pass
            
        try:
            # Check if file exists to add header
            file_exists = os.path.exists(log_path)
            
            with open(log_path, "a", encoding="utf-8") as f:
                if not file_exists:
                    f.write("Timestamp,Filename Prefix,Google Drive URL\n")
                f.write(f"{entry}\n")
                
        except Exception as e:
            return (f"Error logging: {e}", )

        return (entry, )
