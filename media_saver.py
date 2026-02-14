import os
from PIL import Image
import numpy as np
import torch
import imageio
import re

class MediaSaverNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", ),
                "filename_prefix": ("STRING", {"default": "media"}),
                "output_path": ("STRING", {"default": "output"}),
                "mode": (["save_image", "save_video"], ),
                "extension": (["png", "jpg", "jpeg", "webp", "mp4", "webm", "gif"], ),
                "fps": ("INT", {"default": 24, "min": 1, "max": 120}),
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "save_media"
    OUTPUT_NODE = True
    CATEGORY = "utils"

    def get_next_counter(self, output_path, prefix, extension):
        # Scan directory for files matching prefix_XXXX.ext
        if not os.path.exists(output_path):
            return 1
            
        pattern = re.compile(f"^{re.escape(prefix)}_(\d{{4,}}).{re.escape(extension)}$")
        max_counter = 0
        
        for filename in os.listdir(output_path):
            match = pattern.match(filename)
            if match:
                counter = int(match.group(1))
                if counter > max_counter:
                    max_counter = counter
                    
        return max_counter + 1

    def save_media(self, images, filename_prefix, output_path, mode, extension, fps=24):
        if not os.path.exists(output_path):
            os.makedirs(output_path, exist_ok=True)

        counter = self.get_next_counter(output_path, filename_prefix, extension)
        filename_base = f"{filename_prefix}_{counter:04d}"
        full_path = os.path.join(output_path, f"{filename_base}.{extension}")

        results = list()

        if mode == "save_image":
            # Save each image in batch
            for i, image in enumerate(images):
                i_np = 255. * image.cpu().numpy()
                img = Image.fromarray(np.clip(i_np, 0, 255).astype(np.uint8))
                
                # If batch > 1, append index to filename
                if len(images) > 1:
                    current_filename = f"{filename_base}_{i:02d}.{extension}"
                else:
                    current_filename = f"{filename_base}.{extension}"
                
                save_path = os.path.join(output_path, current_filename)
                
                # Format handling
                if extension in ["jpg", "jpeg"]:
                    img = img.convert("RGB") # Remove alpha for jpg
                    img.save(save_path, quality=95)
                else:
                    img.save(save_path)
                    
                results.append({
                    "filename": current_filename,
                    "subfolder": output_path,
                    "type": "output"
                })

        elif mode == "save_video":
            # Combine images into video
            frames = []
            for image in images:
                i_np = 255. * image.cpu().numpy()
                img = np.clip(i_np, 0, 255).astype(np.uint8)
                frames.append(img)
            
            try:
                if extension == "gif":
                    imageio.mimsave(full_path, frames, duration=(1000/fps), loop=0)
                elif extension in ["mp4", "webm"]:
                    # quality=9 is high quality for imageio (0-10)
                    imageio.mimsave(full_path, frames, fps=fps, quality=9)
                else:
                    # Fallback or error? defaulting to gif-like animation if png/webp selected for video mode?
                    # Actually webp supports animation
                    if extension == "webp":
                         imageio.mimsave(full_path, frames, duration=(1000/fps), loop=0)
                    else:
                         raise Exception(f"Video mode not supported for extension: {extension}")
                         
                results.append({
                    "filename": f"{filename_base}.{extension}",
                    "subfolder": output_path,
                    "type": "output"
                })
            except Exception as e:
                raise Exception(f"Error saving video: {e}. Ensure ffmpeg is installed for mp4/webm.")

        return { "ui": { "images": results } }
