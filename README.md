# Iteration Package for ComfyUI

A comprehensive custom node package for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) focused on **iterative workflows** and **advanced file saving**.

This package allows you to drive your workflow using data from CSV/Excel files and save the results (Images or Videos) with perfect file management.

## Included Nodes

### 1. Excel/CSV Iterator
Reads data row-by-row from a `.csv` or `.xlsx` file.
- **Dynamic Prompts**: Outputs up to 4 text columns for use in CLIP Text Encode.
- **File Management**: Outputs a `filename_prefix` and `directory` for each row.
- **Auto-Stop**: Automatically stops the ComfyUI queue when the end of the file is reached.
- **Header Skip**: Automatically skips the first row (Header). Data starts from Row 2.
- **Smart Resume**: Optional `skip_existing` mode checks if the output file already exists and skips that row. Perfect for resuming crashed batches.

### 2. Custom Image Saver
A streamlined image saver that works perfectly with the Iterator.
- **Exact Filenames**: Saves images using the exact filename provided by the Iterator.
- **Custom Paths**: Saves to any directory specified by the Iterator.
- **Format Control**: Supports PNG, JPG, JPEG, WEBP.
- **Output Hook**: Outputs a `completed` (Boolean) signal when saving is done. Useful for custom logic or sequential triggering.

### 3. Media File Saver (Image/Video)
An advanced saver for more complex needs.
- **Video Support**: Combines a batch of images into a single video file (`.mp4`, `.webm`, `.gif`).
- **Auto-Counter**: Automatically finds the next available file number (e.g. `file_0001.mp4` -> `file_0002.mp4`) to prevent overwriting.
- **Multi-Mode**: Switch easily between saving individual images or compiled videos.
- **Output Hook**: Outputs a `completed` (Boolean) signal.

### 4. Logic Gate (Trigger)
- **Input**: Takes a `completed` signal from a Saver node.
- **Output**: Splits the signal into a `trigger` (for the Auto Queuer) and a `count_input`.

### 5. Auto Queuer (Recursive)
- **Use with Caution**: This node automatically triggers the **Queue Prompt** button again when executed.
- **Recursive Loop**: Creates an infinite loop of generation until the Iterator stops it (via End of File error).
- **Setup**: Connect `trigger` from Logic Gate -> `trigger` on Auto Queuer.

## Installation

1.  Clone this repository into your `ComfyUI/custom_nodes/` directory:
    ```bash
    cd ComfyUI/custom_nodes
    git clone https://github.com/Qamarbajwa/comfyui_cycle.git
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage Guide

### Step 1: Prepare Data
Create a `data.csv` with the following columns:
1.  **ID** (Ignored)
2.  **Filename** (e.g. `my_render`)
3.  **Directory** (e.g. `output/project_alpha`)
4.  **Text 1** (Positive Prompt)
5.  **Text 2** (Style/Negative)
6.  **Text 3**
7.  **Text 4**

### Step 2: The Workflow
1.  **Prepare Data**: Put your `.csv` or `.xlsx` file in the **`ComfyUI/input`** folder.
2.  Add **"Excel/CSV Iterator"**.
    - **csv_file**: Select your file from the dropdown list.
    - **manual_path** (Optional): Use this if your file is elsewhere (e.g. `D:/Prompts/data.csv`).
3.  **Connect Index (IMPORTANT)**:
    *   Right-click `index` -> *Convert to Input*.
    *   Add a **Primitive** node and connect it to `index`.
    *   **Right-click the Primitive node** (or use the panel) and set **Control_after_generate** to **"Increment"**.
    *   **Skip Existing**: Set `skip_existing` to **True** (default). This checks your `directory` for the `filename` and skips the row if the file is already there.
4.  **Saving**:
    - **For Images**: Connect `directory` and `filename_prefix` to the **Custom Image Saver**.
    - **For Video**: Connect them to the **Media File Saver**, select `save_video` mode, and choose `.mp4`.

### Step 3: Run
Set your Queue **Batch Count** to a high number (e.g. 100). The iterator will run one row per batch and stop automatically when done.
