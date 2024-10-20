import tkinter as tk
import random
import time

# Giả lập danh sách thẻ RFID đã biết
known_tags = {
    "123456": "Người dùng 1",
    "654321": "Người dùng 2",
    "111222": "Người dùng 3"
}

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

    def scan_tag(self):
        tag_id = self.entry.get()
        self.entry.delete(0, tk.END)  # Xóa ô nhập liệu
        
        # Kiểm tra thẻ đã biết
        if tag_id in known_tags:
            self.result_label.config(text=f"Thẻ RFID hợp lệ: {known_tags[tag_id]}")
        else:
            self.result_label.config(text="Thẻ RFID không hợp lệ!")
        
        # Giả lập thời gian chờ khi quét thẻ
        time.sleep(1)

if __name__ == "__main__":
    root = tk.Tk()
    app = RFIDSimulatorApp(root)
    root.mainloop()
