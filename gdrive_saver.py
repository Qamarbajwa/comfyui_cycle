import os
import io
import shutil
import numpy as np
from PIL import Image

class GoogleDriveSaver:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", ),
                "folder_id": ("STRING", {"default": "root", "multiline": False}), # Drive Folder ID
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
            },
        }

    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("drive_url", )
    FUNCTION = "save_to_drive"
    OUTPUT_NODE = True
    CATEGORY = "automation 101"

    def save_to_drive(self, images, folder_id, filename_prefix):
        # 1. Verification of Libraries
        try:
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaFileUpload
            from google.oauth2 import service_account
            from google.auth.transport.requests import Request
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
        except ImportError:
            return ("Error: Missing Google Libs. Install: google-api-python-client google-auth-httplib2 google-auth-oauthlib", )

        # 2. Filesystem Setup (Temp)
        temp_dir = "temp_drive_upload"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir, exist_ok=True)

        results = []
        
        # 3. Authenticate
        # We look for 'credentials.json' (Service Account) or 'token.json' (User Auth)
        # Ideally user puts 'service_account.json' in this node's folder.
        
        base_dir = os.path.dirname(os.path.realpath(__file__))
        creds_path = os.path.join(base_dir, "credentials.json") # User provided
        token_path = os.path.join(base_dir, "token.json")
        
        creds = None
        service = None
        
        try:
            # Simple Service Account Logic (Best for automation)
            if os.path.exists(creds_path):
                 # Try Service Account first
                 try:
                    creds = service_account.Credentials.from_service_account_file(
                        creds_path, scopes=['https://www.googleapis.com/auth/drive'])
                 except:
                    # Fallback to OAuth Client ID flow if Service Account fails?
                    # Start simplistic.
                    pass
            
            if not creds:
                 # Standard OAuth flow (token.json)
                 if os.path.exists(token_path):
                     creds = Credentials.from_authorized_user_file(token_path, ['https://www.googleapis.com/auth/drive'])

            if not creds:
                 return ("Error: No credentials.json or token.json found in node folder.", )

            service = build('drive', 'v3', credentials=creds)
            
        except Exception as e:
            return (f"Auth Error: {e}", )

        # 4. Process Images
        for i, image in enumerate(images):
            # Convert to PIL
            i_np = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i_np, 0, 255).astype(np.uint8))
            
            # Save Local Temp
            if len(images) > 1:
                fname = f"{filename_prefix}_{i+1:02d}.png"
            else:
                fname = f"{filename_prefix}.png"
                
            local_path = os.path.join(temp_dir, fname)
            img.save(local_path)
            
            # Upload to Drive
            try:
                file_metadata = {
                    'name': fname,
                    'parents': [folder_id]
                }
                media = MediaFileUpload(local_path, mimetype='image/png', resumable=True)
                file = service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
                
                # Success
                link = file.get('webViewLink', f"Uploaded ID: {file.get('id')}")
                results.append(link)
                
                # Delete Local
                os.remove(local_path)
                
            except Exception as e:
                results.append(f"Upload Failed: {e}")
                # Clean up local anyway?
                if os.path.exists(local_path):
                    os.remove(local_path)

        # Cleanup Temp Dir
        try:
            os.rmdir(temp_dir) # Only if empty
        except:
            pass

        return ("\n".join(results), )
