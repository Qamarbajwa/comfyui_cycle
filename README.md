# Qamar mode for modals (ComfyUI Excel/CSV Iterator)

A custom node for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) that allows you to drive your workflow using data from CSV or Excel files. 

It reads row by row, providing dynamic prompts, filenames, and directory paths for batch generation.

## Features
- **Loop through Data**: Automatically processes each row in your file.
- **Auto-Stop**: Stops the ComfyUI queue when the end of the file is reached.
- **CSV & Excel Support**: Native CSV support. Excel (`.xlsx`) support via `pandas` and `openpyxl`.
- **Dynamic Filenames**: Uses a specific column for filenames and directories.
- **Multiple Text Outputs**: Supports up to 4 separate text columns for prompted fields.

## Installation

1.  Clone this repository into your `ComfyUI/custom_nodes/` directory:
    ```bash
    cd ComfyUI/custom_nodes
    git clone https://github.com/yourusername/ComfyUI-Excel-Iterator.git
    ```
2.  Install dependencies (only needed for Excel .xlsx support):
    ```bash
    pip install -r requirements.txt
    ```
    *Note: CSV files work without extra dependencies.*

## data.csv Format

Your data file **MUST** follow this column structure (headers are recommended but column order is strict):

| Col Index | Name | Description |
| :--- | :--- | :--- |
| 1 | **ID** | Ignored. Use for numbering rows. |
| 2 | **Filename** | The filename prefix for saving images. |
| 3 | **Directory** | Subfolder path for saving images. |
| 4 | **Text 1** | First text output (e.g. Positive Prompt). |
| 5 | **Text 2** | Second text output (e.g. Style). |
| 6 | **Text 3** | Third text output. |
| 7 | **Text 4** | Fourth text output. |

### Example CSV
```csv
id,filename,directory,positive,style,negative,extra
1,girl_01,output/portraits,A beautiful girl,cyberpunk,ugly,8k
2,car_01,output/vehicles,A red sports car,realistic,blurry,4k
```

## Usage

1.  **Add Node**: Search for "Qamar mode for modals".
2.  **Select File**: Enter the absolute or relative path to your `.csv` or `.xlsx` file.
3.  **Connect Index (IMPORTANT)**:
    *   Right-click `index` -> *Convert to Input*.
    *   Add a **Primitive** node and connect it to `index`.
    *   **Right-click the Primitive node** (or use the panel) and set **Control_after_generate** to **"Increment"**.
    *   *This is required to make the node loop through rows.*
4.  **Connect Outputs**:
    *   `filename_prefix` -> Connect to Save Image node.
    *   `full_path` -> Connect to Save Image node (combines directory/filename).
    *   `column_1` to `column_4` -> Connect to your CLIP Text Encode nodes.
5.  **Run**: Set your **Batch Count** (Queue Prompt -> Batch Count) to the number of rows (or higher). The node will error and stop automatically when finished.
