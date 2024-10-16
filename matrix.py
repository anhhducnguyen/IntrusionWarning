import tkinter as tk
from EmulatorGUI import GPIO  # Import GPIO giả lập
import time
from GPIO.pnhLCD1602 import LCD1602  # Sử dụng LCD đã có sẵn

# Khởi tạo GPIO
GPIO.setmode(GPIO.BCM)

# Danh sách các GPIO
unlock_pin = 11  # Chân GPIO cho mở khóa
GPIO.setup(unlock_pin, GPIO.OUT)
GPIO.output(unlock_pin, GPIO.LOW)  # Ban đầu đèn tắt

# Khởi tạo LCD
lcd = LCD1602()  # Khởi tạo đối tượng LCD

# Class điều khiển bàn phím ma trận 4x4
class KeypadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bàn phím ma trận 4x4")
        
        # Khung để hiển thị phím nhấn
        self.display = tk.Entry(root, font=("Arial", 24), width=10, justify='center')
        self.display.grid(row=0, column=0, columnspan=4)

        # Ma trận bàn phím 4x4
        self.keys = [
            ['1', '2', '3', 'A'],
            ['4', '5', '6', 'B'],
            ['7', '8', '9', 'C'],
            ['*', '0', '#', 'D']
        ]
        
        # Tạo các nút cho bàn phím
        for row_index, row in enumerate(self.keys):
            for col_index, key in enumerate(row):
                button = tk.Button(root, text=key, font=("Arial", 18), width=5, height=2,
                                   command=lambda k=key: self.key_pressed(k))
                button.grid(row=row_index + 1, column=col_index)

        # Danh sách để lưu trữ sáu ký tự cuối cùng
        self.key_sequence = []
        self.unlock_code = ['2', '7', '2', '0', '0', '3']  # Mã mở khóa

    def key_pressed(self, key):
        # Xử lý khi phím được nhấn
        current_text = self.display.get()
        self.display.delete(0, tk.END)
        self.display.insert(0, current_text + key)

        # Thêm ký tự vừa nhấn vào danh sách key_sequence
        self.key_sequence.append(key)
        if len(self.key_sequence) > 6:
            self.key_sequence.pop(0)  # Chỉ giữ lại 6 ký tự cuối cùng

        # Hiển thị số lượng ký tự nhập trên LCD
        update_lcd_count(len(self.key_sequence))  # Hiển thị số ký tự đã nhập

        # Kiểm tra xem có trùng với mã mở khóa không
        if self.key_sequence == self.unlock_code:
            GPIO.output(unlock_pin, GPIO.HIGH)  # Bật đèn LED nếu đúng mã
            self.display.delete(0, tk.END)  # Xóa màn hình sau khi mở khóa
            self.display.insert(0, "Mở khóa!")
            print("Mở khóa thành công!")
            time.sleep(1)
            GPIO.output(unlock_pin, GPIO.LOW)  # Tắt đèn sau 1 giây
        else:
            GPIO.output(unlock_pin, GPIO.LOW)  # Tắt đèn nếu mã không đúng

# Hàm cập nhật số lượng ký tự nhập trên màn hình LCD
def update_lcd_count(count):
    lcd.clear()  # Xóa màn hình LCD
    lcd.set_cursor(0, 0)  # Đặt con trỏ ở dòng 0, cột 0
    lcd.print("So ky tu: " + str(count))  # In số ký tự đã nhập lên LCD

if __name__ == "__main__":
    root = tk.Tk()
    app = KeypadApp(root)
    root.mainloop()
    GPIO.cleanup()  # Dọn dẹp GPIO khi thoát chương trình
