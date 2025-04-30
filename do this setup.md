# Project Setup: Road Anomaly Detection

## 1. Prerequisites

*   Python 3.9+ & pip
*   Git


## 2. Create & Activate Virtual Environment

```bash
# Create venv
python -m venv venv

```
# Activate

```bash
# macOS/Linux:
source venv/bin/activate
# Windows:     
venv\Scripts\activate

```

# *(Conda users: `conda create -n yolo_env python=3.10 && conda activate yolo_env`)*

## 3. Install Dependencies

# If you have GPU run this, then requirements.txt

```bash
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
```

```bash
# Installs everything, including CPU PyTorch (or GPU if detected & compatible)
pip install -r requirements.txt
```

*   **(Local GPU Only):** If you *need* a specific CUDA version locally, install PyTorch first from [pytorch.org](https://pytorch.org/get-started/locally/), *then* run `pip install -r requirements.txt`.

# 4. Verify Installation(optional)
```code
# Create a test.py file with this code to verify PyTorch GPU setup

import torch
print(f"Is CUDA available: {torch.cuda.is_available()}")
print(f"Current device: {torch.cuda.get_device_name(0)}" if torch.cuda.is_available() else "No CUDA device available")

```
## 5. Run the App

```bash
streamlit run main.py 
```

---

**Notes:**

*   Deactivate environment: `deactivate` (venv) or `conda deactivate` (conda).