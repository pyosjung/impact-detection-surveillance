#sendMail.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from serverData import web_server_ip, web_server_port

class SendMail:
    def __init__(self, sender_email, sender_password):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.recipient_email = ""
        self.subject = "차량에 충돌이 발생했습니다"
        self.contents = f"""
        [충격발생]

        url : {web_server_ip}:{web_server_port} 에 접속해서 영상을 확인하세요.

        """

    def send_email(self):
        msg = MIMEMultipart()
        msg['Subject'] = self.subject
        msg['From'] = self.sender_email
        msg['To'] = self.recipient_email
        text = MIMEText(self.contents)
        msg.attach(text)

        try:
            smtp = smtplib.SMTP("smtp.naver.com", 587) # naver smtp 서버
            smtp.starttls()
            smtp.login(user=self.sender_email, password=self.sender_password)
            smtp.sendmail(self.sender_email, self.recipient_email, msg.as_string())
            smtp.close()
            print("Email sent successfully!")
        except Exception as e:
            print("Failed to send email:", e)