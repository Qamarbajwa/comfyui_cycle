import os
import random

class ExcelIteratorNode: # Keeping class name for compatibility with __init__ mapping, but logic is new
    """
    Excel/CSV Loader node that handles specific prompt columns and indexing logic.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        input_dir = "input"
        try:
            import folder_paths
            input_dir = folder_paths.get_input_directory()
        except ImportError:
            # Fallback if folder_paths not found (unlikely in ComfyUI)
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
            input_dir = os.path.join(base_dir, "input")

        files = []
        if os.path.exists(input_dir):
            files = [f for f in os.listdir(input_dir) if f.endswith(".csv") or f.endswith(".xlsx") or f.endswith(".xls")]
        
        if not files:
            files = ["put_files_in_input_folder.csv"]

        return {
            "required": {
                "file_path": (sorted(files), ),
                "mode": (["fixed", "increment", "decrement", "random"],),
                "index": ("INT", {"default": 0, "min": 0, "max": 100000}),
            },
           "optional": {
                "trigger": ("*", {}), # To force update if needed
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("file_path", "prefix", "prompt_1", "prompt_2", "prompt_3", "prompt_4", "prompt_5", "prompt_6", "prompt_7", "prompt_8")
    FUNCTION = "load_data"
    CATEGORY = "automation 101"

    # Global state to track index across executions
    # We use a dictionary to separate state by file_path or unique_id if we had it.
    # Since we don't have unique_id in do_work easily without hidden inputs, 
    # we'll map by file_path.
    _STATE = {}

    @classmethod
    def IS_CHANGED(s, **kwargs):
        # Force re-execution so increment/random works
        return float("NaN")

    def load_data(self, file_path, mode, index, trigger=None):
        # 0. Resolve File Path (Handle relative paths to ComfyUI/input if needed)
        # The user requested "Type or paste path".
        # We will try to be smart: if it doesn't exist, check 'input' folder.
        
        target_path = file_path
        if not os.path.exists(target_path):
             # Try input folder
            try:
                import folder_paths
                input_dir = folder_paths.get_input_directory()
                potential_path = os.path.join(input_dir, file_path)
                if os.path.exists(potential_path):
                    target_path = potential_path
            except ImportError:
                pass
        
        if not os.path.exists(target_path):
             return ("File Not Found", "Error", "Error", "Error", "Error", "Error", "Error", "Error", "Error", "Error")

        # 1. Load the file
        data = []
        try:
            if target_path.endswith('.csv'):
                 import csv
                 with open(target_path, 'r', newline='', encoding='utf-8-sig') as f:
                     reader = csv.reader(f)
                     data = list(reader)
            elif target_path.endswith('.xlsx') or target_path.endswith('.xls'):
                 try:
                    import pandas as pd
                    df = pd.read_excel(target_path, header=None)
                    # Convert to list of lists, treating NaN as empty string
                    data = df.fillna("").values.tolist()
                 except ImportError:
                     return ("Error: Install pandas", "Error", "Error", "Error", "Error", "Error", "Error", "Error", "Error", "Error")
            else:
                 return ("Unsupported Extension", "Error", "Error", "Error", "Error", "Error", "Error", "Error", "Error", "Error")
        except Exception as e:
            return (f"Error: {e}", "Error", "Error", "Error", "Error", "Error", "Error", "Error", "Error", "Error")

        # Remove Empty Rows? User didn't explicitly ask, but it's good practice.
        # Let's keep it raw as per "grab raw data" instruction unless it breaks.
        # Check if list is empty
        if not data:
             return ("Empty File", "", "", "", "", "", "", "", "", "")

        # Skip header logic?
        # User blueprint says "df.read_csv", which usually takes header=0 by default.
        # But prompts.csv might have "path, prefix..." header.
        # If we just grab row[0], we might get the header.
        # Let's assume Row 1 (Index 0) is DATA. If user has header, they should account for it or we skip row 0?
        # The user's code: "row = df.iloc[target_idx]" implies 0-based index on the DATAFRAME.
        # pd.read_csv uses row 0 as header by default.
        # So df.iloc[0] is actually the *second* line of the file.
        # We should simulate that behavior if we use CSV module.
        
        # If using CSV module, row 0 is header.
        # If using Pandas, headers are stripped.
        # Let's standardize: We want the DATA rows.
        
        # If we used the manual CSV read above, data includes header.
        # We should probably attempt to detect header or just strip row 0 if it looks like keys.
        # Safest: Use Pandas for CSV too if available, to match user's explicit request usage.
        
        # Let's switch to Pandas for CSV too if possible, falling back to CSV module.
        # Actually, user explicitly gave code with `pd.read_csv`.
        
        df = None
        try:
            import pandas as pd
            if target_path.endswith('.csv'):
                df = pd.read_csv(target_path)
            else:
                df = pd.read_excel(target_path)
        except ImportError:
             # Fallback for CSV if pandas missing
             if target_path.endswith('.csv'):
                  import csv
                  with open(target_path, 'r', newline='', encoding='utf-8-sig') as f:
                       # DictReader? Or standard reader and skip header?
                       # User code uses positional iloc. So standard reader.
                       reader = csv.reader(f)
                       raw_data = list(reader)
                       if len(raw_data) > 1:
                            # Create simplified DF-like object
                            headers = raw_data[0]
                            rows = raw_data[1:]
                            # We need simple index access.
                            data = rows
                       else:
                            data = []
             else:
                  return ("Error: Install pandas", "", "", "", "", "", "", "", "", "")
        
        # If we have a dataframe
        if df is not None:
             # Clean NaNs
             df = df.fillna("")
             max_rows = len(df)
        else:
             max_rows = len(data)

        if max_rows == 0:
             return ("Empty Data", "", "", "", "", "", "", "", "", "")

        # 2. Handle Index Logic
        # We use strict state management
        
        state_key = target_path
        
        # Initialize internal state if not present
        if state_key not in self._STATE:
             self._STATE[state_key] = 0
             
        current_internal_index = self._STATE[state_key]
        
        target_idx = 0
        
        if mode == "fixed":
            # Just use the input widget value
            target_idx = index
        elif mode == "increment":
            # Use internal state
            # If we are "running", we should increment.
            # But IS_CHANGED runs before this? 
            # We increment AFTER using it? Or before?
            # User code: target_idx = current % max; current += 1
            
            target_idx = current_internal_index % max_rows
            self._STATE[state_key] += 1
            
        elif mode == "decrement":
            target_idx = current_internal_index % max_rows
            self._STATE[state_key] -= 1
        else: # random
             # User code: random.randint
             target_idx = random.randint(0, max_rows - 1)
             
        # Wrap the final target_idx for fixed/safety
        target_idx = target_idx % max_rows
             
        # 3. Extract Row Data
        # We need Columns A, B, C, D, E (0, 1, 2, 3, 4)
        
        if df is not None:
             row = df.iloc[target_idx]
             # Convert to list to handle varying lengths safely if we can
             row_values = row.values.tolist()
        else:
             row_values = data[target_idx]
             
        # Pad row to 10 columns
        row_values = [str(x) for x in row_values]
        while len(row_values) < 10:
             row_values.append("")
             
        return (
            str(row_values[0]), # Cell A: File Path
            str(row_values[1]), # Cell B: Prefix
            str(row_values[2]), # Cell C: Prompt 1
            str(row_values[3]), # Cell D: Prompt 2
            str(row_values[4]), # Cell E: Prompt 3
            str(row_values[5]), # Cell F: Prompt 4
            str(row_values[6]), # Cell G: Prompt 5
            str(row_values[7]), # Cell H: Prompt 6
            str(row_values[8]), # Cell I: Prompt 7
            str(row_values[9]), # Cell J: Prompt 8
        )
