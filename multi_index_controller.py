import random

class MultiIndexController:
    """
    Five-channel sequential counter with matrix logic.
    Allows indexes to drive each other (cascading/gear logic) or run independently.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        # Define choices
        modes = ["fixed", "increment", "decrement", "random"]
        drivers_base = ["System"]
        
        inputs = {
            "required": {},
            "optional": {} # We can put things here if needed, but we'll put all in required for UI stability
        }
        
        # Helper to generate inputs for 5 indexes
        for i in range(1, 6):
            # Driver options: System + other indexes
            # We allow picking any, even self (though self-driving is weird, maybe useful for "run every time I change?" - effectively System)
            drivers = drivers_base + [f"Index {j}" for j in range(1, 6) if j != i]
            
            inputs["required"][f"index_{i}_mode"] = (modes, {"default": "increment"})
            inputs["required"][f"index_{i}_start"] = ("INT", {"default": 0, "min": 0, "max": 999999})
            inputs["required"][f"index_{i}_min"] = ("INT", {"default": 0, "min": 0, "max": 999999})
            inputs["required"][f"index_{i}_max"] = ("INT", {"default": 10, "min": 0, "max": 999999})
            inputs["required"][f"index_{i}_driver"] = (drivers, {"default": "System" if i==1 else f"Index {i-1}"})
            inputs["required"][f"index_{i}_threshold"] = ("INT", {"default": 1, "min": 1, "max": 9999})

        # Add a reset trigger?
        inputs["optional"] = {"reset_trigger": ("*", {})}
            
        return inputs

    RETURN_TYPES = ("INT", "INT", "INT", "INT", "INT", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("index_1", "index_2", "index_3", "index_4", "index_5", 
                    "index_1_str", "index_2_str", "index_3_str", "index_4_str", "index_5_str")
    FUNCTION = "do_work"
    CATEGORY = "automation 101"

    _STATE = {}

    @classmethod
    def IS_CHANGED(s, **kwargs):
        # Always run to handle "System" ticks
        return float("NaN")

    def do_work(self, **kwargs):
        # Unique ID for state? We don't have one easily. 
        # We'll rely on a singleton/global state for this node class instance usage.
        # Limitation: If user puts 2 of these nodes, they might share state if we don't differentiate.
        # But `id(self)` changes every run? No, `self` is instantiated once per run in Comfy? 
        # Actually Comfy instantiates a new object potentially. 
        # We need a persistent key. 
        # For now, we assume one "global" state or key by arguments hash? 
        # Hash is bad because args change.
        # Let's use a single global state "default" for now, or try to be smart.
        # User requested "Create A Control", singular. 
        
        # Initialize State
        if "values" not in self._STATE:
            self._STATE["values"] = {} # Map '1'->val
            self._STATE["counters"] = {} # Map '1'->ticks
        
        # Reset Logic
        reset = False
        # If we had a reset input we'd check it.
        
        # We track "did_change" for this run to handle casing
        did_change = {} # '1': True/False
        
        current_values = {}
        
        # Process 1 to 5
        for i in range(1, 6):
            mode = kwargs.get(f"index_{i}_mode")
            start = kwargs.get(f"index_{i}_start")
            min_v = kwargs.get(f"index_{i}_min")
            max_v = kwargs.get(f"index_{i}_max")
            driver = kwargs.get(f"index_{i}_driver")
            threshold = kwargs.get(f"index_{i}_threshold", 1)
            
            # State Keys
            val_key = f"v_{i}"
            count_key = f"c_{i}"
            
            # Init Check
            if val_key not in self._STATE["values"]:
                self._STATE["values"][val_key] = start
                self._STATE["counters"][count_key] = 0
                
            current_val = self._STATE["values"][val_key]
            current_count = self._STATE["counters"][count_key]
            
            # 1. Check Driver
            driver_ticked = False
            if driver == "System":
                driver_ticked = True
            else:
                # "Index N"
                try:
                    driver_idx = int(driver.split(" ")[1])
                    # Check if upstream index changed *this run*
                    # If upstream (e.g. 1 driving 2), we know `did_change` status.
                    # If downstream (e.g. 5 driving 1), we look at... we can't look at future.
                    # We accept 1-frame latency for downstream drivers.
                    # Actually, if we want downstream driving, we needed `did_change` from LAST run?
                    # But `did_change` isn't persisted. 
                    # Let's rely on "Order of Operations" (1->5).
                    if driver_idx in did_change:
                        driver_ticked = did_change[driver_idx]
                    else:
                        # Driver hasn't run this frame yet (downstream loop).
                        # Effectively False for this frame.
                        driver_ticked = False 
                except:
                    driver_ticked = False
            
            # 2. Update Threshold Counter
            should_update = False
            if driver_ticked:
                self._STATE["counters"][count_key] += 1
                if self._STATE["counters"][count_key] >= threshold:
                    should_update = True
                    self._STATE["counters"][count_key] = 0 # Reset counter
            
            # 3. Update Value
            new_val = current_val
            
            if should_update:
                if mode == "fixed":
                    new_val = start # Or stay current? Usually "Fixed" means reset to start? Or just don't move? 
                    # User said "increment decrement fixed random". 
                    # Fixed usually means "Manual" or "Constant". Let's assume matches Start.
                    new_val = start
                elif mode == "increment":
                    new_val += 1
                    if new_val > max_v: new_val = min_v
                elif mode == "decrement":
                    new_val -= 1
                    if new_val < min_v: new_val = max_v
                elif mode == "random":
                    new_val = random.randint(min_v, max_v)
            
            # 4. Save & mark change
            if new_val != current_val:
                did_change[i] = True
            else:
                # Even if value didn't change (e.g. fixed -> fixed, or max reached?), 
                # strictly speaking, did the "event" happen?
                # "Index X changes" usually implies value change. 
                # So False.
                did_change[i] = False
                
            self._STATE["values"][val_key] = new_val
            current_values[i] = new_val
            
            
        # Return all
        return (
            current_values[1], current_values[2], current_values[3], current_values[4], current_values[5],
            str(current_values[1]), str(current_values[2]), str(current_values[3]), str(current_values[4]), str(current_values[5])
        )
