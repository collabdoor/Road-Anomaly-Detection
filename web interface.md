# Road Anomaly Detection Web Interface

A simple Flask web application for detecting road defects using a YOLOv8 model.

## Features

- Upload images for road defect detection
- View detection results with bounding boxes
- See detection details (defect type, confidence)

## Setup Instructions

1. **Clone the repository**

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure your model file is available**

   Make sure your `YOLOv8_Small_RDD.pt` file is in the root directory, or update the `MODEL_PATH` in `app.py` to point to the correct location.

4. **Run the application**

   ```bash
   python app.py
   ```

5. **Access the web interface**

   Open your browser and navigate to http://localhost:5000

## Project Structure

```
.
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── YOLOv8_Small_RDD.pt    # Your trained model file
├── static/
│   ├── css/
│   │   └── style.css      # CSS styles
│   ├── uploads/           # Uploaded images (auto-created)
│   └── results/           # Detection result images (auto-created)
└── templates/
    ├── index.html         # Homepage template
    └── results.html       # Results page template
```

## Usage

1. Open the web interface in your browser
2. Upload a road image using the provided form
3. The system will process the image and display the results
4. View the original image, detected anomalies, and detection details