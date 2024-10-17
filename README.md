# Smart-Lock System with FaceID and Intrusion Alert

## 1. Mở đầu
### 1.1. Giới thiệu tổng quan
Hệ thống khóa cửa thông minh ngày càng trở nên phổ biến với sự phát triển của công nghệ, đặc biệt là các tính năng nhận diện khuôn mặt và cảnh báo đột nhập. Hệ thống này mang lại nhiều lợi ích như tăng cường bảo mật, cải thiện sự tiện lợi và tích hợp khả năng điều khiển từ xa. Trong bối cảnh nhu cầu bảo mật và an ninh ngày càng cao, việc phát triển một hệ thống khóa cửa thông minh với FaceID và cảnh báo đột nhập là hết sức cần thiết.

#### 1.1.1. Mục tiêu và phạm vi
Mục tiêu của báo cáo này là trình bày chi tiết về thiết kế và triển khai một hệ thống khóa thông minh với tính năng nhận diện khuôn mặt và cảnh báo đột nhập. Báo cáo phân tích các yêu cầu của hệ thống, giới thiệu các giải pháp hiện tại và đề xuất hệ thống mới với các ưu điểm nổi bật hơn.

## 2. Kiến trúc hệ thống
### 2.1. Tổng quan về kiến trúc hệ thống
Hệ thống khóa thông minh bao gồm nhiều thành phần phần cứng và phần mềm phối hợp để đảm bảo hoạt động hiệu quả. Dưới đây là mô tả chi tiết các thành phần của hệ thống.

#### 2.1.1. Các thành phần của hệ thống
- **Cảm biến:** Dùng để phát hiện đột nhập, theo dõi môi trường và cung cấp dữ liệu thời gian thực.
- **Camera:** Được sử dụng cho tính năng nhận diện khuôn mặt.
- **Vi điều khiển:** Đóng vai trò như bộ xử lý trung tâm, điều khiển các hoạt động của toàn bộ hệ thống.
- **Module FaceID:** Hỗ trợ khả năng nhận diện khuôn mặt với độ chính xác cao.
- **Hệ thống cảnh báo:** Gửi tín hiệu cảnh báo khi có dấu hiệu đột nhập trái phép.
- **Thiết bị liên quan:** Bao gồm khóa cửa điện tử, giao diện điều khiển, và hệ thống điện dự phòng.

## 3. Thiết kế và triển khai phần cứng
### 3.1. Thiết kế phần cứng
Phần cứng là một phần quan trọng của hệ thống, đảm bảo sự phối hợp chính xác giữa các thiết bị để hoạt động ổn định và bảo mật.

#### 3.1.1. Chi tiết các linh kiện và sơ đồ kết nối
- **Cảm biến chuyển động PIR:** Phát hiện chuyển động trong khu vực được giám sát.
- **Camera:** Chụp ảnh và quay video khuôn mặt để tiến hành nhận diện.
- **Khóa cửa điện tử:** Được điều khiển bởi vi điều khiển để khóa/mở cửa khi có sự cho phép.
- **Hệ thống điều khiển GPIO:** Đảm bảo giao tiếp giữa vi điều khiển và các linh kiện khác như cảm biến và khóa cửa.
- **Sơ đồ mạch điện:** Được thiết kế để tối ưu hóa kết nối và đảm bảo sự ổn định trong quá trình sử dụng.

## 4. Thiết kế và triển khai phần mềm
### 4.1. Phần mềm điều khiển hệ thống
Phần mềm điều khiển toàn bộ hoạt động của hệ thống, từ việc xử lý dữ liệu nhận diện khuôn mặt cho đến quản lý các cảnh báo đột nhập. Giao diện người dùng cũng được tích hợp để dễ dàng thao tác và theo dõi.

#### 4.1.1. Thuật toán và chức năng phần mềm
- **Thuật toán nhận diện khuôn mặt:** Sử dụng các thư viện như OpenCV và TensorFlow để phân tích và nhận diện khuôn mặt với độ chính xác cao.
- **Hệ thống cảnh báo đột nhập:** Kích hoạt báo động khi phát hiện đột nhập bất thường, đồng thời gửi thông báo qua ứng dụng di động hoặc email.
- **Quản lý dữ liệu:** Lưu trữ thông tin về các lần mở khóa và cảnh báo trong cơ sở dữ liệu Firebase, giúp người dùng dễ dàng kiểm tra lịch sử.
- **Điều khiển từ xa:** Cho phép người dùng kiểm soát và theo dõi hệ thống qua giao diện di động hoặc máy tính.

## 5. Kết luận
### 5.1. Tổng kết
Hệ thống khóa cửa thông minh với FaceID và cảnh báo đột nhập đã được thiết kế và triển khai thành công, đáp ứng được yêu cầu bảo mật và tiện lợi. Hệ thống tích hợp công nghệ nhận diện khuôn mặt hiện đại và khả năng cảnh báo thời gian thực, giúp người dùng yên tâm hơn về an ninh của ngôi nhà hoặc văn phòng.

#### 5.1.1. Đề xuất và hướng phát triển tương lai
Trong tương lai, hệ thống có thể được mở rộng với các tính năng như:
- **Tích hợp AI:** Cải thiện độ chính xác và hiệu năng của hệ thống nhận diện khuôn mặt.
- **Kết nối với hệ thống nhà thông minh:** Tích hợp với các thiết bị nhà thông minh khác để điều khiển nhiều thiết bị hơn.
- **Cải tiến giao diện người dùng:** Phát triển ứng dụng di động với giao diện thân thiện, dễ sử dụng hơn.
- **Tối ưu hóa hiệu năng:** Nâng cao tốc độ xử lý và tiết kiệm năng lượng cho hệ thống.

