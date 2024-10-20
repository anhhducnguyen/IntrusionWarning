import tkinter as tk
import time
from GPIO.EmulatorGUI import GPIO  # Thay vì gpiozero

# Giả lập danh sách thẻ RFID đã biết
known_tags = {
    "123456": "Người dùng 1",
    "654321": "Người dùng 2",
    "111222": "Người dùng 3"
}

# Định nghĩa các chân GPIO
LED_PIN = 11
DOOR_PIN = 5

# Khởi tạo GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(DOOR_PIN, GPIO.OUT)

# Class để giả lập hệ thống RFID
class RFIDSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Giả lập hệ thống RFID")
        
        # Hiển thị thông tin
        self.info_label = tk.Label(root, text="Quét thẻ RFID", font=("Arial", 24))
        self.info_label.pack(pady=20)
        
        # Ô nhập liệu cho mã thẻ
        self.entry = tk.Entry(root, font=("Arial", 18), justify='center')
        self.entry.pack(pady=10)
        
        # Nút quét thẻ
        self.scan_button = tk.Button(root, text="Quét Thẻ", font=("Arial", 18), command=self.scan_tag)
        self.scan_button.pack(pady=10)
        
        # Khu vực hiển thị kết quả
        self.result_label = tk.Label(root, text="", font=("Arial", 18))
        self.result_label.pack(pady=20)

    # Hàm xử lý quét thẻ
    def scan_tag(self):
        tag_id = self.entry.get()  # Lấy mã thẻ từ ô nhập liệu
        self.entry.delete(0, tk.END)  # Xóa ô nhập liệu sau khi nhập
        
        # Kiểm tra thẻ đã biết
        if tag_id in known_tags:
            self.result_label.config(text=f"Thẻ RFID hợp lệ: {known_tags[tag_id]}")
            self.activate_led_and_door()
        else:
            self.result_label.config(text="Thẻ RFID không hợp lệ!")
    
    # Hàm bật LED và đóng cửa khi quét thẻ hợp lệ
    def activate_led_and_door(self):
        # Bật LED (chân 11) trong 3 giây để báo hiệu quẹt thẻ thành công
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(LED_PIN, GPIO.LOW)
        
        # Đóng cửa (chân 5) trong 2 giây
        GPIO.output(DOOR_PIN, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(DOOR_PIN, GPIO.LOW)

if __name__ == "__main__":
    root = tk.Tk()
    app = RFIDSimulatorApp(root)
    root.mainloop()

    # Sau khi hoàn thành
    GPIO.cleanup()
