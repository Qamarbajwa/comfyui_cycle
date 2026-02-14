import os
from PIL import Image
import numpy as np
import torch

class ImageSaverNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", ),
                "output_path": ("STRING", {"default": "output"}),
                "filename_prefix": ("STRING", {"default": "image"}),
                "extension": (["png", "jpg", "jpeg", "webp"], ),
            },
        }

    RETURN_TYPES = ("BOOLEAN", )
    RETURN_NAMES = ("completed", )
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "utils"

    def save_images(self, images, output_path, filename_prefix, extension="png"):
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        results = list()
        for i, image in enumerate(images):
            # Convert tensor to PIL
            i_np = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i_np, 0, 255).astype(np.uint8))
            
            # Construct filename
            # If batch > 1, add index. 
            # Actually, user might want strict control. 
            # If they use the Excel Iterator, 'filename_prefix' will be unique per row (batch=1 usually).
            # But let's handle batching safely just in case.
            
            if len(images) > 1:
                filename = f"{filename_prefix}_{i:02d}.{extension}"
            else:
                filename = f"{filename_prefix}.{extension}"
                
            full_path = os.path.join(output_path, filename)
            
            # Save
            if extension == "jpg" or extension == "jpeg":
                img.save(full_path, quality=95)
            else:
                img.save(full_path)
                
            results.append({
                "filename": filename,
                "subfolder": output_path,
                "type": "output"
            })
            
        return { "ui": { "images": results }, "result": (True,) }
