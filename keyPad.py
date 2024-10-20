

import time
import tkinter as tk
import threading
from gpio_control import display_lcd_password, display_lcd
from GPIO.EmulatorGUI import GPIO  # Sử dụng EmulatorGUI cho mô phỏng GPIO

DOOR_SENSOR_PIN = 5  
DOOR_PIN = 11  

door_open = False
door_lock = threading.Lock()  # Tạo lock để bảo vệ biến door_open

# Giả lập hàm unlock_door để mở cửa
def unlock_door():
    global door_open
    with door_lock:
        GPIO.output(DOOR_PIN, GPIO.HIGH)  # Bật LED trên chân 11
        print("Cửa đã được mở!")          # Thay bằng hành động mở cửa thực tế
        door_open = True  # Cập nhật trạng thái cửa

def monitor_door_thread():
    global door_open
    door_state_last = GPIO.input(DOOR_SENSOR_PIN)  # Lưu trạng thái cửa ban đầu
    while True:
        door_state = GPIO.input(DOOR_SENSOR_PIN)
        print(f"Door state: {door_state}, Door open: {door_open}")  # Debug trạng thái cửa

        with door_lock:
            if door_open and door_state == GPIO.LOW:
                GPIO.output(DOOR_PIN, GPIO.LOW)
                display_lcd("   DOOR CLOSED", "")
                door_open = False
            elif not door_open and door_state == GPIO.HIGH and door_state_last == GPIO.LOW:
                display_lcd("   DOOR OPENED", "   PLEASE CLOSE")
                door_open = True

        door_state_last = door_state  # Cập nhật trạng thái cửa
        time.sleep(0.1)

class KeypadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Keypad 4x4")
        
        # Biến để lưu trữ chuỗi ký tự đã nhập
        self.input_text = ""
        self.password = "A12345"  # Mật khẩu cố định để mở cửa
        
        # Ma trận bàn phím 4x4
        self.keys = [
            ['1', '2', '3', 'A'],
            ['4', '5', '6', 'B'],
            ['7', '8', '9', 'C'],
            ['*', '0', '#', 'D']
        ]
        
        # Tạo các nút cho bàn phím với màu sắc, thêm padding và border
        for row_index, row in enumerate(self.keys):
            for col_index, key in enumerate(row):
                # Màu cho các phím
                if key in ['A', 'B', 'C', 'D', '*', '#']:
                    button_color = '#FF5733'  # Màu đỏ
                else:
                    button_color = '#007BFF'  # Màu xanh dương

                button = tk.Button(root, text=key, font=("Arial", 10, "bold"), width=4, height=1,
                                   bg=button_color, fg="white",
                                   padx=8, pady=8,
                                   bd=3,
                                   command=lambda k=key: self.key_pressed(k))
                button.grid(row=row_index + 1, column=col_index, padx=5, pady=5)

    def key_pressed(self, key):
        if key == 'C': 
            self.input_text = ""  # Xóa chuỗi khi nhấn 'C'
        elif key == '#':  # Nhấn '#' để xác nhận chuỗi đã nhập
            # Lấy 6 ký tự cuối cùng của input_text
            if len(self.input_text) >= 6:
                input_password = self.input_text[-6:]  # Lấy 6 ký tự cuối
            else:
                input_password = self.input_text  # Nếu ít hơn 6 ký tự, dùng toàn bộ
            
            if input_password == self.password:
                unlock_door()  # Gọi hàm mở cửa
                display_lcd_password("   DOOR OPENED", " CORRECT PASSWORD")
            else:
                display_lcd_password("   DOOR CLOSED", " WRONG PASSWORD")
            self.input_text = ""  # Reset input_text sau khi xác nhận
        else:
            self.input_text += key  # Thêm ký tự mới vào chuỗi
        
        # Thay thế số đã nhập bằng ký tự '*'
        masked_input = '*' * len(self.input_text)
        
        display_lcd(masked_input, "")

if __name__ == "__main__":
    root = tk.Tk()
    app = KeypadApp(root)

    # Khởi động luồng giám sát cửa
    monitoring_thread = threading.Thread(target=monitor_door_thread, daemon=True)
    monitoring_thread.start()

    root.mainloop()

    # Dọn dẹp GPIO sau khi thoát
    GPIO.cleanup()
