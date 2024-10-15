import csv
import os
from datetime import datetime

# Hàm kiểm tra và tạo file CSV với tiêu đề cột
def create_csv_file_if_not_exists():
    if not os.path.exists('people_detection_log.csv'):
        with open('people_detection_log.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            # Ghi tiêu đề cột
            writer.writerow(['Thời gian', 'Số lượng người'])

# Hàm ghi thông tin vào file .csv
def log_person_data(person_count):
    with open('people_detection_log.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        writer.writerow([current_time, person_count])
        print(f"Ghi vào file CSV: Thời gian: {current_time}, Số người: {person_count}")

# Gọi hàm tạo file CSV nếu chưa tồn tại
create_csv_file_if_not_exists()
