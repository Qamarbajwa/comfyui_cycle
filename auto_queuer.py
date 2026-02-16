import urllib.request
import json
import execution
import server

class AutoQueuer:
    """
    Recursively queues the current workflow when triggered.
    WARNING: Can cause infinite loops if not controlled by a logic gate or specific condition.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "trigger": ("*", {}), # Allow any input (e.g., Image, Latent, etc.)
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO", "unique_id": "UNIQUE_ID"},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("status",)
    FUNCTION = "queue_run"
    CATEGORY = "automation 101"
    OUTPUT_NODE = True

    def queue_run(self, trigger, prompt=None, extra_pnginfo=None, unique_id=None):
        # Even if trigger is None (connection removed), we might technically run if user force runs?
        # But usually we only want to recurse if there is a signal.
        # However, checking 'if trigger' on a Tensor is dangerous.
        # We just assume if the node executed, the trigger signal propagated.
        # But we can add a mode to disable it.
        # For now, let's just proceed.

        # Logic: Re-queue the exact same workflow.
        
        try:
            # Attempt to find the port dynamically
            port = 8188
            if hasattr(server, 'args') and hasattr(server.args, 'port'):
                port = server.args.port
            elif hasattr(server, 'PromptServer') and hasattr(server.PromptServer.instance, 'port'):
                port = server.PromptServer.instance.port
            
            url = f"http://127.0.0.1:{port}/prompt"
            client_id = "0" 
            
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
                response.read() # Consume
                
            print(f"[AutoQueuer] Successfully queued new run on port {port}.")
            return ("Queued New Run",)
            
        except Exception as e:
            print(f"\033[91m[AutoQueuer] Error: {e}\033[0m")
            return (f"Error: {e}",)
