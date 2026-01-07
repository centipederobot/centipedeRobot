import cv2
import asyncio
import numpy as np
import onnxruntime as ort
import torch
from ultralytics import YOLO
import os, time

# --- تنظیمات ابعاد ---
std_w, std_h = 640, 480 

async def setup_models():
    if not os.path.exists("yolo11n.onnx"):
        print("📥 Exporting YOLO...")
        YOLO("yolo11n.pt").export(format="onnx", imgsz=640)
    
    if not os.path.exists("midas_small.onnx"):
        print("📥 Exporting MiDaS...")
        midas = torch.hub.load("intel-isl/MiDaS", "MiDaS_small").cpu()
        midas.eval()
        # اینجا نام ورودی را عمداً 'x' می‌گذاریم تا با سخت‌گیرترین حالت سازگار باشد
        torch.onnx.export(midas, torch.randn(1, 3, 256, 256), "midas_small.onnx", 
                          opset_version=11, input_names=['x'])

# اجرای دانلود/تبدیل قبل از تعریف سشن‌ها
if not os.path.exists("yolo11n.onnx") or not os.path.exists("midas_small.onnx"):
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(setup_models())

# لود کردن سشن‌ها
providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
y_sess = ort.InferenceSession("yolo11n.onnx", providers=providers)
m_sess = ort.InferenceSession("midas_small.onnx", providers=providers)

# راه حل نهایی برای خطا: پیدا کردن نام ورودی واقعی مدل در حافظه
m_input_name = m_sess.get_inputs()[0].name 
print(f"✅ MiDaS Input Name Detected: {m_input_name}")

async def process_yolo_onnx(img):
    blob = cv2.resize(img, (640, 640)).transpose(2, 0, 1)[np.newaxis, ...].astype(np.float32) / 255.0
    # YOLO معمولاً نام ورودی‌اش 'images' است
    preds = y_sess.run(None, {y_sess.get_inputs()[0].name: blob})[0]
    return preds[0].T 

async def process_midas_onnx(img):
    blob = cv2.resize(img, (256, 256)).transpose(2, 0, 1)[np.newaxis, ...].astype(np.float32) / 255.0
    # استفاده از نام شناسایی شده (چه x باشد چه input چه هر چیز دیگر)
    depth = m_sess.run(None, {m_input_name: blob})[0][0]
    
    # استخراج خط هزینه (منطق رادار) برای سرعت
    scan_zone = depth[128:230, :] 
    cost_line_small = np.max(scan_zone, axis=0)
    cost_line = cv2.resize(cost_line_small.reshape(1, -1), (std_w, 1))[0]
    cost_line = (cost_line - cost_line.min()) / (cost_line.max() - cost_line.min() + 1e-5)
    
    return cost_line, depth

async def process_frame(frame):
    img = cv2.resize(frame, (std_w, std_h))
    
    # اجرای موازی
    yolo_task = process_yolo_onnx(img)
    midas_task = process_midas_onnx(img)
    yolo_results, (cost_line, depth_small) = await asyncio.gather(yolo_task, midas_task)

    # جریمه YOLO
    for res in yolo_results:
        if res[4] > 0.4:
            x, y, w, h = res[:4]
            x1, x2 = int(x - w/2), int(x + w/2)
            y2 = int(y + h/2)
            if y2 > std_h * 0.4: 
                cost_line[max(0, x1):min(std_w, x2)] += 0.5

    # پنجره لغزان
    robot_width = std_w // 4 
    best_cost, target_x = 100, std_w // 2
    for x in range(0, std_w - robot_width, 15):
        current_cost = np.mean(cost_line[x : x + robot_width])
        bias = abs((x + robot_width//2) - std_w//2) / std_w
        total = current_cost + (bias * 0.2)
        if total < best_cost:
            best_cost, target_x = total, x + robot_width // 2

    # تصمیم
    if best_cost > 0.8: decision = "backward"
    elif target_x < std_w * 0.38: decision = "left"
    elif target_x > std_w * 0.62: decision = "right"
    else: decision = "forward"

    # بصری‌سازی (مطابق استایل شما)
    depth_full = cv2.resize(depth_small, (std_w, std_h))
    depth_viz = cv2.applyColorMap(cv2.normalize(depth_full, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8), cv2.COLORMAP_JET)
    display_img = cv2.addWeighted(img, 0.6, depth_viz, 0.4, 0)
    
    # مستطیل اسکن
    overlay = display_img.copy()
    cv2.rectangle(overlay, (0, int(std_h*0.5)), (std_w, int(std_h*0.9)), (200, 200, 200), -1)
    display_img = cv2.addWeighted(overlay, 0.2, display_img, 0.8, 0)

    color = (0, 255, 0) if decision != "backward" else (0, 0, 255)
    cv2.rectangle(display_img, (target_x - robot_width//2, int(std_h*0.5)), (target_x + robot_width//2, int(std_h*0.9)), color, 2)
    
    cv2.rectangle(display_img, (0, 0), (std_w, 60), (0, 0, 0), -1)
    cv2.putText(display_img, f"COMMAND: {decision.upper()}", (20, 40), cv2.FONT_HERSHEY_DUPLEX, 0.8, color, 2)
    cv2.arrowedLine(display_img, (std_w // 2, std_h - 30), (target_x, std_h - 30), (255, 255, 255), 3)

    return display_img, decision
