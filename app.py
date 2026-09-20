import streamlit as st
import cv2
import os
import time
from ultralytics import YOLO

from ai_engine import get_ai_analysis
from traffic_optimizer import optimize_traffic

# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="AI Smart Traffic Management System",
    page_icon="🚦",
    layout="wide"
)

st.title("🚦 AI Smart Traffic Management System")
st.caption("Computer Vision + Tracking + Traffic Analytics + AI")


# =========================================================
# LOAD YOLO
# =========================================================

@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")


model = load_model()


VEHICLE_CLASSES = {
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck"
}


# =========================================================
# FUNCTIONS
# =========================================================

def traffic_level(count):

    if count <= 5:
        return "LOW"

    elif count <= 12:
        return "MEDIUM"

    else:
        return "HIGH"


def calculate_green_time(count):

    green = 20 + (count * 2)

    return max(20, min(green, 60))


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("🚦 Traffic Control")

uploaded_file = st.sidebar.file_uploader(
    "Upload Traffic Video",
    type=["mp4", "avi", "mov", "mkv"]
)

st.sidebar.divider()


# =========================================================
# 🚑 EMERGENCY CORRIDOR
# =========================================================

st.sidebar.subheader("🚑 Emergency System")

emergency = st.sidebar.toggle(
    "Emergency Vehicle Detected"
)

emergency_road = st.sidebar.selectbox(
    "Emergency Vehicle Road",
    ["Road A", "Road B", "Road C", "Road D"]
)


# =========================================================
# NO VIDEO
# =========================================================

if uploaded_file is None:

    st.info("👈 Upload your traffic video.")

    st.stop()


# =========================================================
# SAVE VIDEO
# =========================================================

video_bytes = uploaded_file.read()

video_path = "traffic_input.mp4"

with open(video_path, "wb") as f:
    f.write(video_bytes)


# =========================================================
# OPEN VIDEO
# =========================================================

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():

    st.error("❌ Could not open video.")

    st.stop()


width = int(
    cap.get(cv2.CAP_PROP_FRAME_WIDTH)
)

height = int(
    cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
)

fps = cap.get(
    cv2.CAP_PROP_FPS
)

if fps <= 0:
    fps = 24


st.sidebar.write(
    f"Resolution: {width} × {height}"
)

st.sidebar.write(
    f"FPS: {fps:.2f}"
)


# =========================================================
# DASHBOARD
# =========================================================

st.divider()

st.subheader("🚦 Traffic Dashboard")

col1, col2, col3, col4 = st.columns(4)

road_a_box = col1.empty()
road_b_box = col2.empty()
road_c_box = col3.empty()
road_d_box = col4.empty()

status_box = st.empty()


# =========================================================
# SIGNAL
# =========================================================

st.divider()

signal_col1, signal_col2, signal_col3 = st.columns(3)

signal_box = signal_col1.empty()
green_box = signal_col2.empty()
emergency_box = signal_col3.empty()


# =========================================================
# VIDEO
# =========================================================

st.divider()

st.subheader("📹 Traffic Video")

video_box = st.empty()


# =========================================================
# AI
# =========================================================

st.divider()

st.subheader("🤖 AI Traffic Analysis")

ai_box = st.empty()


# =========================================================
# TRACKING
# =========================================================

road_counts = {
    "Road A": set(),
    "Road B": set(),
    "Road C": set(),
    "Road D": set()
}


# =========================================================
# AI TIMER
# =========================================================

last_ai_time = 0

ai_result = "Waiting for traffic data..."


# =========================================================
# VIDEO LOOP
# =========================================================

