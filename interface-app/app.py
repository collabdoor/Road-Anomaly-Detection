from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_from_directory,
)
import cv2
import os
import time
import uuid
from pathlib import Path
import numpy as np
from werkzeug.utils import secure_filename

# Import your model code
from ultralytics import YOLO
import supervision as sv

app = Flask(__name__)
app.secret_key = "road_defect_detection_secret_key"
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["RESULT_FOLDER"] = "static/results"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max upload size
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg"}

# Ensure directories exist
for folder in [app.config["UPLOAD_FOLDER"], app.config["RESULT_FOLDER"]]:
    os.makedirs(folder, exist_ok=True)

# Load model
MODEL_PATH = r"..\RoadDetectionModel\RoadModel_yolov8m.pt_rounds120_b9\weights\best.pt"  # Use raw string or fix path separators
CONF_THRESHOLD = 0.35

try:
    model = YOLO(
        r"..\RoadDetectionModel\RoadModel_yolov8m.pt_rounds120_b9\weights\best.pt" # Use raw string or fix path separators
    )
    class_names = model.model.names if hasattr(model, "model") else model.names
    print(f"Model loaded successfully! Classes: {class_names}")
except Exception as e:
    print(f"Failed to load model: {e}")
    model = None

# Initialize annotators
box_annotator = sv.BoxAnnotator(thickness=2)
label_annotator = sv.LabelAnnotator(
    text_thickness=1, text_scale=0.6, text_color=sv.Color.BLACK, text_padding=2
)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


def process_image(image_path):
    """Process an image and return the annotated image and detection info"""
    try:
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            return None, None, "Failed to read image"

        # Run inference
        results = model.predict(image, conf=CONF_THRESHOLD, verbose=False)[0]
        detections = sv.Detections.from_ultralytics(results)

        # Create labels
        labels = [
            f"{class_names[class_id]} {confidence:.2f}"
            for class_id, confidence in zip(detections.class_id, detections.confidence)
        ]

        # Annotate image
        annotated_frame = image.copy()
        annotated_frame = box_annotator.annotate(
            scene=annotated_frame, detections=detections
        )
        annotated_frame = label_annotator.annotate(
            scene=annotated_frame, detections=detections, labels=labels
        )

        # Extract detection details for display
        detection_info = []
        for i, (class_id, conf) in enumerate(
            zip(detections.class_id, detections.confidence)
        ):
            detection_info.append(
                {
                    "id": i + 1,
                    "class": class_names[class_id],
                    "confidence": f"{conf:.2f}",
                }
            )

        # Save annotated image
        result_filename = f"result_{uuid.uuid4().hex}.jpg"
        result_path = os.path.join(app.config["RESULT_FOLDER"], result_filename)
        cv2.imwrite(result_path, annotated_frame)

        return result_filename, detection_info, None

    except Exception as e:
        import traceback

        traceback.print_exc()
        return None, None, f"Error processing image: {str(e)}"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)

    file = request.files["file"]

    if file.filename == "":
        flash("No selected file")
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        # Process the image
        result_filename, detection_info, error = process_image(file_path)

        if error:
            flash(error)
            return redirect(url_for("index"))

        # Return results page
        return render_template(
            "results.html",
            original=filename,
            result=result_filename,
            detections=detection_info,
        )

    flash("Invalid file type. Please upload an image (PNG, JPG, JPEG)")
    return redirect(url_for("index"))


@app.route("/static/<path:path>")
def serve_static(path):
    return send_from_directory("static", path)


if __name__ == "__main__":
    # Check if model loaded correctly
    if model is None:
        print("WARNING: Model failed to load. Application may not work correctly.")

    # Run Flask app
    app.run(debug=True, host="0.0.0.0", port=5000)
