import os
import cv2
from ultralytics import YOLO
import threading
import time
from datetime import datetime
from GPIO.EmulatorGUI import GPIO
import winsound  # Phát âm thanh trên Windows, sử dụng thư viện khác cho Linux/MacOS
from GPIO.lcd import display_lcd
from GPIO.pnhLCD1602 import LCD1602
from log_csv import log_person_data  # Import hàm ghi dữ liệu vào CSV

# Khởi tạo GPIO
GPIO.setmode(GPIO.BCM)

# Danh sách các GPIO
GPIONames = [14, 15, 18, 23, 24, 25, 8, 7]  # Thay đổi theo chân bạn đang sử dụng

# Thiết lập chân GPIO
for pin in GPIONames:
    GPIO.setup(pin, GPIO.OUT)

# Tạo đối tượng YOLO
model = YOLO("yolov8n.pt")  # Chọn phiên bản YOLO thích hợp

# Khởi tạo video capture
cap = cv2.VideoCapture(0)

# Kiểm tra nếu camera mở thành công
if not cap.isOpened():
    print("Không thể truy cập camera.")
    exit()

# Tạo VideoWriter để lưu video với timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_video_path = os.path.join("videos", f'output_{timestamp}.avi')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_video_path, fourcc, 20.0, (640, 480))

# Hàm điều khiển LED và phát âm thanh, đưa vào luồng riêng
def alert_person_detected():
    def alert():
        # Kiểm tra thời gian hiện tại
        current_time = datetime.now().time()
        start_time = datetime.strptime("10:00:00", "%H:%M:%S").time()
        end_time = datetime.strptime("16:00:00", "%H:%M:%S").time()

        # Chỉ bật LED và phát âm thanh nếu trong khoảng từ 10 giờ đến 16 giờ
        if start_time <= current_time <= end_time:
            GPIO.output(GPIONames[0], GPIO.HIGH)  # Bật đèn LED ở chân GPIO 14
            winsound.Beep(1000, 500)  # Phát âm thanh tần số 1000 Hz trong 500 ms (Chỉ trên Windows)
            time.sleep(0.5)
            GPIO.output(GPIONames[0], GPIO.LOW)  # Tắt đèn LED

    # Khởi chạy tác vụ trong một luồng mới để không chặn vòng lặp chính
    threading.Thread(target=alert).start()

# Hàm cập nhật số lượng người và cảnh báo trên màn hình LCD
def update_lcd_count_and_alert(count):
    if count > 0:
        display_lcd("WARNING", f"NUMBER: {count}")
    else:
        display_lcd("SAFE", "NUMBER: 0")

# Hàm kiểm tra kích thước hộp bao (bounding box)
def is_person_box_valid(x1, y1, x2, y2):
    # Kiểm tra kích thước hộp bao có lớn hơn ngưỡng tối thiểu không (ví dụ: 50 pixel)
    width = x2 - x1
    height = y2 - y1
    return width > 50 and height > 100  # Điều chỉnh ngưỡng phù hợp với kích thước thực tế

# Lưu trữ vị trí đối tượng qua các khung hình để kiểm tra chuyển động
previous_positions = {}

# Biến lưu thời gian ghi video cuối cùng
last_record_time = 0

while True:
    # Đọc từng khung hình từ camera
    ret, frame = cap.read()

    if not ret:
        print("Không thể nhận khung hình.")
        break

    # Resize khung hình để cải thiện tốc độ xử lý
    frame_resized = cv2.resize(frame, (640, 480))  # Resize cho hiệu suất tốt hơn

    # Dò tìm người trong khung hình
    results = model(frame_resized)

    # Đếm số lượng người phát hiện được trong khung hình
    person_count_in_frame = 0
    for r in results:
        for box in r.boxes:
            if int(box.cls[0]) == 0:  # Lớp '0' là người
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # Kiểm tra điều kiện kích thước hộp bao để loại bỏ đối tượng quá nhỏ
                if is_person_box_valid(x1, y1, x2, y2):
                    # Tính toán trung tâm của hộp bao để theo dõi vị trí
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    person_id = f"{center_x}_{center_y}"

                    # Kiểm tra sự di chuyển của đối tượng qua các khung hình
                    if person_id in previous_positions:
                        prev_x, prev_y = previous_positions[person_id]
                        movement = abs(center_x - prev_x) + abs(center_y - prev_y)
                        if movement < 20:  # Nếu đối tượng không di chuyển nhiều, bỏ qua
                            continue
                    
                    # Cập nhật vị trí hiện tại
                    previous_positions[person_id] = (center_x, center_y)

                    # Nếu đối tượng đạt yêu cầu, vẽ hình chữ nhật và tăng biến đếm
                    person_count_in_frame += 1
                    cv2.rectangle(frame_resized, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Vẽ hình chữ nhật xung quanh người

    # Nếu phát hiện người, gọi hàm thông báo và lưu video
    current_time = time.time()
    if person_count_in_frame > 0 and current_time - last_record_time >= 1:
        alert_person_detected()  # Kích hoạt cảnh báo
        out.write(frame_resized)  # Ghi khung hình vào video
        last_record_time = current_time  # Cập nhật thời gian ghi cuối cùng

    # Ghi số lượng người vào file CSV
    log_person_data(person_count_in_frame)  # Ghi số lượng người vào CSV

    # Cập nhật số người hiện tại trên LCD
    update_lcd_count_and_alert(person_count_in_frame)  # Cập nhật số lượng người và cảnh báo trên LCD

    # Hiển thị khung hình đã xử lý
    cv2.imshow('People Detection with YOLOv8', frame_resized)

    # Thoát khi nhấn phím 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
out.release()
cv2.destroyAllWindows()
GPIO.cleanup()
