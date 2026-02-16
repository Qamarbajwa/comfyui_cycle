import os
from PIL import Image
import numpy as np

class ImageSaverNode:
    """
    Saves images to a specified folder with a prefix.
    Supports overrides via inputs for flexible automation.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", ),
                "folder_path": ("STRING", {"default": "output"}),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
            },
            "optional": {
                "folder_path_override": ("STRING", {"forceInput": True}),
                "filename_prefix_override": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("saved_paths", )
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "automation 101"

    def save_images(self, images, folder_path, filename_prefix, folder_path_override=None, filename_prefix_override=None):
        # Prefer connected inputs if valid
        if folder_path_override and isinstance(folder_path_override, str) and folder_path_override.strip():
            folder_path = folder_path_override
        
        if filename_prefix_override and isinstance(filename_prefix_override, str) and filename_prefix_override.strip():
            filename_prefix = filename_prefix_override

        # Create directory if it doesn't exist
        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path, exist_ok=True)
            except Exception as e:
                return (f"Error creating directory: {e}", )

        results = []
        for i, image in enumerate(images):
            # Convert tensor to PIL
            i_np = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i_np, 0, 255).astype(np.uint8))
            
            # Construct filename
            if len(images) > 1:
                filename = f"{filename_prefix}_{i+1:02d}.png"
            else:
                filename = f"{filename_prefix}.png"
                
            full_path = os.path.join(folder_path, filename)
            
            img.save(full_path)
            results.append(full_path)
            
        return ("\n".join(results), )
