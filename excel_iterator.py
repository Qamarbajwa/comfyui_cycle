import os
import csv

class ExcelIteratorNode:
    def __init__(self):
        self.cache = {}

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "file_path": ("STRING", {"default": "data.csv"}),
                "index": ("INT", {"default": 0, "min": 0, "max": 999999}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("filename_prefix", "directory", "full_path", "column_1", "column_2", "column_3", "column_4")
    FUNCTION = "do_work"
    CATEGORY = "utils"

    def custom_read_csv(self, file_path):
        data = []
        with open(file_path, 'r', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile)
            # Skip header if present, or just read all. Assuming no header or handle index 0 logic?
            # User request implies specific columns. Let's assume header exists or handle it gracefully.
            # actually usually these ML datasets have headers.
            # But simpler to just read all rows.
            for row in reader:
                if not row: continue # skip empty
                data.append(row)
        return data

    def custom_read_excel(self, file_path):
        import pandas as pd
        df = pd.read_excel(file_path, header=None) # Read without header to get index 0 access easily or match csv
        # Actually standard is usually with header. stick to index access.
        # Let's use pandas for robust excel reading
        return df.values.tolist()

    def do_work(self, file_path, index):
        if not os.path.exists(file_path):
             return ("File not found", "", "", "", "", "", "")

        # Very basic caching based on file mtime could be added, but for now load fresh to be safe
        # Or load and check mtime.
        
        data = []
        if file_path.endswith(".csv"):
            data = self.custom_read_csv(file_path)
        elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
            try:
                data = self.custom_read_excel(file_path)
            except ImportError:
                 raise Exception("Pandas/Openpyxl not installed. Please install 'pandas' and 'openpyxl' to use Excel files, or use CSV.")
        else:
             raise Exception("Unsupported file type")

        total_rows = len(data)
        
        # Auto-stop logic
        if index >= total_rows:
            # Reached end of file
            # Raising an exception stops the ComfyUI execution queue
            raise Exception("Finished processing all rows in file.")

        # Get the row
        row = data[index]
        
        # Pad row if short
        row = [str(x) if x is not None else "" for x in row]
        while len(row) < 7:
            row.append("")

        # 0: ID (ignore)
        # 1: Filename
        # 2: Directory
        # 3: Text 1
        # 4: Text 2
        # 5: Text 3
        # 6: Text 4
        
        filename_prefix = row[1]
        directory = row[2]
        
        # Construct full path
        if directory and filename_prefix:
            full_path = os.path.join(directory, filename_prefix).replace("\\", "/")
        elif filename_prefix:
             full_path = filename_prefix
        else:
             full_path = ""

        col1 = row[3]
        col2 = row[4]
        col3 = row[5]
        col4 = row[6]

        return (filename_prefix, directory, full_path, col1, col2, col3, col4)
