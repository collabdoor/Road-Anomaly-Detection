import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
import supervision as sv
import tempfile
import os
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode
import av
import logging

# --- Configuration ---
MODEL_PATHS = {
    "M1 (Model 1)": "./RoadDetectionModel/RoadModel_yolov8m.pt_rounds120_b9/weights/best.pt",
    "M2 (Model 2)": "./YOLOv8_Small_2nd_Model.pt",
}
MODEL_PREFIX = {
    "M1 (Model 1)": "M1",
    "M2 (Model 2)": "M2",
}
DEFAULT_CONF = {"M1 (Model 1)": 0.35, "M2 (Model 2)": 0.40}

# Target width for processing live frames. Lower values increase performance.
LIVE_FEED_TARGET_WIDTH = 640 

# Setup logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


@st.cache_resource
def load_yolo_model(path: str):
    try:
        model = YOLO(path)
        logger.info(f"Successfully loaded model from {path}")
        return model, model.names
    except Exception as e:
        st.error(f"Error loading model at {path}: {e}")
        logger.error(f"Failed to load model at {path}", exc_info=e)
        return None, {}


def make_annotators(color: sv.Color):
    box_annotator = sv.BoxAnnotator(thickness=1, color=color)
    label_annotator = sv.LabelAnnotator(
        text_thickness=1,
        text_scale=0.4,
        color=sv.Color.WHITE,
        text_color=sv.Color.BLACK,
        text_padding=2,
    )
    return box_annotator, label_annotator


