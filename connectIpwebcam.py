import cv2

# Địa chỉ IP của camera
ip_address = "192.168.1.6"    # Thay bằng địa chỉ IP của camera
port = "8080"                  # Thay bằng port nếu cần (có thể là 8080 hoặc 554)
video_path = "/video"          # Thay đổi nếu cần thiết

# Tạo URL kết nối
ip_camera_url = f"http://{ip_address}:{port}{video_path}"

# Mở kết nối đến camera IP
cap = cv2.VideoCapture(ip_camera_url)

if not cap.isOpened():
    print("Không thể mở camera IP")
    exit()

while True:
    # Đọc khung hình từ camera
    ret, frame = cap.read()
    
    if not ret:
        print("Không thể đọc khung hình từ camera")
        break
    
    # Hiển thị khung hình
    cv2.imshow('Camera IP', frame)
    
    # Thoát khi nhấn phím 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng camera và đóng cửa sổ
cap.release()
cv2.destroyAllWindows()
