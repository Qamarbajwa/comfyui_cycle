# Project History: ComfyUI Excel Iterator & Automation Package

This document serves as a reference for all tasks performed and features implemented in this project.

## 1. Project Objective
To create a robust system for driving ComfyUI workflows using external data (CSV/Excel) and automating the saving/looping process.

## 2. Nodes Created

### A. Core Logic
- **`Excel/CSV Iterator`** (`excel_iterator.py`)
    - **Function**: Reads rows from `.csv` or `.xlsx` files.
    - **Features**: 
        - **File Picker**: Scans `ComfyUI/input` folder for files.
        - **Header Skip**: Automatically skips the first row (Header).
        - **Smart Resume**: Checks output folder to skip already processed rows (based on filename).
        - **Auto-Stop**: Stops execution when data is exhausted.

### B. Saving / Output
- **`Custom Image Saver`** (`image_saver.py`)
    - **Function**: Saves images exactly as named by the Iterator.
    - **Features**: Creates directories, supports multiple formats (PNG/JPG/WEBP), outputs a `completed` signal.
- **`Media File Saver`** (`media_saver.py`)
    - **Function**: Generates Videos (MP4/GIF) from image batches.
    - **Features**: Auto-incrementing counter, ffmpeg integration.

### C. Logic & Looping (Advanced)
- **`Logic Gate (Trigger)`** (`trigger_logic.py`)
    - **Function**: Takes a signal and passes it through to control flow.
- **`Auto Queuer (Recursive)`** (`auto_queuer.py`)
    - **Function**: Automatically triggers the "Queue Prompt" API to restart the workflow for the next row.

## 3. Development Changelog

### Phase 1: Basic Structure
- [x] Initialized Git repository.
- [x] Implemented `ExcelIteratorNode` with Pandas/OpenPyXL support.
- [x] Created `README.md`.

### Phase 2: Saving Improvements
- [x] Added `ImageSaverNode` for strict filename control.
- [x] Added `MediaSaverNode` for video creation.

### Phase 3: Smart Logic
- [x] **Smart Resume**: Added logic to check for existing files and skip processing for them.
- [x] **Sequential Output**: Added `completed` boolean output to Saver nodes.

### Phase 4: Feedback Loops
- [x] Created `TriggerLogic` and `AutoQueuer` to allow infinite looping without manual batch count setting.

### Phase 5: Usability
- [x] **File Picker**: Replaced manual path entry with a dropdown scanning `ComfyUI/input`.
- [x] **Row Logic**: Enforced "Skip Header" (Row 1) and "Filter Empty Rows" to ensure clean data processing.

## 4. File Structure
```
custom_nodes/ComfyUI-Excel-Iterator/
├── __init__.py          # Node Registration
├── excel_iterator.py    # Main Data Logic
├── image_saver.py       # Image Saving Logic
├── media_saver.py       # Video Saving Logic
├── trigger_logic.py     # Flow Control
├── auto_queuer.py       # API Automation
├── README.md            # User Manual
├── PROJECT_HISTORY.md   # This File
└── requirements.txt     # Dependencies (pandas, openpyxl, etc.)
```
