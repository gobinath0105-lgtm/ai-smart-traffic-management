# 🚦 AI Smart Traffic Management & Emergency Corridor System

An AI-based traffic management prototype that uses **YOLOv8 object detection** and **OpenCV** to analyze traffic from video and support intelligent traffic signal management.

The system is designed to monitor traffic conditions, identify vehicles, estimate traffic levels, and provide an emergency corridor concept for priority vehicles.

## 🎯 Problem

Traditional traffic signals generally operate using fixed or predefined timings. These timings may not respond effectively to changing traffic conditions.

Heavy traffic can result in:

* 🚗 Increased vehicle queues
* ⏱️ Longer waiting time
* ⛽ Higher fuel consumption
* 🌫️ Increased emissions
* 🚑 Delays for emergency vehicles

This project explores an AI-based approach to make traffic management more responsive to current road conditions.

## 💡 Proposed Solution

The system processes traffic video using **YOLOv8** and **OpenCV**.

The basic workflow is:

```text
Traffic Video
      ↓
OpenCV
      ↓
YOLOv8 Object Detection
      ↓
Vehicle Detection / Traffic Analysis
      ↓
Traffic Condition
      ↓
Traffic Optimization
      ↓
Emergency Corridor
```

The project also includes an AI integration using the **Grok API** for intelligent assistance.

## 🧠 Technologies Used

* **Python**
* **YOLOv8**
* **OpenCV**
* **Ultralytics**
* **Grok API**
* **Streamlit**
* **Git & GitHub**

## 🚗 AI Traffic Detection

The project uses the **YOLOv8** object-detection model to process traffic video.

YOLO is used to detect vehicles from the video input.

The project contains:

```text
yolov8n.pt
```

which is the YOLOv8 nano model used by the prototype.

Traffic video files used for testing include:

```text
traffic_input.mp4
traffic_video.mp4
```

## 🚦 Traffic Management

After detecting vehicles, the system can use the traffic information to understand the current traffic condition.

The prototype contains a traffic optimization component:

```text
traffic_optimizer.py
```

The goal is to use the detected traffic condition to support better traffic signal decisions.

## 🚑 Emergency Green Corridor

A major feature of the project is the concept of an **Emergency Green Corridor**.

The idea is:

```text
🚑 Emergency Vehicle
        ↓
Detect emergency situation
        ↓
Identify required route
        ↓
Prioritize traffic signals
        ↓
🟢 Green Corridor
        ↓
Emergency vehicle moves faster
        ↓
Restore normal traffic
```

This can help reduce unnecessary delays for emergency vehicles.

## 🤖 Grok API Integration

The project also experiments with the **Grok API** to provide AI-based assistance within the traffic management system.

The AI component can be used alongside the traffic analysis system to support intelligent decision-making and interaction.

> API credentials should never be uploaded to GitHub. Store API keys in environment variables or a `.env` file and add `.env` to `.gitignore`.

## 🖥️ Application

The main Streamlit application is:

```text
app.py
```

Run the application with:

```bash
streamlit run app.py
```

## 📁 Project Structure

```text
ai-smart-traffic-management/
│
├── .gitignore
│
├── app.py
│
├── ai_engine.py
│
├── traffic_optimizer.py
│
├── test_ai.py
│
├── traffic_input.mp4
│
├── traffic_video.mp4
│
└── yolov8n.pt
```

### File Description

| File                   | Purpose                                              |
| ---------------------- | ---------------------------------------------------- |
| `app.py`               | Main Streamlit application                           |
| `ai_engine.py`         | AI-related processing                                |
| `traffic_optimizer.py` | Traffic optimization logic                           |
| `test_ai.py`           | Testing AI functionality                             |
| `yolov8n.pt`           | YOLOv8 nano model                                    |
| `traffic_input.mp4`    | Traffic video input                                  |
| `traffic_video.mp4`    | Traffic video used by the prototype                  |
| `.gitignore`           | Prevents unwanted files/secrets from being committed |

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/gobinath0105-lgtm/ai-smart-traffic-management.git
```

Go into the project:

```bash
cd ai-smart-traffic-management
```

Install the required Python packages:

```bash
pip install ultralytics opencv-python streamlit
```

Install any additional packages required by the AI/API components in the project.

## ▶️ Run the Project

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

## 🔬 Current Prototype

The current prototype demonstrates:

* YOLOv8-based vehicle detection
* OpenCV-based video processing
* Traffic analysis
* Traffic optimization logic
* Emergency corridor concept
* Streamlit interface
* Grok API integration

## 🚀 Future Improvements

Possible future improvements include:

* Real-time traffic-camera integration
* More accurate vehicle counting
* Multi-intersection coordination
* Improved traffic-flow simulation
* Dynamic signal timing
* Emergency vehicle detection
* Route optimization
* Traffic prediction
* More detailed fuel and CO₂ estimation
* Quantum optimization using QUBO/QAOA

## 👨‍💻 Project

**AI Smart Traffic Management & Emergency Corridor System**

Built as an AI/ML prototype for intelligent traffic management and emergency vehicle prioritization.
