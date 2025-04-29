from ultralytics import YOLO
import cv2
import supervision as sv
import time
from pathlib import Path
import traceback  

# Configuration
MODEL_1_WEIGHTS_PATH_STR = r".\RoadDetectionModel\RoadModel_yolov8m.pt_rounds120_b9\weights\best.pt"
MODEL_2_WEIGHTS_PATH_STR = r"YOLOv8_Small_2nd_Model.pt"

CONF_THRESHOLD_MODEL_1 = 0.35
CONF_THRESHOLD_MODEL_2 = 0.40

MODE = "video"  # Options: "image", "video", "live"

INPUT_IMAGE_PATH_STR = r"path\to\your\test\image.jpg"
INPUT_VIDEO_PATH_STR = r"Downloads\v.mp4"
OUTPUT_DIR_STR = "inference_output_two_models"
CAMERA_INDEX = 0

# Setup
MODEL_1_WEIGHTS_PATH = Path(MODEL_1_WEIGHTS_PATH_STR)
MODEL_2_WEIGHTS_PATH = Path(MODEL_2_WEIGHTS_PATH_STR)
OUTPUT_DIR = Path(OUTPUT_DIR_STR)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load Models
model1 = None
model2 = None
class_names1 = {}
class_names2 = {}
models_loaded = False

try:
    if not MODEL_1_WEIGHTS_PATH.is_file():
        print(f"Model 1 weights not found at {MODEL_1_WEIGHTS_PATH}")
    else:
        model1 = YOLO(str(MODEL_1_WEIGHTS_PATH))
        class_names1 = model1.names
        print("Model 1 loaded successfully.")

    if not MODEL_2_WEIGHTS_PATH.is_file():
        print(f"Model 2 weights not found at {MODEL_2_WEIGHTS_PATH}")
    else:
        model2 = YOLO(str(MODEL_2_WEIGHTS_PATH))
        class_names2 = model2.names
        print("Model 2 loaded successfully.")

    if model1 and model2:
        models_loaded = True
        print("Great! Both models loaded successfully.")
    else:
        print("Problem: One or both models failed to load. Please check the paths.")

except Exception as e:
    print(f"Something went wrong loading the models: {e}")
    traceback.print_exc()

if not models_loaded:
    exit()

# Initialize Supervision Annotators
box_annotator1 = sv.BoxAnnotator(thickness=2, color=sv.Color.RED)
label_annotator1 = sv.LabelAnnotator(
    text_thickness=1,
    text_scale=0.5,
    color=sv.Color.WHITE,
    text_color=sv.Color.BLACK,
    text_padding=2,
    text_position=sv.Position.TOP_LEFT,
)
box_annotator2 = sv.BoxAnnotator(thickness=2, color=sv.Color.BLUE)
label_annotator2 = sv.LabelAnnotator(
    text_thickness=1,
    text_scale=0.5,
    color=sv.Color.WHITE,
    text_color=sv.Color.BLACK,
    text_padding=2,
    text_position=sv.Position.TOP_RIGHT,
)

# Inference Functions


def process_frame_two_models(
    frame: cv2.typing.MatLike, frame_index: int
) -> cv2.typing.MatLike:
    """Runs prediction and annotation for two models on a single frame."""
    annotated_frame = frame.copy()

    # Model 1 Inference & Annotation
    try:
        results1 = model1.predict(frame, conf=CONF_THRESHOLD_MODEL_1, verbose=False)[0]
        detections1 = sv.Detections.from_ultralytics(results1)
        labels1 = [
            f"M1:{class_names1.get(cls_id, f'cls_{cls_id}')} {conf:.2f}"
            for cls_id, conf in zip(detections1.class_id, detections1.confidence)
        ]
        annotated_frame = box_annotator1.annotate(
            scene=annotated_frame, detections=detections1
        )
        annotated_frame = label_annotator1.annotate(
            scene=annotated_frame, detections=detections1, labels=labels1
        )
    except Exception as e:
        print(f"Error with Model 1 on frame {frame_index}: {e}")

    # Model 2 Inference & Annotation
    try:
        results2 = model2.predict(frame, conf=CONF_THRESHOLD_MODEL_2, verbose=False)[0]
        detections2 = sv.Detections.from_ultralytics(results2)
        labels2 = [
            f"M2:{class_names2.get(cls_id, f'cls_{cls_id}')} {conf:.2f}"
            for cls_id, conf in zip(detections2.class_id, detections2.confidence)
        ]
        annotated_frame = box_annotator2.annotate(
            scene=annotated_frame, detections=detections2
        )
        annotated_frame = label_annotator2.annotate(
            scene=annotated_frame, detections=detections2, labels=labels2
        )
    except Exception as e:
        print(f"Error with Model 2 on frame {frame_index}: {e}")

    return annotated_frame


def infer_on_image(image_path_str: str, output_dir: Path):
    """Runs inference on a single image."""
    image_path = Path(image_path_str)
    if not image_path.is_file():
        print(f"Can't find the image at {image_path}")
        return

    frame = cv2.imread(str(image_path))
    if frame is None:
        print(f"Couldn't read the image at {image_path}")
        return

    annotated_frame = process_frame_two_models(frame, 0)
    output_path = output_dir / f"{image_path.stem}_annotated_2models.jpg"
    cv2.imwrite(str(output_path), annotated_frame)
    print(f"Saved annotated image to: {output_path}")


def infer_on_video(video_path_str: str, output_dir: Path):
    """Runs inference on a video file."""
    video_path = Path(video_path_str)
    if not video_path.is_file():
        print(f"Can't find the video at {video_path}")
        return

    output_path = output_dir / f"{video_path.stem}_annotated_2models.mp4"
    print(f"Processing video: {video_path.name} -> {output_path.name}")

    try:
        sv.process_video(
            source_path=str(video_path),
            target_path=str(output_path),
            callback=process_frame_two_models,
        )
        print(f"Finished! Annotated video saved to: {output_path}")
    except Exception as e:
        print(f"Video processing error: {e}")
        traceback.print_exc()


def infer_on_live_camera(camera_index: int):
    """Runs inference on a live camera feed."""
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"Couldn't open camera {camera_index}")
        return

    print(f"Starting live feed from camera {camera_index}. Press 'q' to quit.")
    prev_time = 0
    frame_count = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Lost connection to the camera.")
                time.sleep(0.5)
                continue

            annotated_frame = process_frame_two_models(frame, frame_count)
            frame_count += 1

            # Calculate and display FPS
            current_time = time.time()
            fps = (
                1.0 / (current_time - prev_time)
                if (current_time - prev_time) > 0
                else 0
            )
            prev_time = current_time
            cv2.putText(
                annotated_frame,
                f"FPS: {fps:.1f}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2,
            )

            cv2.imshow("Live Camera - Two Models (Press 'q' to quit)", annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    except Exception as e:
        print(f"Camera feed error: {e}")
        traceback.print_exc()
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Camera closed.")


# Main Execution
if __name__ == "__main__":
    if not models_loaded:
        print("Exiting due to model loading failure.")
        exit()

    print(f"\n=== Road Anomaly Detection: {MODE} Mode ===")

    if MODE == "image":
        infer_on_image(INPUT_IMAGE_PATH_STR, OUTPUT_DIR)
    elif MODE == "video":
        infer_on_video(INPUT_VIDEO_PATH_STR, OUTPUT_DIR)
    elif MODE == "live":
        infer_on_live_camera(CAMERA_INDEX)
    else:
        print(f"Invalid mode '{MODE}'. Use 'image', 'video', or 'live' instead.")

    print("\nAll done!")
