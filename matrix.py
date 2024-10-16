import tkinter as tk

# test
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
    
    def key_pressed(self, key):
        # Xử lý khi phím được nhấn
        current_text = self.display.get()
        self.display.delete(0, tk.END)  # Xóa nội dung hiện tại
        self.display.insert(0, current_text + key)  # Thêm phím mới vào hiển thị


if __name__ == "__main__":
    root = tk.Tk()
    app = KeypadApp(root)
    root.mainloop()
