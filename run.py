from ultralytics import YOLO
import cv2
import supervision as sv
import time
from pathlib import Path

# Configuration
BEST_WEIGHTS_PATH_STR = r"YOLOv8_Small_2nd_Model.pt"
CONF_THRESHOLD = 0.35
MODE = "image"

INPUT_IMAGE_PATH_STR = r"path\to\your\test\image.jpg"
INPUT_VIDEO_PATH_STR = r"path\to\your\test\video.mp4"
OUTPUT_DIR_STR = "inference_output"
CAMERA_INDEX = 0

# Setup
BEST_WEIGHTS_PATH = Path(BEST_WEIGHTS_PATH_STR)
OUTPUT_DIR = Path(OUTPUT_DIR_STR)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load Model
print(f"Loading model from: {BEST_WEIGHTS_PATH}")

try:
    model = YOLO(str(BEST_WEIGHTS_PATH))
    class_names = model.model.names if hasattr(model, "model") else model.names
    print(f"Model loaded! Classes: {class_names}")
except Exception as e:
    print(f"Failed to load model: {e}")
    print(f"Please ensure the model file exists at: {BEST_WEIGHTS_PATH}")
    exit()

# Initialize Supervision Annotators
box_annotator = sv.BoxAnnotator(thickness=2)
label_annotator = sv.LabelAnnotator(
    text_thickness=1, text_scale=0.6, text_color=sv.Color.BLACK, text_padding=2
)


def process_frame(frame: cv2.typing.MatLike, frame_index: int) -> cv2.typing.MatLike:
    results = model.predict(frame, conf=CONF_THRESHOLD, verbose=False)[0]
    detections = sv.Detections.from_ultralytics(results)

    labels = [
        f"{class_names[class_id]} {confidence:.2f}"
        for class_id, confidence in zip(detections.class_id, detections.confidence)
    ]

    annotated_frame = frame.copy()
    annotated_frame = box_annotator.annotate(
        scene=annotated_frame, detections=detections
    )
    annotated_frame = label_annotator.annotate(
        scene=annotated_frame, detections=detections, labels=labels
    )

    return annotated_frame


def infer_on_image(image_path_str: str, output_dir: Path):
    image_path = Path(image_path_str)
    if not image_path.is_file():
        print(f"Can't find the image at {image_path}")
        return

    print(f"Working on image: {image_path.name}")
    frame = cv2.imread(str(image_path))
    if frame is None:
        print(f"Couldn't open the image {image_path}")
        return

    annotated_frame = process_frame(frame, 0)

    output_path = output_dir / f"{image_path.stem}_annotated.jpg"
    cv2.imwrite(str(output_path), annotated_frame)
    print(f"Saved results to: {output_path}")


def infer_on_video(video_path_str: str, output_dir: Path):
    video_path = Path(video_path_str)
    if not video_path.is_file():
        print(f"Can't find the video at {video_path}")
        return

    print(f"Processing video: {video_path.name}")
    output_path = output_dir / f"{video_path.stem}_annotated.mp4"

    try:
        sv.process_video(
            source_path=str(video_path),
            target_path=str(output_path),
            callback=process_frame,
        )
        print(f"Done! Annotated video saved to: {output_path}")
    except Exception as e:
        print(f"Something went wrong during video processing: {e}")
        import traceback

        traceback.print_exc()


def infer_on_live_camera(camera_index: int):
    print(f"Firing up camera {camera_index}. Press 'q' when you're done.")

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"Couldn't access camera {camera_index}")
        return

    prev_time = 0
    frame_count = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Lost connection to the camera.")
                break

            annotated_frame = process_frame(frame, frame_count)
            frame_count += 1

            current_time = time.time()
            if (current_time - prev_time) > 0:
                fps = 1.0 / (current_time - prev_time)
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

            cv2.imshow("Live Camera View (Press 'q' to quit)", annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("Closing camera view.")
                break
    except Exception as e:
        print(f"Camera feed error: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Camera closed.")


if __name__ == "__main__":
    print("\n=== Road Defect Detection ===\n")

    if MODE == "video":
        video_path = Path(INPUT_VIDEO_PATH_STR)
        if not video_path.is_file():
            print(f"The video file doesn't exist: {video_path}")
            print("Double-check the path and try again.")
            exit()

    if MODE == "image":
        infer_on_image(INPUT_IMAGE_PATH_STR, OUTPUT_DIR)
    elif MODE == "video":
        infer_on_video(INPUT_VIDEO_PATH_STR, OUTPUT_DIR)
    elif MODE == "live":
        infer_on_live_camera(CAMERA_INDEX)
    else:
        print(f"Invalid mode '{MODE}'. Use 'image', 'video', or 'live' instead.")

    print("\nAll done!")
