# Safety Gear Detection System

This project aims to create a video processing pipeline that uses a YOLO model to detect various safety gear items such as helmets, gloves, and seat belts. The system provides real-time detection status and draws a table with warnings based on the detection results.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction
The Safety Gear Detection System uses computer vision techniques to monitor safety compliance in real-time. It processes video frames to detect the presence of specific safety gear items and provides visual feedback on compliance status.

## Features
- **Real-time Detection:** Uses YOLO model for detecting various safety gear items.
- **Detection Confirmation:** Ensures detections are confirmed over a specific duration to reduce false positives.
- **Visual Feedback:** Draws a table on the video frames indicating the detection status of each safety gear item.
- **Flexible Configuration:** Easily configurable detection parameters and intervals.

## Installation
### Prerequisites
- Python 3.7+
- OpenCV
- PyTorch
- YOLOv8

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/yakupzengin/yolov8-object-detection.git
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Download the YOLOv8 model and place it in the project directory.

## Usage
1. Adjust the `model_path`, `video_path`, and `output_path` variables in the `main.py` script to point to your model file, input video, and desired output location.
2. Run the main script:
    ```bash
    python main.py
    ```

## Project Structure
```plaintext
safety-gear-detection/
│
├── YOLOModel.py                  # YOLO model wrapper class
├── VideoProcessor.py             # Video processing class
├── DetectionDrawer.py            # Drawing detections and statuses on frames
├── main.py                       # Main script for running the detection system
├── requirements.txt              # List of dependencies
└── README.md                     # Project documentation
