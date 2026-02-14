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
                "skip_existing": ("BOOLEAN", {"default": True}),
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
            for row in reader:
                if not row: continue # skip empty
                data.append(row)
        return data

    def custom_read_excel(self, file_path):
        import pandas as pd
        df = pd.read_excel(file_path, header=None) 
        return df.values.tolist()

    def check_file_exists(self, directory, filename_prefix):
        # Check for common image/video extensions
        extensions = ["png", "jpg", "jpeg", "webp", "mp4", "webm", "gif"]
        if not directory:
            directory = "."
        
        # We need to check if ANY file with this prefix exists.
        # But wait, the Saver adds _0001 counter?
        # The Excel Iterator defines the "Base" prefix. 
        # If "Custom Image Saver" is used, it uses the EXACT filename provided here.
        # If "Media Saver" is used, it appends counters.
        
        # Assumption: If using "Custom Image Saver", the file is exactly {directory}/{filename_prefix}.{ext}
        # If using "Media Saver", we can't easily track it back to this row unless we know the counter.
        
        # Let's assume the user is using "Custom Image Saver" or strictly naming their files as per CSV.
        
        for ext in extensions:
            full_path = os.path.join(directory, f"{filename_prefix}.{ext}")
            if os.path.exists(full_path):
                return True
        return False

    def do_work(self, file_path, index, skip_existing):
        if not os.path.exists(file_path):
             return ("File not found", "", "", "", "", "", "")

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

        # Smart Resume Logic
        effective_index = index
        
        if skip_existing:
            # We need to calculate how many rows are *already done* relative to the requested index.
            # Actually, "skip_existing" usually means "Don't process rows that exist".
            # So we iterate through the data. For each row, check if file exists.
            
            # We want to find the (index)-th MISSING row.
            # Example: Rows 0, 1, 2 exist.
            # Index 0 requested -> Should return Row 3.
            # Index 1 requested -> Should return Row 4.
            
            found_missing_count = -1
            found_row_index = -1
            
            for i in range(total_rows):
                # Parse row to get check params
                row_check = data[i]
                row_check = [str(x) if x is not None else "" for x in row_check]
                while len(row_check) < 3: row_check.append("")
                
                fname = row_check[1]
                dname = row_check[2]
                
                if self.check_file_exists(dname, fname):
                    continue # File exists, skip
                
                # File missing
                found_missing_count += 1
                if found_missing_count == index:
                    found_row_index = i
                    break
            
            if found_row_index != -1:
                effective_index = found_row_index
            else:
                # We ran out of rows while searching
                raise Exception("Finished processing all rows (all valid rows skipped or completed).")
        
        else:
             # Standard behavior
             if index >= total_rows:
                raise Exception("Finished processing all rows in file.")

        # Get the row
        row = data[effective_index]
        
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
