import tkinter as tk
from tkinter import messagebox
from GPIO.EmulatorGUI import GPIO  # Thư viện GPIO cho Raspberry Pi hoặc mô phỏng
from GPIO.pnhLCD1602 import LCD1602
import time

# Khởi tạo GPIO
GPIO.setmode(GPIO.BCM)
LED_PIN = 18  # Chân điều khiển đèn LED
GPIO.setup(LED_PIN, GPIO.OUT)

# Khởi tạo LCD
lcd = LCD1602()

# Mã thẻ hợp lệ, bạn có thể thay đổi giá trị này khi cần
valid_rfid = '123456'

def open_lock():
    """Mở khóa và hiển thị thông báo trên LCD."""
    GPIO.output(LED_PIN, GPIO.HIGH)  # Bật đèn LED
    lcd.clear()
    lcd.write_string("Mo khoa")
    time.sleep(2)  # Giữ đèn LED bật trong 2 giây
    GPIO.output(LED_PIN, GPIO.LOW)  # Tắt đèn LED

def check_rfid():
    """Kiểm tra mã thẻ RFID nhập vào."""
    rfid_tag = rfid_entry.get()  # Lấy mã thẻ từ ô nhập văn bản
    if rfid_tag == valid_rfid:
        open_lock()  # Mở khóa nếu thẻ hợp lệ
        messagebox.showinfo("Thành công", "Khóa đã mở!")
    else:
        lcd.clear()
        lcd.write_string("Khong hop le")
        messagebox.showwarning("Thất bại", "Thẻ không hợp lệ!")

def set_rfid():
    """Cập nhật mã thẻ RFID hợp lệ."""
    global valid_rfid
    valid_rfid = password_entry.get()  # Lấy mã thẻ từ ô nhập văn bản
    messagebox.showinfo("Cập nhật thành công", "Mã thẻ đã được cập nhật!")

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Khóa Simulated")

# Tạo hộp mô phỏng ổ khóa
lock_box = tk.Frame(root, width=300, height=150, bg='grey')
lock_box.pack_propagate(False)  # Giữ kích thước cố định
lock_box.pack(pady=20)

# Tạo ô nhập văn bản cho mã thẻ
rfid_entry = tk.Entry(root, width=30, show='*')  # Ẩn ký tự đã nhập
rfid_entry.pack(pady=5)
rfid_entry.focus_set()  # Tự động đặt con trỏ vào ô nhập văn bản
rfid_entry.insert(0, "Nhập mã thẻ")  # Thêm hướng dẫn cho người dùng

# Tạo ô nhập văn bản cho việc cập nhật mã thẻ
password_entry = tk.Entry(root, width=30)  # Không ẩn ký tự, có thể hiển thị
password_entry.pack(pady=5)
password_entry.insert(0, "Nhập mã thẻ mới")  # Thêm hướng dẫn cho người dùng

# Tạo nút để cập nhật mã thẻ
set_button = tk.Button(root, text="Cập nhật thẻ", command=set_rfid)
set_button.pack(pady=5)

# Tạo nút để kiểm tra thẻ
check_button = tk.Button(root, text="Quẹt thẻ", command=check_rfid)
check_button.pack(pady=5)

# Bắt sự kiện đóng cửa sổ
def on_closing():
    GPIO.cleanup()  # Dọn dẹp tài nguyên GPIO
    lcd.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Bắt đầu vòng lặp chính
root.mainloop()
