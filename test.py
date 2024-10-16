import RPi.GPIO as GPIO
import time
from pnhLCD1602 import LCD1602
from MFRC522 import SimpleMFRC522

# Khởi tạo GPIO
GPIO.setmode(GPIO.BCM)
LED_PIN = 18  # Chân điều khiển đèn LED
GPIO.setup(LED_PIN, GPIO.OUT)

# Khởi tạo LCD
lcd = LCD1602()

# Khởi tạo đọc thẻ RFID
reader = SimpleMFRC522()

try:
    while True:
        print("Đưa thẻ RFID gần đầu đọc...")
        id, text = reader.read()  # Đọc thẻ RFID
        print("ID thẻ:", id)
        
        # Kiểm tra ID và xác định hành động
        if id:  # Nếu có thẻ được đọc
            GPIO.output(LED_PIN, GPIO.HIGH)  # Bật đèn LED
            lcd.clear()
            lcd.write_string("Mo cua!")
            time.sleep(2)  # Thời gian mở cửa
            lcd.clear()
            lcd.write_string("Dong cua!")
            GPIO.output(LED_PIN, GPIO.LOW)  # Tắt đèn LED
            time.sleep(2)  # Thời gian cho LCD hiển thị trước khi quay lại
            lcd.clear()  # Xóa màn hình LCD

except KeyboardInterrupt:
    print("Chương trình dừng lại.")

finally:
    # Dọn dẹp tài nguyên GPIO
    GPIO.cleanup()
    lcd.close()