def process_frame(
    frame: np.ndarray, models: dict[str, tuple], thresholds: dict[str, float]
) -> np.ndarray:
    annotated_frame = frame.copy()
    for model_name, (model, names_map, box_ann, label_ann) in models.items():
        try:
            # Perform inference
            results = model.predict(frame, conf=thresholds[model_name], verbose=False)[
                0
            ]
            detections = sv.Detections.from_ultralytics(results)

            # Create labels
            labels = [
                f"{MODEL_PREFIX[model_name]}:{names_map.get(cls_id, str(cls_id))} {conf:.2f}"
                for cls_id, conf in zip(detections.class_id, detections.confidence)
            ]

            # Annotate the frame
            annotated_frame = box_ann.annotate(annotated_frame, detections)
            annotated_frame = label_ann.annotate(
                annotated_frame, detections, labels=labels
            )

        except Exception as e:
            logger.error(f"Error during prediction/annotation for {model_name}: {e}")
            cv2.putText(
                annotated_frame,
                f"Error processing {model_name}",
                (10, 30 + list(models.keys()).index(model_name) * 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
            )

    return annotated_frame


def handle_image_input(models, thresholds, placeholder):
    uploaded_file = st.sidebar.file_uploader(
        "Upload Image", type=["jpg", "jpeg", "png", "bmp", "webp"], key="img_upload"
    )
    if uploaded_file:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if img is None:
            st.error("Could not decode image. Please upload a valid image file.")
            placeholder.empty()
        else:
            with st.spinner("Processing image..."):
                processed_img = process_frame(img, models, thresholds)
            placeholder.image(processed_img, channels="BGR", use_container_width=True)
            st.success("Image processing complete.")
    else:
        placeholder.info("Upload an image using the sidebar to start.")


def handle_video_input(models, thresholds, status_placeholder):
    uploaded_file = st.sidebar.file_uploader(
        "Upload Video", type=["mp4", "avi", "mov", "mkv"], key="vid_upload"
    )
    if uploaded_file:
        input_tmp_path = None
        output_video_path = None
        cap = None
        writer = None

        try:
            # Save uploaded video to a temporary file
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=".mp4"
            ) as input_tmp_file:
                input_tmp_path = input_tmp_file.name
                input_tmp_file.write(uploaded_file.read())
            logger.info(f"Input video saved to temporary file: {input_tmp_path}")

            cap = cv2.VideoCapture(input_tmp_path)
            if not cap.isOpened():
                st.error("Error opening uploaded video file.")
                status_placeholder.empty()
                return

            # Get video properties
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            if fps <= 0:  # Handle potential issue with reading FPS
                fps = 30
                logger.warning("Could not read video FPS, defaulting to 30.")

            # Create a temporary file for the output video
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=".mp4"
            ) as output_tmp_file:
                output_video_path = output_tmp_file.name
            logger.info(f"Output video will be saved to: {output_video_path}")

            # Setup VideoWriter
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Codec for MP4
            writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
            if not writer.isOpened():
                st.error(
                    f"Error initializing video writer. Check codec ('mp4v') and OpenCV backend."
                )
                logger.error(
                    f"Failed to open VideoWriter for path: {output_video_path}"
                )
                output_video_path = None 
                return

            prog_bar = st.progress(0, text="Processing video...")
            status_placeholder.info("Processing video... Preview shown below.")
            preview_placeholder = st.empty() 
            frame_idx = 0

            while True:
                ret, frame = cap.read()
                if not ret:
                    break  # End of video

                # Process frame
                out_frame = process_frame(frame, models, thresholds)

                # Write to output file
                writer.write(out_frame)

                # Show preview
                preview_placeholder.image(
                    out_frame, channels="BGR", use_container_width=True
                )

                # Update progress
                frame_idx += 1
                progress_percentage = (
                    frame_idx / total_frames if total_frames > 0 else 0
                )
                prog_text = f"Processing video... {frame_idx}/{total_frames if total_frames > 0 else '?'}"
                prog_bar.progress(min(progress_percentage, 1.0), text=prog_text)

            # Processing finished
            preview_placeholder.empty()  
            status_placeholder.success("✅ Video processing complete!")
            prog_bar.progress(1.0, text="Processing complete.")
            logger.info("Video processing finished.")

        except Exception as e:
            st.error(f"An error occurred during video processing: {e}")
            logger.error("Error during video processing loop", exc_info=e)
            status_placeholder.error("Processing failed.")  
            preview_placeholder.empty()  
            prog_bar.empty()
            output_video_path = None  
            
        finally:
            # Release resources
            if cap is not None:
                cap.release()
            if writer is not None:
                writer.release()
            logger.info("Video capture and writer resources released.")

            # Clean up input temporary file
            if input_tmp_path and os.path.exists(input_tmp_path):
                try:
                    os.remove(input_tmp_path)
                    logger.info(f"Removed input temp file: {input_tmp_path}")
                except OSError as rm_err:
                    logger.error(
                        f"Error removing input temp file {input_tmp_path}: {rm_err}"
                    )

        # --- Provide Download Button ---
        if output_video_path and os.path.exists(output_video_path):
            try:
                with open(output_video_path, "rb") as f:
                    video_bytes = f.read()
                st.download_button(
                    label="⬇️ Download Processed Video",
                    data=video_bytes,
                    file_name=f"processed_{uploaded_file.name}",
                    mime="video/mp4",
                )
                logger.info(f"Download button provided for: {output_video_path}")
            except Exception as e:
                st.error(f"Error reading processed video for download: {e}")
                logger.error(
                    f"Error reading output file {output_video_path} for download",
                    exc_info=e,
                )
            finally:
                # Clean up output temporary file AFTER offering download
                if os.path.exists(output_video_path):
                    try:
                        os.remove(output_video_path)
                        logger.info(f"Removed output temp file: {output_video_path}")
                    except OSError as rm_err:
                        logger.error(
                            f"Error removing output temp file {output_video_path}: {rm_err}"
                        )
        elif (
            output_video_path
        ): 
            logger.warning(
                "Output video file not found for download, likely due to processing error."
            )
        prog_bar.empty()  
        
    else:
        status_placeholder.info("Upload a video using the sidebar to start.")


class YOLOVideoProcessor(VideoProcessorBase):
    def __init__(self, models, thresholds, target_width):
        self.models = models
        self.thresholds = thresholds
        self.target_width = target_width
        logger.info(
            f"YOLOVideoProcessor initialized. Target processing width: {self.target_width}"
        )

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        original_height, original_width = img.shape[:2]
        img_resized = img  
        
        # Resize for performance if needed
        if self.target_width is not None and original_width > self.target_width:
            aspect_ratio = original_height / original_width
            target_height = int(self.target_width * aspect_ratio)
            img_resized = cv2.resize(
                img, (self.target_width, target_height), interpolation=cv2.INTER_AREA
            )

        # Process the (potentially resized) frame
        annotated_frame_resized = process_frame(
            img_resized, self.models, self.thresholds
        )

        # Resize back to original dimensions for display consistency
        if img_resized is not img:  
            final_frame = cv2.resize(
                annotated_frame_resized,
                (original_width, original_height),
                interpolation=cv2.INTER_LINEAR,
            )
        else:
            final_frame = annotated_frame_resized

        return av.VideoFrame.from_ndarray(final_frame, format="bgr24")


