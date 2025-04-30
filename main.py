import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
import supervision as sv
import tempfile
import os

# Configuration
MODEL_PATHS = {
    "M1 (Model 1)": "./RoadDetectionModel/RoadModel_yolov8m.pt_rounds120_b9/weights/best.pt",
    "M2 (Model 2)": "./YOLOv8_Small_2nd_Model.pt",
}
MODEL_PREFIX = {
    "M1 (Model 1)": "M1",
    "M2 (Model 2)": "M2",
}
DEFAULT_CONF = {"M1 (Model 1)": 0.35, "M2 (Model 2)": 0.40}
DEFAULT_CAMERA_IDX = 0


@st.cache_resource
def load_yolo_model(path: str):
    try:
        model = YOLO(path)
        return model, model.names
    except Exception as e:
        st.error(f"Failed to load model at {path}: {e}")
        return None, {}


# Annotator Factory
def make_annotators(color: sv.Color):
    box = sv.BoxAnnotator(thickness=2, color=color)
    label = sv.LabelAnnotator(
        text_thickness=1,
        text_scale=0.5,
        color=sv.Color.WHITE,
        text_color=sv.Color.BLACK,
        text_padding=2,
    )
    return box, label


# Frame Processing
def process_frame(
    frame: np.ndarray, models: dict[str, tuple], thresholds: dict[str, float]
) -> np.ndarray:
    out = frame.copy()
    for name, (model, names_map, box_ann, label_ann) in models.items():
        res = model.predict(frame, conf=thresholds[name], verbose=False)[0]
        dets = sv.Detections.from_ultralytics(res)
        labels = [
            f"{MODEL_PREFIX[name]}:{names_map.get(c, str(c))} {conf:.2f}"
            for c, conf in zip(dets.class_id, dets.confidence)
        ]
        out = box_ann.annotate(out, dets)
        out = label_ann.annotate(out, dets, labels=labels)
    return out


# Input Mode Handlers


def show_image(img: np.ndarray, placeholder):
    placeholder.image(img, channels="BGR", use_container_width=True)


def handle_image_input(models, thresholds, placeholder):
    file = st.sidebar.file_uploader(
        "Upload Image", ["jpg", "jpeg", "png", "bmp", "webp"]
    )
    if file:
        data = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(data, cv2.IMREAD_COLOR)
        if img is None:
            st.error("Invalid image file.")
            placeholder.empty() 
        else:
            placeholder.info("Processing image...")
            out_frame = process_frame(img, models, thresholds)
            show_image(out_frame, placeholder)
    else:
        placeholder.info("Upload an image using the sidebar to start.")


def handle_video_input(models, thresholds, placeholder):
    file = st.sidebar.file_uploader("Upload Video", ["mp4", "avi", "mov", "mkv"])
    if file:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        tmp_path = tmp.name
        tmp.write(file.read())
        tmp.close()

        cap = cv2.VideoCapture(tmp_path)
        if not cap.isOpened():
            st.error("Error opening video file.")
            placeholder.empty()
        else:
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            prog_bar = st.progress(0)
            frame_idx = 0
            placeholder.info("Processing video...")
            try:
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    out_frame = process_frame(frame, models, thresholds)
                    show_image(
                        out_frame, placeholder
                    )  # Display frame in the placeholder
                    frame_idx += 1
                    if total_frames > 0:
                        prog_bar.progress(frame_idx / total_frames)
                    else:
                        prog_bar.progress(1.0)  # Handle unknown length videos

                # Clear placeholder and show success message after loop finishes
                placeholder.success("Video processing complete.")
                prog_bar.empty()  # Remove progress bar

            except Exception as e:
                st.error(f"An error occurred during video processing: {e}")
                placeholder.empty()
            finally:
                cap.release()
                try:
                    os.remove(tmp_path)  # Clean up temp file
                except:
                    pass  # Ignore cleanup errors
    else:
        placeholder.info("Upload a video using the sidebar to start.")


