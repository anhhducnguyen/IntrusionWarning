import time
from pnhLCD1602 import LCD1602  # For LCD display simulation

lcd = LCD1602()

# Hàm hiển thị thông báo lên màn hình LCD
def display_lcd(person_detected):
    lcd.clear()
    
    # Nếu phát hiện người, hiển thị thông báo cảnh báo
    if person_detected:
        lcd.set_cursor(0, 0)
        lcd.write_string("Cảnh báo!")
        lcd.set_cursor(1, 0)
        lcd.write_string("Co nguoi xuat hien")
    else:
        lcd.set_cursor(0, 0)
        lcd.write_string("Khong co nguoi")
        lcd.set_cursor(1, 0)
        lcd.write_string("nao xuat hien")
    
    time.sleep(5)  # Giữ màn hình hiển thị trong 5 giây
    lcd.clear()    # Sau 5 giây, xóa màn hình

# Giả lập phát hiện người
person_detected = True  # Đặt thành False nếu không phát hiện người
display_lcd(person_detected)
