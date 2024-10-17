import csv
import os
from datetime import datetime
import time

# Biến để theo dõi thời gian đã ghi vào file CSV
last_log_time = None

# Hàm kiểm tra và tạo file CSV với tiêu đề cột
def create_csv_file_if_not_exists():
    # Luôn tạo lại file mới để đảm bảo tiêu đề cột
    with open('people_detection_log.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        # Ghi tiêu đề cột với khoảng cách
        writer.writerow(['Date      ', 'Time    ', 'Person Count'])  # Thêm khoảng trắng vào tên cột

# Hàm ghi thông tin vào file .csv
def log_person_data(person_count):
    global last_log_time
    current_time = datetime.now()
    date_str = current_time.strftime('%Y-%m-%d')
    time_str = current_time.strftime('%H:%M:%S')

    # Chỉ ghi vào CSV nếu thời gian hiện tại khác với thời gian đã ghi
    if last_log_time is None or (datetime.now() - last_log_time).seconds >= 1:
        with open('people_detection_log.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            # Ghi dữ liệu với khoảng trắng giữa các giá trị
            writer.writerow([f"{date_str:<10}", f"{time_str:<8}", f"{person_count:<12}"])  # Định dạng với khoảng trắng
            last_log_time = datetime.now()  # Cập nhật thời gian ghi
            print(f"Ghi vào file CSV: Ngày: {date_str}, Thời gian: {time_str}, Số người: {person_count}")

# Gọi hàm tạo file CSV và ghi tiêu đề cột
create_csv_file_if_not_exists()

