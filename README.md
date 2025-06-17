# Road Anomaly Detection

Our Road Anomaly Detection project. We've been working on using computer vision, specifically YOLOv8 models, to automatically spot issues like cracks and potholes on road surfaces. This repository contains the dataset details, the models we trained and used, evaluation results, and the demo applications we built.

![app](https://github.com/user-attachments/assets/3dbea096-a373-4b12-ad8c-a0dd4a990dd0)

## Dataset

We put together a custom dataset specifically for training our main detection model. The whole process, from sourcing data to annotation, is documented if you're curious about the nitty-gritty details.

*   **Dataset Creation Documentation:** [Read the full process here](https://docs.google.com/document/d/1ICyVPLAKgyiLljKMv-1-_pa14pUD2c5RarL6ku9r8X0/edit?usp=sharing)

The dataset structure within this repository looks like this:

```tree
dataset/
├── test/
│   ├── images/
│   └── labels/
├── train/
│   ├── images/
│   └── labels/
└── valid/
    ├── images/
    └── labels/
```
<!-- ![s](https://www.mermaidchart.com/raw/9d89fee1-5127-41e5-a641-ef1ae628fc61?theme=light&version=v0.1&format=svg) -->

```mermaid
---
config:
  theme: base
  themeVariables:
    primaryColor: '#ffffff'
    primaryTextColor: '#000'
    primaryBorderColor: '#7C838A'
    lineColor: '#536162'
    textColor: '#000'
---
flowchart TD
 subgraph sg0["1️⃣Initial Data Collection"]
    direction LR
        DS1["RAD Dataset<br>(~8.4k img)"]
        DS2["Indian Roads<br>(~5.1k img)"]
        DS3["Humps/Bumps/Potholes<br>(~3.2k img)"]
        DS4["HighRPD Dataset<br>(~11.7k img)"]
  end
 subgraph sg1["2️⃣HighRPD Preprocessing"]
        PreprocHighRPD["Preprocess HighRPD<br>(XML-&gt;YOLO, Map Classes, Split 70/20/10)"]
        PreprocOutput["Preprocessed HighRPD<br>(Train/Valid/Test Splits)"]
  end
 subgraph sg2["3️⃣Label Standardization"]
        InitialCollect["Combined Other Datasets<br>(RAD, Indian, HBP)"]
        Standardize["Standardize All Labels<br>(Define 7 Unified Classes)"]
  end
 subgraph sg3["4️⃣Merging &amp; Initial Split"]
        Merge["Merge Datasets<br>(HighRPD Splits + Standardized Others)<br>Add Prefixes, Verify Pairs"]
        InitialMerged["Initial Merged Dataset<br>Train: 18,005 | Valid: 4,518 | Test: 2,846<br>(Total: 25,369 Images)"]
  end
 subgraph sg4["5️⃣Balancing via Augmentation (Train Set)"]
        AnalyzeImbalance["Analyze Train Set Imbalance<br>(Low: HV, Ped, SB)"]
        Augment["Augment Minority Classes<br>(Flips, Brightness, Rotations)"]
        AugmentedImages["Generated Augmented Images<br>(+5,316 Train: HV, Ped, SB)"]
  end
 subgraph sg5["6️⃣Class Weight Calculation"]
        CalcWeights["Calculate Class Weights<br>(Based on Final Train Dist.)"]
        WeightsOutput["Class Weights<br>(for data.yaml)"]
  end
 subgraph sg6["7️⃣Final Dataset"]
        FinalDataset["Final Unified &amp; Balanced Dataset<br>Total: 30,685 Images<br><b>Train: 23,321</b> (Orig+Aug)<br>Valid: 4,518 | Test: 2,846<br>(YOLOv8 Format + Weights)"]
  end
    DS4 --> PreprocHighRPD
    PreprocHighRPD --> PreprocOutput
    DS1 --> InitialCollect
    DS2 --> InitialCollect
    DS3 --> InitialCollect
    InitialCollect -- Data & Labels --> Standardize
    PreprocOutput -- HighRPD Data & Labels --> Standardize
    Standardize -- Standardized Data --> Merge
    PreprocOutput -- "Pre-split HighRPD Data" --> Merge
    Merge --> InitialMerged
    InitialMerged -- Train Split --> AnalyzeImbalance
    AnalyzeImbalance --> Augment
    Augment --> AugmentedImages
    Augment -- "Post-Augmentation Train Dist." --> CalcWeights
    CalcWeights --> WeightsOutput
    InitialMerged -- Original Train, Valid, Test Splits --> FinalDataset
    AugmentedImages -- Augmented Train Images --> FinalDataset
    WeightsOutput -- Class Weights --> FinalDataset
     DS1:::dataset
     DS2:::dataset
     DS3:::dataset
     DS4:::dataset
     PreprocHighRPD:::process
     PreprocOutput:::output
     InitialCollect:::output
     Standardize:::process
     Merge:::process
     InitialMerged:::output
     AnalyzeImbalance:::importantNote
     Augment:::process
     AugmentedImages:::output
     CalcWeights:::process
     WeightsOutput:::output
     FinalDataset:::output
    classDef dataset fill:#E0F7FA,stroke:#00796B,stroke-width:2px,color:#000
    classDef process fill:#E8F5E9,stroke:#388E3C,stroke-width:2px,color:#000
    classDef output fill:#FFFDE7,stroke:#FBC02D,stroke-width:2px,color:#000
    classDef importantNote fill:#FFEBEE,stroke:#D32F2F,stroke-width:2px,color:#000
```

## Model 1: Custom Trained YOLOv8m (`best.pt`)

This is the primary model we trained from scratch using our custom dataset.

*   **Model Architecture:** YOLOv8m
*   **Training Epochs:** 120
*   **Training Time:** Approx. 27.8 hours
*   **Hardware:** NVIDIA GeForce RTX 3060 Laptop GPU (6GB)
*   **Best Weights File:** `RoadDetectionModel/RoadModel_yolov8m.pt_rounds120_b9/weights/best.pt` (Size: 52.0 MB)
*   **Repository:** [Based on this structure](https://github.com/collabdoor/Road-Anomaly-Detection)

### Validation Performance (`best.pt` during training)

These metrics reflect the performance on the validation set using the best weights saved during the training process.

| Class         | Precision | Recall | mAP@.5 | mAP@.5:.95 |
| :------------ | :-------- | :----- | :----- | :--------- |
| **Overall**   | **0.738** | **0.726** | **0.733** | **0.443** |
| Heavy-Vehicle | 0.921     | 0.976  | 0.979  | 0.764      |
| Light-Vehicle | 0.894     | 0.965  | 0.967  | 0.659      |
| Pedestrian    | 0.838     | 0.903  | 0.910  | 0.494      |
| Crack         | 0.553     | 0.430  | 0.454  | 0.219      |
| Crack-Severe  | 0.526     | 0.467  | 0.471  | 0.265      |
| Pothole       | 0.595     | 0.432  | 0.432  | 0.171      |
| Speed-Bump    | 0.842     | 0.911  | 0.919  | 0.530      |

*   *Validation results saved in:* `RoadDetectionModel/RoadModel_yolov8m.pt_rounds120_b9`

### Test Set Performance (`best.pt` - Final Evaluation)

We ran a final evaluation on a dedicated test set using the `best.pt` model.

| Class         | Precision | Recall | mAP@.5 | mAP@.5:.95 |
| :------------ | :-------- | :----- | :----- | :--------- |
| **Overall**   | **0.736** | **0.740** | **0.745** | **0.448** |
| Heavy-Vehicle | 0.913     | 0.978  | 0.981  | 0.763      |
| Light-Vehicle | 0.892     | 0.951  | 0.961  | 0.649      |
| Pedestrian    | 0.822     | 0.915  | 0.918  | 0.522      |
| Crack         | 0.576     | 0.484  | 0.505  | 0.240      |
| Crack-Severe  | 0.548     | 0.503  | 0.493  | 0.273      |
| Pothole       | 0.597     | 0.440  | 0.468  | 0.198      |
| Speed-Bump    | 0.804     | 0.908  | 0.885  | 0.487      |

*   **Average Inference Speed:** ~12.0 ms per image
*   *Test results saved in:* `runs/detect/val3`

# **Sample Processed Video:** [Watch a sample here](https://www.youtube.com/watch?v=W_SFcuZuRBE)

#### Overall Test Metrics Summary:

*   **Precision:** 0.736
*   **Recall:** 0.740
*   **mAP@0.5:** 0.745
*   **mAP@0.5:0.95:** 0.448
*   **F1-Score:** 0.738 (Calculated as 2 * (P * R) / (P + R))

### Test Set Evaluation Visualizations (Model 1 - `best.pt`)

Here are some charts generated during the final test set evaluation:

<table>
  <tr>
    <td><img src="runs/detect/val3/confusion_matrix.png" alt="Confusion Matrix" width="250"/></td>
    <td><img src="runs/detect/val3/confusion_matrix_normalized.png" alt="Normalized Confusion Matrix" width="250"/></td>
    <td><img src="runs/detect/val3/F1_curve.png" alt="F1 Curve" width="250"/></td>
  </tr>
  <tr>
    <td><img src="runs/detect/val3/PR_curve.png" alt="Precision-Recall Curve" width="250"/></td>
    <td><img src="runs/detect/val3/P_curve.png" alt="Precision Curve" width="250"/></td>
    <td><img src="runs/detect/val3/R_curve.png" alt="Recall Curve" width="250"/></td>
  </tr>
</table>

*(Images sourced from `runs/detect/val3`)*

## Model 2: Pre-trained YOLOv8s (`YOLOv8_Small_2nd_Model.pt`)

We also incorporated a second, pre-trained model for comparison and potential fusion.

*   **Model File:** `YOLOv8_Small_2nd_Model.pt`
*   **Model Architecture:** YOLOv8s
*   **Source Repository:** [oracl4/RoadDamageDetection](https://github.com/oracl4/RoadDamageDetection)
*   **Training Data:** CRDDC2022 Dataset
*   **Detected Classes:** `Longitudinal Crack`, `Transverse Crack`, `Alligator Crack`, `Potholes`

## Demo Applications

We've built a couple of interfaces to showcase the models in action.

### Streamlit Web App

This is our main demo app, allowing you to test the models easily.

*   **Functionality:** Detect anomalies in uploaded images, videos, or a live camera feed ("Dash Cam").

<!-- ![app](https://www.mermaidchart.com/raw/58877765-627f-44d3-9349-5c7817849fa3?theme=light&version=v0.1&format=svg) -->

```mermaid
---
config:
  theme: base
  themeVariables:
    primaryColor: '#ffffff'
    primaryTextColor: '#000'
    primaryBorderColor: '#7C838A'
    lineColor: '#536162'
    textColor: '#000'
---
flowchart TD
    U["User"] --> SB["Streamlit Sidebar"]
    SB --> MS["Model Selection"] & CT["Confidence Thresholds"] & IS["Input Source"]
    IS --> FileInput["Uploaded File (Image)/(Video)"] & CamInput["Camera Feed"]
    FileInput --> Frame["Input Frame/Image"]
    CamInput --> Frame
    Frame --> PROC["Processing Engine"]
    MS --> PROC
    CT --> PROC
    PROC --> YOLO["YOLOv8 Inference"] & AnnotatedFrame["Annotated Frame/Image"]
    YOLO --> PROC
    AnnotatedFrame --> MA["Streamlit Main Area"]
    MA --> U
     U:::user
     SB:::ui
     MS:::config
     CT:::config
     IS:::config
     FileInput:::data
     CamInput:::data
     Frame:::data
     PROC:::process
     YOLO:::model
     AnnotatedFrame:::data
     MA:::ui
    classDef user fill:#FFCDD2,stroke:#C62828,stroke-width:2px,color:#000
    classDef ui fill:#D1C4E9,stroke:#4527A0,stroke-width:2px,color:#000
    classDef config fill:#FFF9C4,stroke:#F9A825,stroke-width:2px,color:#000
    classDef data fill:#C8E6C9,stroke:#2E7D32,stroke-width:2px,color:#000
    classDef process fill:#B3E5FC,stroke:#0277BD,stroke-width:2px,color:#000
    classDef model fill:#FFCCBC,stroke:#D84315,stroke-width:2px,color:#000
```

*   **Features:**
    *   Choose between Model 1 (`M1`) and Model 2 (`M2`) or use both.
    *   Adjust the confidence threshold for each model independently.
    *   View detections overlaid on the input. M1 detections are in **RED**, M2 detections are in **BLUE**.
*   **Live Demo:** [**Try it out here!**](https://road-anomaly-detection.streamlit.app/)

### Flask Interface App (Under Construction)

We started building a Flask-based interface as well.

*   **Location:** `interface-app/`
*   **Status:** This app is currently under development and not fully functional yet.

## Project Structure

Here's a glance at how the project files are organized:

```
C:.
│   .gitignore
│   do this setup.md
│   main.py
│   packages.txt
│   README.md
│   requirements.txt
│   run.py
│   run2model.py
│   train.ipynb
│   visualize_annotations_data.py
│   web interface.md
│   yolo11n.pt
│   yolov8m.pt
│   YOLOv8_Small_2nd_Model.pt
│
├───.devcontainer
│       devcontainer.json
│
├───.streamlit
│       config.toml
│
├───.vscode
│       settings.json
│
├───dataset
│   ├───test
│   │   ├───images
│   │   └───labels
│   ├───train
│   │   ├───images
│   │   └───labels
│   └───valid
│       ├───images
│       └───labels
│
├───inference_output
│       India_000884_jpg.rf.7d8d1739a4debaece30cbe543980de9c_annotated.jpg     
│
├───inference_output_two_models
│       v_annotated_2models.mp4
│
├───interface-app
│   │   app.py
│   │   requirements.txt
│   │   ... (static, templates folders)
│
├───RoadDetectionModel
│   └───RoadModel_yolov8m.pt_rounds120_b9
│       │   args.yaml
│       │   confusion_matrix.png
│       │   ... (other training/validation outputs)
│       │
│       └───weights
│               best.pt
│               last.pt
│
└───runs
    └───detect
        ├───val
        │    ... (older Test Set Evaluation Metrics)
        │
        └───val3
             (New Test Set Evaluation Metrics )

```

## Running Locally

Want to run this project on your own machine? Great! We've put together a guide to help you set up the environment and get things running.

Please follow the instructions in the [**`do this setup.md`**](https://github.com/collabdoor/Road-Anomaly-Detection/blob/main/do%20this%20setup.md) file located in the root of this repository.

---

## Authors

- [Nikita Kumari](https://github.com/iamnikitaa)
- [Navneet Sharma](https://github.com/nav9v)
- [Ojus Kumar](https://github.com/ojuss)

Thanks for checking out our project
