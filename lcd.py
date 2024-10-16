import time
from pnhLCD1602 import LCD1602  # For LCD display simulation

lcd = LCD1602()

# def display_lcd(text_line1, text_line2):
#     lcd.clear()
#     lcd.set_cursor(0, 0)
#     lcd.write_string(text_line1)
#     lcd.set_cursor(1,4)
#     lcd.write_string(text_line2)
    
#     time.sleep(2)  
#     lcd.clear()    

# Hàm hiển thị thông báo lên màn hình LCD
# def display_lcd(person_detected):
#     lcd.clear()
    
#     # Nếu phát hiện người, hiển thị thông báo cảnh báo
#     if person_detected:
#         lcd.set_cursor(0, 0)
#         lcd.write_string("Cảnh báo!")
#         lcd.set_cursor(1, 0)
#         lcd.write_string("Co nguoi xuat hien")
#     else:
#         lcd.set_cursor(0, 0)
#         lcd.write_string("Khong co nguoi")
#         lcd.set_cursor(1, 0)
#         lcd.write_string("nao xuat hien")
    
#     time.sleep(5)  # Giữ màn hình hiển thị trong 5 giây
#     lcd.clear()    # Sau 5 giây, xóa màn hình

# # Giả lập phát hiện người
# person_detected = True  # Đặt thành False nếu không phát hiện người
# display_lcd(person_detected)


# Hàm cập nhật LCD
def display_lcd_warning(person_detected):
    lcd.clear()
    if person_detected:
        lcd.write_string("Canh bao!")
        lcd.set_cursor(1, 0)
        lcd.write_string("Co nguoi xuat hien")
    else:
        lcd.write_string("Khong co nguoi")
        lcd.set_cursor(1, 0)
        lcd.write_string("nao xuat hien")
    time.sleep(1)  # Thời gian hiển thị ngắn hơn để tăng tốc
    lcd.clear()

