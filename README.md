# Automation 101 for ComfyUI

A collection of professional automation nodes designed to streamline your ComfyUI workflows (prompts, saving, sequencing, and cloud uploads).

## 📂 Nodes Overview

All nodes are located under the **`automation 101`** category in ComfyUI.

### 1. Excel Prompt Loader
**"The Brain"**
- **Purpose**: Reads prompts/data from `.csv` or `.xlsx` files in your `ComfyUI/input` folder.
- **Features**:
    - Supports random, sequential, or fixed indexing.
    - Persistent memory (remembers where it left off).
    - Outputs up to **8 prompts** + File Path + Prefix.
- **Usage**: Connect the strings to your CLIP Text Encoders or Image Savers.

### 2. Index Control
**"The Sequencer"**
- **Purpose**: Advanced counter logic to control *which* row the Excel Loader picks.
- **Features**:
    - **5 Independent Channels**.
    - **Matrix Logic**: Any channel can drive any other channel.
    - **Gear Ratios**: "Wait for Channel 1 to tick 10 times before Channel 2 ticks once."
- **Use Case**: Complex sequential generation (Character X in Outfit Y in Location Z).

### 3. Save Image to Folders
**"The Organizer"**
- **Purpose**: Saves images to exact folder paths.
- **Features**:
    - Accepts `folder_path` and `filename_prefix` inputs (e.g., from Excel).
    - Automatically creates folders if they don't exist.

### 4. Save Text to Folders
- **Purpose**: Saves text data (metadata, prompts) to `.txt` files.
- **Features**: Matches the logic of the Image Saver for perfect pairing.

### 5. Save to Google Drive
**"The Cloud"**
- **Purpose**: Uploads your generations to a specific Google Drive folder and cleans up the local copy.
- **Setup**: Requires `credentials.json` (Service Account) in the node folder.
- **Features**:
    - Uploads to specific `Folder ID`.
    - Returns the web link.
    - Auto-deletes local "temp" file after successful upload.

---

## 🛠️ Installation & Dependencies

1.  **Python Libraries**:
    Run this command in your ComfyUI python environment:
    ```bash
    pip install pandas openpyxl imageio imageio-ffmpeg google-api-python-client google-auth-httplib2 google-auth-oauthlib
    ```

2.  **Google Drive Setup**:
    - Get a Service Account Key from Google Cloud Console.
    - Rename it to `credentials.json`.
    - Place it in: `custom_nodes/ComfyUI-Excel-Iterator/credentials.json`.
    - **Share** your target Drive folder with the Service Account email.

## 🤝 Troubleshooting

- **Node Not Found?** Check your console for "ImportError". You likely miss a library (pandas or google).
- **Drive Upload Fails?** Check `credentials.json` location and ensure the Google Drive folder is **Shared** with the Service Account email.
### 6. Log Uploads (CSV)
- **Purpose**: Creates a local history of all your Google Drive uploads.
- **Inputs**: Connect `drive_url` from the Saver node to this node.
- **Output**: Writes to `upload_log.csv` (Timestamp, Prefix, URL).

### 7. Logic Gate (Trigger)
- **Purpose**: A simple pass-through node.
- **Use Case**: Use it to force a node to wait for another node. Connect an output to `trigger` and it passes it through.

### 8. Auto Queuer (Recursive)
- **Purpose**: Automatically queues a new generation when it runs.
- **⚠️ Warning**: This creates an **Infinite Loop** unless you stop it manually.
- **Use Case**: Continuous generation (creating datasets, testing randomness).

