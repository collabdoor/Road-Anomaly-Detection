import cv2
import os
import yaml
import numpy as np

# Configuration
DATASET_BASE_DIR = "dataset"
DATA_YAML_PATH = os.path.join(DATASET_BASE_DIR, "data.yaml")
SPLIT_TO_VIEW = "train"

IMAGE_DIR = os.path.join(DATASET_BASE_DIR, SPLIT_TO_VIEW, "images")
LABEL_DIR = os.path.join(DATASET_BASE_DIR, SPLIT_TO_VIEW, "labels")

# Default window size and scale factor
DEFAULT_MAX_WIDTH = 1280
DEFAULT_MAX_HEIGHT = 720
DEFAULT_SCALE_FACTOR = 1.0

# Load Class Names
try:
    with open(DATA_YAML_PATH, "r") as f:
        data_yaml = yaml.safe_load(f)
        CLASS_NAMES = data_yaml["names"]
        print(f"Found these classes: {CLASS_NAMES}")
except Exception as e:
    print(f"Couldn't read the class names from {DATA_YAML_PATH}: {e}")
    CLASS_NAMES = None


# Visualization Function
def visualize_yolo_annotations(image_dir, label_dir, class_names):
    image_files = sorted(
        [
            f
            for f in os.listdir(image_dir)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]
    )
    num_images = len(image_files)
    current_index = 0
    scale_factor = DEFAULT_SCALE_FACTOR

    # Window name
    window_name = "YOLO Annotations - n:next p:prev q:quit +/-:zoom r:reset"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    while True:
        if current_index < 0:
            current_index = 0
        if current_index >= num_images:
            current_index = num_images - 1

        img_filename = image_files[current_index]
        img_path = os.path.join(image_dir, img_filename)
        label_filename = os.path.splitext(img_filename)[0] + ".txt"
        label_path = os.path.join(label_dir, label_filename)

        # Load Image
        image = cv2.imread(img_path)
        if image is None:
            print(f"Can't load this image: {img_path}")
            key = cv2.waitKey(0)
            if key == ord("q"):
                break
            elif key == ord("n"):
                current_index += 1
                continue
            elif key == ord("p"):
                current_index -= 1
                continue
            else:
                continue

        orig_h, orig_w, _ = image.shape
        vis_image = image.copy()

        # Load and Draw Annotations
        if os.path.exists(label_path):
            try:
                with open(label_path, "r") as f:
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) >= 5:
                            (
                                class_id,
                                x_center_norm,
                                y_center_norm,
                                width_norm,
                                height_norm,
                            ) = map(float, parts[:5])
                            class_id = int(class_id)

                            # Denormalize coordinates
                            box_w = width_norm * orig_w
                            box_h = height_norm * orig_h
                            center_x = x_center_norm * orig_w
                            center_y = y_center_norm * orig_h

                            x_min = int(center_x - (box_w / 2))
                            y_min = int(center_y - (box_h / 2))
                            x_max = int(center_x + (box_w / 2))
                            y_max = int(center_y + (box_h / 2))

                            # Draw bounding box (Green color)
                            cv2.rectangle(
                                vis_image,
                                (x_min, y_min),
                                (x_max, y_max),
                                (0, 255, 0),
                                2,
                            )

                            # Draw label
                            if class_names and 0 <= class_id < len(class_names):
                                label = class_names[class_id]
                            else:
                                label = f"Class_{class_id}"

                            # Put label text above the box
                            (text_width, text_height), baseline = cv2.getTextSize(
                                label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1
                            )
                            cv2.rectangle(
                                vis_image,
                                (x_min, y_min - text_height - baseline),
                                (x_min + text_width, y_min),
                                (0, 255, 0),
                                -1,
                            )  # Filled background
                            cv2.putText(
                                vis_image,
                                label,
                                (x_min, y_min - baseline),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.5,
                                (0, 0, 0),
                                1,
                            )  # Black text

            except Exception as e:
                print(f"Problem reading label file {label_path}: {e}")
        else:
            print(f"No label file for this image: {label_path}")

        # Add display information
        display_text = f"{SPLIT_TO_VIEW}: {img_filename} ({current_index + 1}/{num_images}) - Scale: {scale_factor:.2f}x"
        cv2.putText(
            vis_image,
            display_text,
            (10, 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2,
        )

        # Resize image to fit window while maintaining aspect ratio
        display_h, display_w = int(orig_h * scale_factor), int(orig_w * scale_factor)

        # Resize if the image is too large or too small (based on scale_factor)
        if display_w != orig_w or display_h != orig_h:
            vis_image = cv2.resize(
                vis_image,
                (display_w, display_h),
                interpolation=cv2.INTER_AREA if scale_factor < 1 else cv2.INTER_LINEAR,
            )

        # Resize window to fit the content (with limits)
        window_w = min(display_w, DEFAULT_MAX_WIDTH)
        window_h = min(display_h, DEFAULT_MAX_HEIGHT)
        cv2.resizeWindow(window_name, window_w, window_h)

        # Display Image
        cv2.imshow(window_name, vis_image)

        # Key Handling
        key = cv2.waitKey(0)
        if key == ord("q"):
            break
        elif key == ord("n"):
            current_index += 1
        elif key == ord("p"):
            current_index -= 1
        elif key == ord("+") or key == ord("="):
            scale_factor *= 1.2
        elif key == ord("-") or key == ord("_"):
            scale_factor /= 1.2
        elif key == ord("r"):
            scale_factor = DEFAULT_SCALE_FACTOR
        elif key == 32:
            if (
                cv2.getWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN)
                == cv2.WINDOW_FULLSCREEN
            ):
                cv2.setWindowProperty(
                    window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL
                )
            else:
                cv2.setWindowProperty(
                    window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN
                )

    cv2.destroyAllWindows()
    print("All done viewing annotations!")


# Run Visualization
if __name__ == "__main__":
    if not os.path.exists(IMAGE_DIR) or not os.path.exists(LABEL_DIR):
        print(
            f"Can't find images or labels. Check these folders: {IMAGE_DIR} and {LABEL_DIR}"
        )
    elif CLASS_NAMES is None:
        print("No class names found. Make sure data.yaml exists and is formatted correctly.")
    else:
        visualize_yolo_annotations(IMAGE_DIR, LABEL_DIR, CLASS_NAMES)
