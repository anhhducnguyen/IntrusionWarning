import os
import cv2
from ultralytics import YOLO
import threading
import time
from datetime import datetime
# from GPIO.lcd import display_lcd_warning
from GPIO.pnhLCD1602 import LCD1602
from GPIO.EmulatorGUI import GPIO  # Thư viện GPIO cho Raspberry Pi hoặc mô phỏng

# Tạo thư mục "videos" nếu chưa tồn tại
video_folder = "videos"
if not os.path.exists(video_folder):
    os.makedirs(video_folder)

# Khởi tạo GPIO
GPIO.setmode(GPIO.BCM)
LED_PIN = 18  # Chân điều khiển đèn LED
GPIO.setup(LED_PIN, GPIO.OUT)

# Khởi tạo LCD
lcd = LCD1602()

# Khởi tạo mô hình YOLO (nhẹ để cải thiện tốc độ)
model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(0)

# Kiểm tra nếu camera mở thành công
if not cap.isOpened():
    print("Không thể truy cập camera.")
    exit()

# Tạo VideoWriter để lưu video với timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_video_path = os.path.join(video_folder, f'output_{timestamp}.avi')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_video_path, fourcc, 20.0, (640, 480))

# Hàm điều khiển LED cảnh báo
def alert_person_detected():
    GPIO.output(LED_PIN, GPIO.HIGH)  # Bật LED
    time.sleep(0.5)
    GPIO.output(LED_PIN, GPIO.LOW)  # Tắt LED



# Biến lưu thời gian ghi video cuối cùng
last_record_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Không thể nhận khung hình.")
        break

    # Giảm kích thước khung hình để tăng tốc xử lý
    frame_resized = cv2.resize(frame, (640, 480))

    # Nhận diện người
    results = model(frame_resized, conf=0.4)  # Giảm ngưỡng tự tin nếu cần

    person_detected = False
    for r in results:
        for box in r.boxes:
            if int(box.cls[0]) == 0:  # Lớp '0' là người
                person_detected = True
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame_resized, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Nếu phát hiện người và đã qua ít nhất 1 giây từ lần ghi trước đó
    current_time = time.time()
    if person_detected and current_time - last_record_time >= 1:
        alert_person_detected()  # Kích hoạt cảnh báo
        out.write(frame_resized)  # Ghi khung hình vào video
        last_record_time = current_time  # Cập nhật thời gian ghi cuối cùng

    # Cập nhật thông tin trên LCD
    # display_lcd_warning(person_detected)

    # Hiển thị khung hình đã xử lý
    cv2.imshow('People Detection with YOLOv8', frame_resized)

    # Thoát khi nhấn phím 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
out.release()
cv2.destroyAllWindows()
lcd.close()
GPIO.cleanup()
