import os

class TextSaverNode:
    """
    Saves text content to a .txt file in a specified folder.
    Useful for saving prompts alongside images.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
                "folder_path": ("STRING", {"default": "output"}),
                "filename_prefix": ("STRING", {"default": "text_data"}),
            },
        }

    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("saved_paths", )
    FUNCTION = "save_text"
    OUTPUT_NODE = True
    CATEGORY = "automation 101"

    def save_text(self, text, folder_path, filename_prefix):
        # Create directory if it doesn't exist
        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path, exist_ok=True)
            except Exception as e:
                return (f"Error creating directory: {e}", )

        filename = f"{filename_prefix}.txt"
        full_path = os.path.join(folder_path, filename)
        
        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(text)
        except Exception as e:
            return (f"Error writing file: {e}", )
            
        return (full_path, )
