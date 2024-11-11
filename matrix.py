import tkinter as tk
from EmulatorGUI import GPIO  # Import GPIO giả lập
import time
from GPIO.pnhLCD1602 import LCD1602  # Sử dụng LCD đã có sẵn

# Khởi tạo GPIO
GPIO.setmode(GPIO.BCM)

# Danh sách các GPIO
unlock_pin = 11  # Chân GPIO cho mở khóa
led_pin = 13  # Chân GPIO cho đèn LED báo thành công
buzzer_pin = 15  # Chân GPIO cho âm thanh
GPIO.setup(unlock_pin, GPIO.OUT)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(buzzer_pin, GPIO.OUT)

GPIO.output(unlock_pin, GPIO.LOW)  # Ban đầu đèn tắt
GPIO.output(led_pin, GPIO.LOW)     # Đèn LED tắt ban đầu
GPIO.output(buzzer_pin, GPIO.LOW)  # Tắt âm thanh ban đầu

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
                # Bỏ qua nút A và B để không cho phép chúng hoạt động
                if key in ['A', 'B']:
                    button = tk.Button(root, text=key, font=("Arial", 13), width=5, height=2, state=tk.DISABLED)
                else:
                    button = tk.Button(root, text=key, font=("Arial", 13), width=5, height=2,
                                       command=lambda k=key: self.key_pressed(k))
                button.grid(row=row_index + 1, column=col_index)

        # Danh sách để lưu trữ sáu ký tự cuối cùng
        self.key_sequence = []
        self.unlock_code = ['2', '7', '2', '0', '0', '3']  # Mã mở khóa ban đầu
        self.new_code = []  # Dùng để lưu mã mới khi thay đổi mật khẩu
        self.mode = "normal"  # Chế độ mặc định là "normal"

    def key_pressed(self, key):
        """Xử lý khi phím được nhấn"""
        # Chế độ bình thường (Nhập mật khẩu để mở khóa)
        if self.mode == "normal":
            if key == 'C':
                # Chuyển sang chế độ yêu cầu nhập mật khẩu cũ
                self.mode = "confirm_old_password"
                self.display.delete(0, tk.END)
                self.display.insert(0, "Enter Current Password")  # Nhập mật khẩu cũ
                print("Chế độ xác nhận mật khẩu cũ")
            elif key == 'D':
                # Xóa tất cả ký tự nhập
                self.clear_code()
            elif key == '#':
                # Xóa ký tự cuối cùng
                self.key_sequence = self.key_sequence[:-1]
                self.display.delete(0, tk.END)
                self.display.insert(0, ''.join(self.key_sequence))
                update_lcd_count(len(self.key_sequence))  # Cập nhật số ký tự hiển thị
            else:
                # Thêm ký tự vào danh sách và chỉ giữ lại 6 ký tự cuối
                self.key_sequence.append(key)
                if len(self.key_sequence) > 6:
                    self.key_sequence = self.key_sequence[-6:]
                
                self.display.delete(0, tk.END)
                self.display.insert(0, ''.join(self.key_sequence))
                update_lcd_count(len(self.key_sequence))  # Cập nhật số ký tự hiển thị

                # Kiểm tra xem có trùng với mã mở khóa không
                if self.key_sequence == self.unlock_code:
                    GPIO.output(unlock_pin, GPIO.HIGH)  # Bật đèn LED nếu đúng mã
                    self.display.delete(0, tk.END)
                    self.display.insert(0, "Unlock!")
                    print("Mở khóa thành công!")
                    time.sleep(1)
                    GPIO.output(unlock_pin, GPIO.LOW)  # Tắt đèn sau 1 giây
                else:
                    GPIO.output(unlock_pin, GPIO.LOW)  # Tắt đèn nếu mã không đúng

        # Chế độ xác nhận mật khẩu cũ (Confirm Old Password)
        elif self.mode == "confirm_old_password":
            if key == 'D':
                # Xóa tất cả ký tự nhập
                self.clear_code()
            elif key == '#':
                # Xóa ký tự cuối cùng
                self.key_sequence = self.key_sequence[:-1]
                self.display.delete(0, tk.END)
                self.display.insert(0, ''.join(self.key_sequence))
                update_lcd_count(len(self.key_sequence))  # Cập nhật số ký tự hiển thị
            elif len(self.key_sequence) < 6:
                # Tiếp tục nhập mật khẩu cũ
                self.key_sequence.append(key)
                self.display.delete(0, tk.END)
                self.display.insert(0, ''.join(self.key_sequence))
            elif len(self.key_sequence) == 6:
                if self.key_sequence == self.unlock_code:
                    # Nếu mật khẩu cũ đúng, chuyển sang chế độ nhập mật khẩu mới
                    self.display.delete(0, tk.END)
                    self.display.insert(0, "Enter New Password")  # Nhập mật khẩu mới
                    self.mode = "set_new_code"  # Chuyển sang chế độ nhập mật khẩu mới
                    self.key_sequence = []  # Xóa chuỗi ký tự nhập
                    print("Chuyển sang chế độ nhập mật khẩu mới")
                else:
                    # Nếu mật khẩu cũ sai
                    self.display.delete(0, tk.END)
                    self.display.insert(0, "Wrong Password")
                    time.sleep(1)
                    self.display.delete(0, tk.END)
                    self.display.insert(0, "Normal Mode")
                    self.mode = "normal"  # Quay lại chế độ bình thường

        # Chế độ nhập mật khẩu mới (Set New Password)
        elif self.mode == "set_new_code":
            if key == 'D':
                # Xóa tất cả ký tự nhập
                self.clear_code()
            elif key == '#':
                # Xóa ký tự cuối cùng
                self.key_sequence = self.key_sequence[:-1]
                self.display.delete(0, tk.END)
                self.display.insert(0, ''.join(self.key_sequence))
                update_lcd_count(len(self.key_sequence))  # Cập nhật số ký tự hiển thị
            elif len(self.key_sequence) < 6:
                # Tiếp tục nhập mật khẩu mới
                self.key_sequence.append(key)
                self.display.delete(0, tk.END)
                self.display.insert(0, ''.join(self.key_sequence))
            elif len(self.key_sequence) == 6:
                # Đã nhập đủ 6 ký tự mới
                self.unlock_code = self.key_sequence  # Cập nhật mã mở khóa với mã mới
                self.key_sequence = []
                self.display.delete(0, tk.END)
                self.display.insert(0, "Changed Password")  # Hiển thị thông báo mật khẩu đã thay đổi
                print("Mã mở khóa đã được thay đổi!")

                # Phản hồi thành công
                self.success_feedback()

                time.sleep(1)
                self.mode = "normal"  # Trở về chế độ bình thường

    def clear_code(self):
        """Chức năng xóa chuỗi nhập hiện tại"""
        self.key_sequence = []  # Xóa danh sách nhập
        self.display.delete(0, tk.END)  # Xóa màn hình
        print("Đã xóa chuỗi nhập!")

    def success_feedback(self):
        """Phản hồi thành công: Bật đèn LED và phát âm thanh khi thay đổi mật khẩu thành công"""
        GPIO.output(led_pin, GPIO.HIGH)  # Bật đèn LED
        GPIO.output(buzzer_pin, GPIO.HIGH)  # Phát âm thanh
        time.sleep(0.5)  # Đợi 0.5 giây
        GPIO.output(led_pin, GPIO.LOW)  # Tắt đèn LED
        GPIO.output(buzzer_pin, GPIO.LOW)  # Tắt âm thanh

# Hàm cập nhật số lượng ký tự nhập trên màn hình LCD
def update_lcd_count(count):
    lcd.clear()  # Xóa màn hình LCD
    lcd.set_cursor(0, 0)  # Đặt con trỏ ở dòng 0, cột 0
    lcd.write_string("So ky tu: " + str(count))  # In số ký tự đã nhập lên LCD

if __name__ == "__main__":
    root = tk.Tk()
    app = KeypadApp(root)
    root.mainloop()
    GPIO.cleanup()  # Dọn dẹp GPIO khi thoát chương trình
