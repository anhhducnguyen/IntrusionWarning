import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load các biến từ file .env
load_dotenv()

def send_email(subject, message, attachment_path=None):
    # Lấy thông tin cấu hình email từ .env
    email_host = os.getenv('EMAIL_HOST')
    email_port = int(os.getenv('EMAIL_PORT'))
    email_host_user = os.getenv('EMAIL_HOST_USER')
    email_host_password = os.getenv('EMAIL_HOST_PASSWORD')
    email_receiver = os.getenv('EMAIL_RECEIVER')

    # Tạo email
    msg = MIMEMultipart()
    msg['From'] = email_host_user
    msg['To'] = email_receiver
    msg['Subject'] = subject

    # Thêm nội dung email
    msg.attach(MIMEText(message, 'plain'))

    # Thêm tệp đính kèm nếu có
    if attachment_path:
        with open(attachment_path, 'rb') as attachment:
            part = MIMEText(attachment.read(), 'base64', 'utf-8')
            part.add_header(
                'Content-Disposition',
                f'attachment; filename="{os.path.basename(attachment_path)}"'
            )
            msg.attach(part)

    # Gửi email
    try:
        server = smtplib.SMTP(email_host, email_port)
        server.starttls()
        server.login(email_host_user, email_host_password)
        server.sendmail(email_host_user, email_receiver, msg.as_string())
        server.quit()
        print(f"Email đã được gửi tới {email_receiver}")
    except Exception as e:
        print(f"Không thể gửi email. Lỗi: {str(e)}")



