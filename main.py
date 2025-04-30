import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
import supervision as sv
import tempfile
import os
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode
import av 

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
        # Ensure text position is handled correctly if needed, e.g., using sv.Position.TOP_LEFT
        # text_position=sv.Position.TOP_LEFT
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
                    show_image(out_frame, placeholder)
                    frame_idx += 1
                    if total_frames > 0:
                        prog_bar.progress(frame_idx / total_frames)
                    else:
                        prog_bar.progress(1.0)  # Handle unknown length videos

                # Clear placeholder and show success message after loop finishes
                placeholder.success("Video processing complete.")
                prog_bar.empty() 

            except Exception as e:
                st.error(f"An error occurred during video processing: {e}")
                placeholder.empty()
            finally:
                cap.release()
                try:
                    os.remove(tmp_path) 
                except:
                    pass
    else:
        placeholder.info("Upload a video using the sidebar to start.")


# Replace the old handle_live_camera function with this one
def handle_live_camera(models, thresholds):
    class YOLOVideoProcessor(VideoProcessorBase):
        def __init__(self):
            self.models = models
            self.thresholds = thresholds

        def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
            img = frame.to_ndarray(format="bgr24")
            annotated_frame = process_frame(img, self.models, self.thresholds)
            return av.VideoFrame.from_ndarray(annotated_frame, format="bgr24")

    st.sidebar.info(
        "Click 'Start' below to access your dash cam."
    )  # Changed webcam to dash cam

    webrtc_ctx = webrtc_streamer(
        key="live-camera",
        mode=WebRtcMode.SENDRECV,
        video_processor_factory=YOLOVideoProcessor,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
        rtc_configuration={  # Add this to potentially improve connection stability
            "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
        },
    )

    if not webrtc_ctx.state.playing:
        st.info(
            "DashCam feed stopped or not started."
        ) 
    else:
        st.info(
            "Processing live DashCam feed..."
        )  


# Streamlit App
st.set_page_config(layout="wide", page_title="  RDD Using DL")
st.title("✨ Road Anomaly Detection with YOLOv8 🚗🚨")
st.markdown(
    "[Check On Github](https://github.com/collabdoor/Road-Anomaly-Detection)"
) 

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

# --- Main Logic ---
if input_mode == "Image":
    placeholder = st.empty()
    handle_image_input(models, thresholds, placeholder)
elif input_mode == "Video":
    placeholder = st.empty() 
    handle_video_input(models, thresholds, placeholder)
elif input_mode == "Live Camera":
    handle_live_camera(models, thresholds)

# Footer
st.markdown("---")
st.write("© 2025 Team 21")