while True:

    success, frame = cap.read()

    if not success:
        break


    # =====================================================
    # YOLO TRACKING
    # =====================================================

    results = model.track(
        frame,
        persist=True,
        classes=list(VEHICLE_CLASSES.keys()),
        conf=0.15,
        imgsz=1280,
        verbose=False
    )


    current_detections = 0
    active_ids = 0
    intersection_count = 0


    # =====================================================
    # INTERSECTION AREA
    # =====================================================

    ix1 = int(width * 0.35)
    ix2 = int(width * 0.65)

    iy1 = int(height * 0.30)
    iy2 = int(height * 0.70)


    # =====================================================
    # VEHICLE DETECTION
    # =====================================================

    if results and results[0].boxes is not None:

        boxes = results[0].boxes


        for i in range(len(boxes)):

            if boxes.id is None:
                continue


            track_id = int(
                boxes.id[i].item()
            )

            active_ids += 1


            x1, y1, x2, y2 = boxes.xyxy[i].tolist()

            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)


            cx = int(
                (x1 + x2) / 2
            )

            cy = int(
                (y1 + y2) / 2
            )


            class_id = int(
                boxes.cls[i].item()
            )


            class_name = VEHICLE_CLASSES.get(
                class_id,
                "vehicle"
            )


            confidence = float(
                boxes.conf[i].item()
            )


            current_detections += 1


            # =================================================
            # INTERSECTION CHECK
            # =================================================

            inside_intersection = (

                ix1 <= cx <= ix2

                and

                iy1 <= cy <= iy2
            )


            if inside_intersection:

                intersection_count += 1

                road = "INTERSECTION"


            else:

                # =============================================
                # ROAD ASSIGNMENT
                # =============================================

                if cy < iy1:

                    road = "Road B"

                elif cy > iy2:

                    road = "Road D"

                elif cx < ix1:

                    road = "Road A"

                elif cx > ix2:

                    road = "Road C"

                else:

                    road = None


                if road is not None:

                    road_counts[road].add(
                        track_id
                    )


            # =================================================
            # DRAW VEHICLE BOX
            # =================================================

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (255, 255, 255),
                2
            )


            label = (
                f"{class_name} "
                f"ID:{track_id} "
                f"{confidence:.2f}"
            )


            cv2.putText(
                frame,
                label,
                (x1, max(y1 - 8, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                2
            )


            cv2.circle(
                frame,
                (cx, cy),
                4,
                (0, 255, 255),
                -1
            )


    # =========================================================
    # ROAD COUNTS
    # =========================================================

    count_a = len(
        road_counts["Road A"]
    )

    count_b = len(
        road_counts["Road B"]
    )

    count_c = len(
        road_counts["Road C"]
    )

    count_d = len(
        road_counts["Road D"]
    )


    counts = {
        "Road A": count_a,
        "Road B": count_b,
        "Road C": count_c,
        "Road D": count_d
    }
    


    # =========================================================
    # TRAFFIC LEVEL
    # =========================================================

    level_a = traffic_level(count_a)

    level_b = traffic_level(count_b)

    level_c = traffic_level(count_c)

    level_d = traffic_level(count_d)


    # =========================================================
    # HIGHEST TRAFFIC
    # =========================================================

    highest_road = max(
        counts,
        key=counts.get
    )

    highest_count = counts[
        highest_road
    ]


    # =========================================================
    # 🚑 EMERGENCY SIGNAL CONTROL
    # =========================================================

    if emergency:

        # Emergency road gets green

        current_signal = emergency_road

        green_time = 60

    else:

        # Normal traffic control

        current_signal = highest_road

        green_time = calculate_green_time(
            highest_count
        )


    # =========================================================
    # ROAD DASHBOARD
    # =========================================================

    road_a_box.metric(
        "🔵 Road A",
        f"{count_a} vehicles",
        level_a
    )

    road_b_box.metric(
        "🟢 Road B",
        f"{count_b} vehicles",
        level_b
    )

    road_c_box.metric(
        "🔴 Road C",
        f"{count_c} vehicles",
        level_c
    )

    road_d_box.metric(
        "🟡 Road D",
        f"{count_d} vehicles",
        level_d
    )


    # =========================================================
    # SIGNAL DASHBOARD
    # =========================================================

    signal_box.metric(
        "🚦 Current Signal",
        current_signal
    )

    green_box.metric(
        "🟢 Green Time",
        f"{green_time} sec"
    )


    # =========================================================
    # EMERGENCY STATUS
    # =========================================================

    if emergency:

        emergency_box.error(
            f"🚑 EMERGENCY CORRIDOR ACTIVE → {emergency_road}"
        )

    else:

        emergency_box.success(
            "Normal Traffic"
        )


    # =========================================================
    # STATUS
    # =========================================================

    status_box.info(
        f"🚗 Current detections: {current_detections} | "
        f"🎯 Active tracking IDs: {active_ids} | "
        f"🚦 Vehicles inside intersection: {intersection_count}"
    )


    # =========================================================
    # DRAW INTERSECTION
    # =========================================================

    cv2.rectangle(
        frame,
        (ix1, iy1),
        (ix2, iy2),
        (100, 100, 100),
        3
    )


    cv2.putText(
        frame,
        "INTERSECTION",
        (ix1 + 10, iy1 + 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )


    # =========================================================
    # ROAD LABELS
    # =========================================================

    cv2.putText(
        frame,
        "ROAD B",
        (width // 2 - 50, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )


    cv2.putText(
        frame,
        "ROAD D",
        (width // 2 - 50, height - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )


    cv2.putText(
        frame,
        "ROAD A",
        (20, height // 2),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )


    cv2.putText(
        frame,
        "ROAD C",
        (width - 120, height // 2),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )


    # =========================================================
    # AI ANALYSIS
    # =========================================================

    current_time = time.time()


    if current_time - last_ai_time > 8:

        traffic_data = {

            "Road A": count_a,

            "Road B": count_b,

            "Road C": count_c,

            "Road D": count_d,

            "Emergency": (
                f"YES - {emergency_road}"
                if emergency
                else "NO"
            ),

            "Current Signal":
                current_signal,

            "Green Time":
                green_time
        }


        ai_result = get_ai_analysis(
            traffic_data
        )


        last_ai_time = current_time


    ai_box.info(
        ai_result
    )


    # =========================================================
    # DISPLAY VIDEO
    # =========================================================

    display_width = 1000

    display_height = int(
        height *
        display_width /
        width
    )


    display_frame = cv2.resize(
        frame,
        (
            display_width,
            display_height
        )
    )


    display_frame = cv2.cvtColor(
        display_frame,
        cv2.COLOR_BGR2RGB
    )


    video_box.image(
        display_frame,
        channels="RGB",
        use_container_width=True
    )


    time.sleep(
        1 / fps
    )


# =========================================================
# END
# =========================================================

cap.release()

st.success(
    "✅ Traffic video processing completed."
)