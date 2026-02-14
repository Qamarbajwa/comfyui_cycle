import urllib.request
import json
import execution
import server

class AutoQueuer:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "trigger": ("BOOLEAN", {"default": False}),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO", "unique_id": "UNIQUE_ID"},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("status",)
    FUNCTION = "queue_run"
    CATEGORY = "utils"
    OUTPUT_NODE = True

    def queue_run(self, trigger, prompt=None, extra_pnginfo=None, unique_id=None):
        if not trigger:
            return ("Skipped",)

        # Logic: Re-queue the exact same workflow.
        # ComfyUI's 'prompt' input contains the executing workflow (api format).
        # We just post it back to /prompt.
        
        try:
            # The 'prompt' object contains the node inputs.
            # We need to ensure we don't create an infinite loop immediately in the SAME execution tick.
            # This node runs at the END (Output Node).
            # So the queue happens, ComfyUI handles it as a NEW job.
            
            prompt_id = "requeue_" + str(unique_id)
            
            # Prepare payload
            # We use localhost:8188 by default. 
            # Note: This might fail if user changed port. 
            # But getting port programmatically is hard without checking args.
            
            url = "http://127.0.0.1:8188/prompt"
            client_id = "0" # Default client ID? Or extract?
            
            # We assume standard API format
            payload = {
                "prompt": prompt,
                "client_id": client_id 
            }
            
            if extra_pnginfo:
                payload["extra_data"] = {"extra_pnginfo": extra_pnginfo}

            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
            
            # Send request
            with urllib.request.urlopen(req) as response:
                response_data = response.read()
                
            return ("Queued New Run",)
            
        except Exception as e:
            print(f"AutoQueuer Error: {e}")
            return (f"Error: {e}",)
