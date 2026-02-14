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

## 3. Development Changelog (Detailed)

### Phase 1: Core Setup
- [x] Check existing custom nodes and python environment (pandas support)
- [x] Create implementation plan for ComfyUI-Excel-Iterator
- [x] Create folder structure custom_nodes/ComfyUI-Excel-Iterator
- [x] Implement excel_node.py (as excel_iterator.py) with CSV/Excel reading logic
- [x] Implement __init__.py to register the node
- [x] Create a requirements.txt if pandas/openpyxl is needed
- [x] Verify the code (static analysis/review)
- [x] Explain usage to user (how to use increment primitive)
- [x] Create README.md documentation
- [x] Initialize Git repository in custom_nodes/ComfyUI-Excel-Iterator
- [x] Commit files to local git
- [x] Ask user for remote repository URL to push

### Phase 2: Saver Implementation
- [x] Analyze existing image save logic (check websocket_image_save.py or similar)
- [x] Create implementation plan for ImageSaverNode
- [x] Implement image_saver.py in custom_nodes/ComfyUI-Excel-Iterator
- [x] Update __init__.py to register ImageSaverNode
- [x] Verify the code
- [x] Update documentation and walkthrough
- [x] Commit and push to Git
- [x] Create implementation plan for MediaSaverNode
- [x] Implement media_saver.py using imageio for video
- [x] Add Counter logic (scan directory or internal state)
- [x] Update __init__.py to register MediaSaverNode
- [x] Update requirements.txt if needed (imageio is standard but check)
- [x] Verify and Document
- [x] Push to Git

### Phase 3: Documentation & Refinement
- [x] Rename package in README "Iteration Package for ComfyUI"
- [x] Update documentation to cover all 3 nodes comprehensively
- [x] Push documentation updates to Git

### Phase 4: Smart Logic (Resume & Header)
- [x] Modify excel_iterator.py to add skip_existing logic
- [x] Update README.md to explain the Resume feature
- [x] Commit and Push changes
- [x] Modify excel_iterator.py to scan input folder (File Picker)
- [x] Implement Dropdown in INPUT_TYPES
- [x] Update documentation to explain "Put files in Input folder"
- [x] Commit and Push
- [x] Update excel_iterator.py to exclude Header row
- [x] Ensure empty row check is robust
- [x] Commit and Push

### Phase 5: Automation & Loops
- [x] Add completed output to MediaSaverNode
- [x] Add completed output to ImageSaverNode
- [x] Update documentation to explain the new outputs
- [x] Commit and Push
- [x] Create developer_guide.md explaining code structure of Saver nodes
- [x] Create trigger_logic.py (Node 1: Feedback Logic)
- [x] Create auto_queuer.py (Node 2: API Caller)
- [x] Register new nodes in __init__.py
- [x] Document usage (Recursive Loop)
- [x] Push to Git

### Phase 6: Project Management
- [x] Create native PROJECT_HISTORY.md file

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
