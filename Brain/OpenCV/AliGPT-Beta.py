import cv2
import numpy as np
from collections import deque
import time

# =========================
# CONFIG
# =========================
W, H = 320, 240          # رزولوشن پایین برای سرعت
FRAME_INTERVAL = 0.4    # ثانیه
FLOW_TH = 1.5
EDGE_TH = 0.08

CLIMB_LIMIT = 2         # حداکثر تلاش برای بالا رفتن
MEMORY_LEN = 5

# =========================
# STATE
# =========================
state = "CRUISE"
climb_attempts = 0
history = deque(maxlen=MEMORY_LEN)

prev_gray = None
last_time = 0

# =========================
# UTILS
# =========================
def split_zones(img):
    h = img.shape[0]
    return img[int(h*0.6):, :], img[int(h*0.3):int(h*0.6), :], img[:int(h*0.3), :]

def edge_density(img):
    edges = cv2.Canny(img, 50, 150)
    return np.sum(edges > 0) / edges.size

def optical_flow(prev, curr):
    flow = cv2.calcOpticalFlowFarneback(
        prev, curr, None, 0.5, 3, 15, 3, 5, 1.2, 0
    )
    mag, _ = cv2.cartToPolar(flow[...,0], flow[...,1])
    return mag

# =========================
# MAIN ANALYSIS
# =========================
def analyze_environment(prev_gray, gray):
    flow = optical_flow(prev_gray, gray)

    low, mid, high = split_zones(gray)
    flow_low, flow_mid, flow_high = split_zones(flow)

    f_low = np.mean(flow_low)
    f_mid = np.mean(flow_mid)
    f_high = np.mean(flow_high)

    e_low = edge_density(low)

    # ارتفاع مانع
    if f_high > FLOW_TH:
        height = "HIGH"
    elif f_mid > FLOW_TH:
        height = "MID"
    else:
        height = "LOW"

    # شیب یا دیوار
    slope = (f_low > FLOW_TH and e_low < EDGE_TH)

    return height, slope, f_low

# =========================
# DECISION ENGINE (FSM)
# =========================
def decide(height, slope):
    global state, climb_attempts

    if state == "CRUISE":
        if height == "LOW":
            state = "CLIMB"
            climb_attempts += 1
            return "forward"
        if height == "MID":
            return "left"
        if height == "HIGH":
            return "right"

    if state == "CLIMB":
        if slope:
            return "forward"
        if climb_attempts >= CLIMB_LIMIT:
            state = "AVOID"
            return "left"
        return "forward"

    if state == "AVOID":
        state = "CRUISE"
        climb_attempts = 0
        return "right"

    return "forward"

# =========================
# MAIN LOOP
# =========================
cap = cv2.VideoCapture(0)
cap.set(3, W)
cap.set(4, H)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    now = time.time()
    if now - last_time < FRAME_INTERVAL:
        continue
    last_time = now

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if prev_gray is None:
        prev_gray = gray
        continue

    height, slope, danger = analyze_environment(prev_gray, gray)
    decision = decide(height, slope)

    history.append(decision)
    prev_gray = gray

    # =========================
    # VISUAL DEBUG
    # =========================
    cv2.putText(frame, f"STATE: {state}", (10,20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
    cv2.putText(frame, f"HEIGHT: {height}", (10,40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
    cv2.putText(frame, f"SLOPE: {slope}", (10,60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
    cv2.putText(frame, f"CMD: {decision}", (10,80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

    cv2.imshow("Crawler Vision", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
