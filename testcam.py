import cv2
from ultralytics import YOLO
import threading
import tkinter as tk
import time
from datetime import datetime
from EmulatorGUI import GPIO
import winsound  # Phát âm thanh trên Windows, sử dụng thư viện khác cho Linux/MacOS
from pnhLCD1602 import LCD1602

# Khởi tạo GPIO
GPIO.setmode(GPIO.BCM)

# Danh sách các GPIO
GPIONames = [14, 15, 18, 23, 24, 25, 8, 7]  # Thay đổi theo chân bạn đang sử dụng

# Thiết lập chân GPIO
for pin in GPIONames:
    GPIO.setup(pin, GPIO.OUT)

# Khởi tạo LCD
lcd = LCD1602() 

# Biến đếm số người phát hiện được
person_count = 0
was_person_detected = False  # Biến theo dõi trạng thái phát hiện người trước đó

# Tạo đối tượng YOLO
model = YOLO("yolov8n.pt")  # Chọn phiên bản YOLO thích hợp

cap = cv2.VideoCapture(0)

# Kiểm tra nếu camera mở thành công
if not cap.isOpened():
    print("Không thể truy cập camera.")
    exit()

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

# Class điều khiển giao diện LED và hiển thị trạng thái phát hiện người
class LEDController(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.person_detected = False
        self.start()

    def run(self):
        self.root = tk.Tk()
        self.root.wm_title("Camera giám sát an ninh")

        # Label để hiển thị trạng thái phát hiện người
        self.status_label = tk.Label(self.root, text="Không phát hiện được người nào", font=("Arial", 18))
        self.status_label.pack(pady=20)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def update_status(self, detected):
        # Cập nhật thông báo trên GUI
        self.person_detected = detected
        if detected:
            self.status_label.config(text="Đã phát hiện người!", fg="green")
        else:
            self.status_label.config(text="Không phát hiện được người nào", fg="red")

    def on_close(self):
        GPIO.cleanup()
        self.root.destroy()

# Hàm cập nhật số lượng người trên màn hình LCD
def update_lcd_count(count):
    lcd.clear()  # Xóa màn hình LCD
    lcd.set_cursor(0, 0)  # Đặt con trỏ ở dòng 0, cột 0
    lcd.print("So nguoi: " + str(count))  # In số lượng người lên LCD

# Khởi tạo luồng điều khiển LED và GUI
app = LEDController()

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

    # Kiểm tra xem có phát hiện người không
    person_detected = False
    for r in results:
        for box in r.boxes:
            if int(box.cls[0]) == 0:  # Lớp '0' là người
                person_detected = True
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame_resized, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    # Nếu phát hiện người và trước đó chưa phát hiện, tăng biến đếm và báo hiệu
    if person_detected and not was_person_detected:
        person_count += 1
        alert_person_detected()
        update_lcd_count(person_count)  # Cập nhật số lượng người trên LCD
    
    # Cập nhật trạng thái vào giao diện GUI
    app.update_status(person_detected)

    # Cập nhật trạng thái phát hiện người của khung hình hiện tại
    was_person_detected = person_detected

    # Hiển thị khung hình đã xử lý
    cv2.imshow('People Detection with YOLOv8', frame_resized)

    # Thoát khi nhấn phím 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()
