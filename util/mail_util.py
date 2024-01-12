from email import contentmanager
import smtplib, ssl
from smtplib import SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

from dotenv import load_dotenv

from model import Chat

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, "../.env"))

# 이메일 서버 연결 정보
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465
SMTP_EMAIL = 'ilsa1115111500@gmail.com'
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


async def send_email(
        receiver: str, chat: Chat
):
    try:
        smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        smtp.login(SMTP_EMAIL, SMTP_PASSWORD)

        message = MIMEMultipart()
        message["Subject"] = "[ComfortChat]" + " " + chat.keyword
        message["From"] = SMTP_EMAIL
        message['To'] = receiver

        smtp.sendmail(SMTP_EMAIL, receiver, message.as_string())
    except Exception as e:
        print("이메일 전송 중 오류 발생:", str(e))
    finally:
        smtp.quit()
