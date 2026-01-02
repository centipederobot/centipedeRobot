import cv2
import torch
import numpy as np
from ultralytics import YOLO

# ۱. بارگذاری مدل‌ها
yolo_model = YOLO("yolo11n.pt")
midas = torch.hub.load("intel-isl/MiDaS", "MiDaS_small")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
midas.to(device).eval()
transform = torch.hub.load("intel-isl/MiDaS", "transforms").small_transform

async def process_frame(frame):
    # الف) Resize و پردازش اولیه
    std_w, std_h = 640, 480
    img = cv2.resize(frame, (std_w, std_h))

    # ب) تشخیص اشیاء
    results = yolo_model(img, verbose=False)[0]

    # ج) تخمین عمق
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    input_batch = transform(img_rgb).to(device)
    with torch.no_grad():
        prediction = midas(input_batch)
        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1), size=(std_h, std_w), mode="bicubic", align_corners=False
        ).squeeze()

    depth = prediction.cpu().numpy()
    depth = (depth - depth.min()) / (depth.max() - depth.min() + 1e-5)

    # د) ایجاد نقشه هزینه (Cost Map) - ترکیب هوشمند
    # به جای میانگین، مقدار مینیمم (دورترین نقطه) در هر ستون را در ناحیه دید می‌گیریم
    # این باعث می‌شود شکاف‌های بین اشیاء بهتر دیده شوند
    scan_zone = depth[int(std_h*0.5):int(std_h*0.9), :]
    cost_line = np.min(scan_zone, axis=0)

    # اعمال موانع یولو روی نقشه هزینه با شدت بالا
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        if y2 > std_h * 0.4: # فقط موانع نیمه پایین
            cost_line[x1:x2] += 0.5 # جریمه سنگین برای وجود جسم صلب

    # ه) الگوریتم Sliding Window برای پیدا کردن دالان عبور
    robot_width = std_w // 4  # عرض فرضی ربات
    best_cost = 100
    target_x = std_w // 2

    # بررسی تمام دالان‌های ممکن برای عبور ربات
    for x in range(0, std_w - robot_width, 10):
        current_window_cost = np.mean(cost_line[x : x + robot_width])

        # اولویت‌دهی به مسیر مستقیم: اگر دالان به مرکز نزدیک بود، هزینه‌اش را کمتر فرض کن
        center_bias = abs((x + robot_width//2) - std_w//2) / std_w
        total_cost = current_window_cost + (center_bias * 0.2)

        if total_cost < best_cost:
            best_cost = total_cost
            target_x = x + robot_width // 2

    # و) تصمیم‌گیری نهایی
    decision = "forward"
    if best_cost > 0.8: # حتی بهترین راه هم مسدود است
        decision = "backward"
    elif target_x < std_w * 0.38:
        decision = "left"
    elif target_x > std_w * 0.62:
        decision = "right"
    else:
        decision = "forward"

    # ز) ویژوال‌سازی پیشرفته (Professional Dashboard)
    # ۱. تبدیل نقشه عمق به رنگی
    depth_viz = cv2.applyColorMap((depth * 255).astype(np.uint8), cv2.COLORMAP_JET)

    # ۲. ترکیب تصویر اصلی و نقشه عمق (برای دید بهتر)
    display_img = cv2.addWeighted(img, 0.6, depth_viz, 0.4, 0)

    # ۳. رسم باکس‌های YOLO با ضخامت کم
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cv2.rectangle(display_img, (x1, y1), (x2, y2), (255, 255, 255), 1)
        label = yolo_model.names[int(box.cls[0])]
        cv2.putText(display_img, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

    # ۴. رسم ناحیه اسکن (Scan Zone) به صورت نیمه‌شفاف
    overlay = display_img.copy()
    cv2.rectangle(overlay, (0, int(std_h*0.5)), (std_w, int(std_h*0.9)), (200, 200, 200), -1)
    display_img = cv2.addWeighted(overlay, 0.2, display_img, 0.8, 0)

    # ۵. رسم دالان عبور ربات (Target Path)
    color = (0, 255, 0) if decision != "backward" else (0, 0, 255)
    cv2.rectangle(display_img, (target_x - robot_width//2, int(std_h*0.5)),
                  (target_x + robot_width//2, int(std_h*0.9)), color, 2)

    # ۶. اضافه کردن پنل وضعیت (Status Bar)
    cv2.rectangle(display_img, (0, 0), (std_w, 60), (0, 0, 0), -1)

    # متن فرمان با رنگ متغیر
    cmd_colors = {"forward": (0, 255, 0), "left": (255, 165, 0), "right": (255, 165, 0), "backward": (0, 0, 255)}
    current_color = cmd_colors.get(decision, (255, 255, 255))

    cv2.putText(display_img, f"COMMAND: {decision.upper()}", (20, 40),
                cv2.FONT_HERSHEY_DUPLEX, 0.8, current_color, 2)
    cv2.putText(display_img, f"COST: {best_cost:.2f}", (std_w - 180, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

    # ۷. رسم نشانگر جهت در پایین تصویر
    center_pt = (std_w // 2, std_h - 30)
    target_pt = (target_x, std_h - 30)
    cv2.arrowedLine(display_img, center_pt, target_pt, (255, 255, 255), 3, tipLength=0.3)

    return display_img, decision