def handle_live_camera(models, thresholds, placeholder):
    cam_idx = st.sidebar.number_input(
        "Camera Index", value=DEFAULT_CAMERA_IDX, min_value=0
    )

    # Initialize session state for live feed control
    if "live_active" not in st.session_state:
        st.session_state.live_active = False

    start_button = st.sidebar.button("Start Live Feed", key="start_live")
    stop_button = st.sidebar.button("Stop Live Feed", key="stop_live")

    if start_button:
        st.session_state.live_active = True
    if stop_button:
        st.session_state.live_active = False

    if st.session_state.live_active:
        cap = cv2.VideoCapture(cam_idx)
        if not cap.isOpened():
            st.error(f"Cannot access camera index {cam_idx}.")
            st.session_state.live_active = False  # Stop if camera fails
            placeholder.empty()
        else:
            placeholder.info("Live feed running...")
            try:
                while st.session_state.live_active:  # Check state in loop
                    ret, frame = cap.read()
                    if not ret:
                        st.warning("Failed to grab frame from camera.")
                        break
                    out_frame = process_frame(frame, models, thresholds)
                    show_image(
                        out_frame, placeholder
                    )  # Display frame in the placeholder

                    # Check again if stop button was pressed during processing
                    if not st.session_state.live_active:
                        break

            except Exception as e:
                st.error(f"An error occurred during live feed: {e}")
                st.session_state.live_active = False  # Stop on error
            finally:
                cap.release()
                if (
                    not st.session_state.live_active
                ):  # Show stopped message only if stopped
                    placeholder.warning("Live feed stopped.")

    else:
        placeholder.info("Click 'Start Live Feed' in the sidebar to begin.")


# Streamlit App 
st.set_page_config(layout="wide", page_title="  RDD Using DL")
st.title("✨ Road Detection with YOLOv8 🚗🚨")
st.markdown("[Check On Github](https://github.com/collabdoor/Road-Anomaly-Detection)") # Add this line

# Sidebar: Model selection
st.sidebar.header("Configuration")
st.sidebar.subheader("🧠 Models")
use_m1 = st.sidebar.checkbox("M1 (Model 1)", value=True)
use_m2 = st.sidebar.checkbox("M2 (Model 2)", value=True)

models: dict[str, tuple] = {}
thresholds: dict[str, float] = {}

# Load selected models
if use_m1:
    model_m1, names_m1 = load_yolo_model(MODEL_PATHS["M1 (Model 1)"])
    if model_m1:
        box_m1, label_m1 = make_annotators(sv.Color.RED)
        models["M1 (Model 1)"] = (model_m1, names_m1, box_m1, label_m1)
        thresholds["M1 (Model 1)"] = st.sidebar.slider(
            "M1 Confidence",
            0.0,
            1.0,
            DEFAULT_CONF["M1 (Model 1)"],
            0.05,
            key="m1_conf",
        )

if use_m2:
    model_m2, names_m2 = load_yolo_model(MODEL_PATHS["M2 (Model 2)"])
    if model_m2:
        box_m2, label_m2 = make_annotators(sv.Color.BLUE)
        models["M2 (Model 2)"] = (model_m2, names_m2, box_m2, label_m2)
        thresholds["M2 (Model 2)"] = st.sidebar.slider(
            "M2 Confidence", 0.0, 1.0, DEFAULT_CONF["M2 (Model 2)"], 0.05, key="m2_conf"
        )

if not models:
    st.sidebar.error("Select at least one model to continue.")
    st.stop()

# Sidebar: Input mode
st.sidebar.subheader("🎬 Input Source")
input_mode = st.sidebar.radio(
    "Select Input Type", ["Image", "Video", "Live Camera"], key="input_mode"
)

# Main area placeholder for dynamic content
placeholder = st.empty()

# --- Main Logic ---
if input_mode == "Image":
    handle_image_input(models, thresholds, placeholder)
elif input_mode == "Video":
    handle_video_input(models, thresholds, placeholder)
elif input_mode == "Live Camera":
    handle_live_camera(models, thresholds, placeholder)

# Footer
st.markdown("---")
st.write("© 2025 Team 21")