def handle_live_camera(models, thresholds):
    st.sidebar.info(
        "Click 'START' below to access your camera. "
        "Ensure camera permissions are granted in your browser."
    )

    # Suggest lower resolution/FPS to the browser for better performance
    media_constraints = {
        "video": {
            "width": {"ideal": 640},
            "height": {"ideal": 480},
            "frameRate": {"ideal": 15, "max": 30}  
        },
        "audio": False,
    }

    def processor_factory():
        return YOLOVideoProcessor(
            models=models, thresholds=thresholds, target_width=LIVE_FEED_TARGET_WIDTH
        )

    webrtc_ctx = webrtc_streamer(
        key="live-camera-streamer",
        mode=WebRtcMode.SENDRECV,
        video_processor_factory=processor_factory,
        media_stream_constraints=media_constraints,
        async_processing=True,  
        rtc_configuration={  
            "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
        },
    )

    if not webrtc_ctx.state.playing:
        st.info("Camera feed stopped or not started.")


# --- Streamlit App Main ---
def main():
    st.set_page_config(layout="wide", page_title="Road Anomaly Detection")
    st.title("✨ Road Anomaly Detection with YOLOv8 🚗🚨")
    st.markdown(
        "[Check On Github](https://github.com/collabdoor/Road-Anomaly-Detection)"
    )

    # Sidebar Configuration
    st.sidebar.header("⚙️ Configuration")
    st.sidebar.subheader("🧠 Models")
    use_m1 = st.sidebar.checkbox("M1 (RoadModel_yolov8m)", value=True, key="cb_m1")
    use_m2 = st.sidebar.checkbox("M2 (YOLOv8_Small_2nd_Model)", value=True, key="cb_m2")

    models_to_load = {}
    if use_m1:
        models_to_load["M1 (Model 1)"] = MODEL_PATHS["M1 (Model 1)"]
    if use_m2:
        models_to_load["M2 (Model 2)"] = MODEL_PATHS["M2 (Model 2)"]

    # Load models and setup annotators
    loaded_models = {}
    thresholds = {}
    model_load_failed = False

    if not models_to_load:
        st.sidebar.warning("Select at least one model checkbox to start.")
        st.info("👈 Please select models and configure input source in the sidebar.")
        st.stop()

    for name, path in models_to_load.items():
        model, names_map = load_yolo_model(path)
        if model and names_map:
            color = sv.Color.RED if name == "M1 (Model 1)" else sv.Color.BLUE
            box_ann, label_ann = make_annotators(color)
            loaded_models[name] = (model, names_map, box_ann, label_ann)
            thresholds[name] = st.sidebar.slider(
                f"{name} Confidence",
                0.1,
                1.0,
                DEFAULT_CONF[name],
                0.05,
                key=f"{name}_conf",
            )
        else:
            model_load_failed = True

    if model_load_failed:
        st.error("One or more models failed to load. Check logs and file paths.")
        st.stop() 

    # Sidebar Input Selection
    st.sidebar.subheader("🎬 Input Source")
    input_mode = st.sidebar.radio(
        "Select Input Type", ["Image", "Video", "Live Camera"], key="input_mode_radio"
    )

    # Main Area Logic based on Input Mode
    if input_mode == "Image":
        image_placeholder = st.empty()
        handle_image_input(loaded_models, thresholds, image_placeholder)
    elif input_mode == "Video":
        video_status_placeholder = st.empty()
        handle_video_input(loaded_models, thresholds, video_status_placeholder)
    elif input_mode == "Live Camera":
        handle_live_camera(loaded_models, thresholds)

    # Footer
    st.markdown("---")
    st.write("© 2025 Team 21")


if __name__ == "__main__":
    main()
