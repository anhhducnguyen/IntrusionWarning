import time
from GPIO.pnhLCD1602 import LCD1602  # For LCD display simulation

lcd = LCD1602()

def display_lcd(text_line1, text_line2):
    lcd.clear()
    lcd.set_cursor(0, 0)
    lcd.write_string(text_line1)
    lcd.set_cursor(1, 0)
    lcd.write_string(text_line2)


def display_lcd_password(text_line1, text_line2):
    lcd.clear()
    lcd.set_cursor(0, 0)
    lcd.write_string(text_line1)
    lcd.set_cursor(1, 0)
    lcd.write_string(text_line2)

    time.sleep(2)  # Giữ màn hình hiển thị trong 2 giây
    lcd.clear()    # Sau 2 giây, xóa màn hình