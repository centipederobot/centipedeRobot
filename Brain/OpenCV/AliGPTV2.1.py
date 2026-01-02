import cv2
import asyncio
import numpy as np
import onnxruntime as ort
import torch
from ultralytics import YOLO
import os


print("--- در حال آماده‌سازی مدل YOLO11 ---")
yolo_model = YOLO("yolo11n.pt")
yolo_model.export(format="onnx", imgsz=640)
print("✅ تبدیل به ONNX با موفقیت انجام شد.")
print("--- در حال تبدیل مدل MiDaS ---")
device = torch.device("cpu")
model_type = "MiDaS_small"
midas = torch.hub.load("intel-isl/MiDaS", model_type).to(device)
midas.eval()

dummy_input = torch.randn(1, 3, 256, 256).to(device)

try:
    torch.onnx.export(midas, 
                      dummy_input, 
                      "midas_small.onnx", 
                      export_params=True, 
                      opset_version=11, # نسخه پایدار برای اکثر سیستم‌ها
                      do_constant_folding=True, 
                      input_names=['input'], 
                      output_names=['output'],
                      dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}})
    print("✅ فایل midas_small.onnx با موفقیت ساخته شد.")
except Exception as e:
    print(f"❌ خطا در تبدیل: {e}")

providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
y_sess = ort.InferenceSession("yolo11n.onnx", providers=providers)
m_sess = ort.InferenceSession("midas_small.onnx", providers=providers)

std_w, std_h = 640, 480

async def process_yolo_onnx(img):
    blob = cv2.resize(img, (640, 640)).transpose(2, 0, 1)[np.newaxis, ...].astype(np.float32) / 255.0
    preds = y_sess.run(None, {"images": blob})[0]
    return preds[0].T 
async def process_midas_onnx(img):
    blob = cv2.resize(img, (256, 256)).transpose(2, 0, 1)[np.newaxis, ...].astype(np.float32) / 255.0
    depth = m_sess.run(None, {"input": blob})[0]
    depth = cv2.resize(depth[0], (std_w, std_h))
    depth = (depth - depth.min()) / (depth.max() - depth.min() + 1e-5)
    return depth

async def process_frame(frame):
    img = cv2.resize(frame, (std_w, std_h))

    # الف) اجرای همزمان دو مدل با سرعت ONNX
    yolo_results, depth = await asyncio.gather(
        process_yolo_onnx(img),
        process_midas_onnx(img)
    )

    # ب) بازگشت به منطق دقیق "نقشه هزینه" شما
    scan_zone = depth[int(std_h*0.5):int(std_h*0.9), :]
    cost_line = np.max(scan_zone, axis=0) # اصلاح شد: در MiDaS مقدار بیشتر یعنی جسم نزدیک‌تر

    # اعمال جریمه اشیاء شناسایی شده YOLO
    for res in yolo_results:
        conf = res[4]
        if conf > 0.4: # فیلتر دقت
            x, y, w, h = res[:4] # مختصات YOLO ONNX معمولاً مختصات مرکز و ابعاد است
            x1, x2 = int(x - w/2), int(x + w/2)
            y2 = int(y + h/2)
            if y2 > std_h * 0.4: 
                cost_line[max(0, x1):min(std_w, x2)] += 0.5

    # ج) الگوریتم پنجره لغزان و انحراف از مرکز (دقیقاً طبق کد شما)
    robot_width = std_w // 4 
    best_cost = 100
    target_x = std_w // 2

    for x in range(0, std_w - robot_width, 10):
        current_window_cost = np.mean(cost_line[x : x + robot_width])
        center_bias = abs((x + robot_width//2) - std_w//2) / std_w
        total_cost = current_window_cost + (center_bias * 0.2)

        if total_cost < best_cost:
            best_cost = total_cost
            target_x = x + robot_width // 2

    # د) منطق تصمیم‌گیری جهت‌ها
    if best_cost > 0.8: 
        decision = "backward"
    elif target_x < std_w * 0.38:
        decision = "left"
    elif target_x > std_w * 0.62:
        decision = "right"
    else:
        decision = "forward"

    # ه) بصری‌سازی پیشرفته (Overlay, Arrow, Boxes)
    depth_viz = cv2.applyColorMap((depth * 255).astype(np.uint8), cv2.COLORMAP_JET)
    display_img = cv2.addWeighted(img, 0.6, depth_viz, 0.4, 0)

    # لایه خاکستری ناحیه اسکن
    overlay = display_img.copy()
    cv2.rectangle(overlay, (0, int(std_h*0.5)), (std_w, int(std_h*0.9)), (200, 200, 200), -1)
    display_img = cv2.addWeighted(overlay, 0.2, display_img, 0.8, 0)

    # رسم مستطیل مسیر انتخاب شده
    color = (0, 255, 0) if decision != "backward" else (0, 0, 255)
    cv2.rectangle(display_img, (target_x - robot_width//2, int(std_h*0.5)),
                  (target_x + robot_width//2, int(std_h*0.9)), color, 2)

    # پنل اطلاعات بالا
    cv2.rectangle(display_img, (0, 0), (std_w, 60), (0, 0, 0), -1)
    cmd_colors = {"forward": (0, 255, 0), "left": (255, 165, 0), "right": (255, 165, 0), "backward": (0, 0, 255)}
    cv2.putText(display_img, f"COMMAND: {decision.upper()}", (20, 40),
                cv2.FONT_HERSHEY_DUPLEX, 0.8, cmd_colors.get(decision, (255,255,255)), 2)
    cv2.putText(display_img, f"COST: {best_cost:.2f}", (std_w - 180, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

    # رسم فلش راهنما
    cv2.arrowedLine(display_img, (std_w // 2, std_h - 30), (target_x, std_h - 30), (255, 255, 255), 3, tipLength=0.3)

    return display_img, decision