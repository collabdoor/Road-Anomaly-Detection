
## 1. Create Python Virtual Environment
```bash
# Create a new virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate

```

## 2. Install Required Packages
```bash
# Install PyTorch with CUDA support for GPU acceleration
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

# Install other required packages
pip install ultralytics
pip install opencv-python
pip install supervision
```

## 3. Verify Installation
```python
# Create a test.py file with this code to verify PyTorch GPU setup
import torch
print(f"Is CUDA available: {torch.cuda.is_available()}")
print(f"Current device: {torch.cuda.get_device_name(0)}" if torch.cuda.is_available() else "No CUDA device available")
```