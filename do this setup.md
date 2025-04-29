
## 1. Create Python Virtual Environment  Or use Anaconda Environment to run this locally
```bash
# Create a new virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate

```
# to deactivate (venv) type

```bash
deactivate
```

# or

## Create a anaconda

```bash
# Create a new conda environment with Python
conda create -n yolo_env python =3.10

# Activate the conda environment
conda activate yolo_env
```


## 2. Install Required Packages Use reqirements.txt
```bash
# Install PyTorch with CUDA support for GPU acceleration
pip3 install -r requirements.txt      

```

## 3. Verify Installation
```python
# Create a test.py file with this code to verify PyTorch GPU setup
import torch
print(f"Is CUDA available: {torch.cuda.is_available()}")
print(f"Current device: {torch.cuda.get_device_name(0)}" if torch.cuda.is_available() else "No CUDA device available")
```