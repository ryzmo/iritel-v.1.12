import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

import torch
import cv2
import time
import csv
from datetime import datetime

# Load YOLOv5 model
print("Memuat model YOLOv5...")
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Open camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Gagal membuka kamera.")
    exit()

# Define rack zones (each with unique product type)
racks = {
    "Rak A - Snack":   {"area": (30, 100, 100, 200), "produk": "Snack"},
    "Rak A - Minuman": {"area": (30, 210, 100, 300), "produk": "Minuman"},
    "Rak A - Buah":    {"area": (30, 310, 100, 400), "produk": "Buah"},
    "Rak B - Minuman": {"area": (540, 30, 620, 90),  "produk": "Minuman"},
    "Rak B - Sereal":  {"area": (540, 100, 620, 150),"produk": "Sereal"}
}

# Prepare logging
log_file = "interaksi_log.csv"
try:
    with open(log_file, 'x', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "rak", "produk", "durasi_detik"])
except FileExistsError:
    pass

# Initialize interaction states
interaction_states = {rak: {"start_time": None, "ongoing": False, "duration": 0} for rak in racks}

# Function to check overlap
def is_overlap(box1, box2):
    x1_min, y1_min, x1_max, y1_max = box1
    x2_min, y2_min, x2_max, y2_max = box2
    return not (x1_max < x2_min or x2_max < x1_min or y1_max < y2_min or y2_max < y1_min)

print("✅ Sistem siap. Tekan 'q' untuk keluar.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ Tidak bisa membaca frame dari kamera.")
        break

    results = model(frame)
    frame_with_boxes = results.render()[0].copy()

    person_boxes = [tuple(map(int, det[:4])) for det in results.xyxy[0] if int(det[5]) == 0]

    for rak_label, rak_info in racks.items():
        x1, y1, x2, y2 = rak_info["area"]
        produk = rak_info["produk"]

        # Jumlah orang di depan zona rak
        count = sum(is_overlap(box, rak_info["area"]) for box in person_boxes)
        interaction = count > 0

        color = (0, 255, 0) if interaction else (0, 0, 255)

        # Draw rack zone rectangles and labels
        cv2.rectangle(frame_with_boxes, (x1, y1), (x2, y2), color, 2)
        label = f"{rak_label}"
        cv2.putText(frame_with_boxes, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # Draw count of people
        cv2.putText(frame_with_boxes, f"{count} orang", (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # Show duration if interacting
        state = interaction_states[rak_label]
        if interaction:
            if not state["ongoing"]:
                state["start_time"] = time.time()
                state["ongoing"] = True
            else:
                state["duration"] = time.time() - state["start_time"]
                cv2.putText(frame_with_boxes, f"Durasi: {int(state['duration'])} dtk", (x1, y2 + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        elif not interaction and state["ongoing"]:
            duration = state["duration"]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Interaksi {rak_label} ({produk}) selama {duration:.2f} detik.")
            with open(log_file, 'a', newline='') as f:
                csv.writer(f).writerow([timestamp, rak_label, produk, f"{duration:.2f}"])
            state["ongoing"] = False
            state["duration"] = 0

    cv2.imshow("Interaksi Produk - Smart Retail", frame_with_boxes)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("🛑 Program dihentikan.")
