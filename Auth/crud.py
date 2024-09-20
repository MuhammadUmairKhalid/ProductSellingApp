import random
from Auth.models import OTP
import smtplib
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from jose import jwt
from dotenv import load_dotenv

load_dotenv('confidential.env')
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
email=os.getenv('email')
password=os.getenv('password')
def generateOtp():
    otp=random.randint(1000,9000)
    return otp

def deleteUserOTP(Email:str):
    OTP.objects.filter(email=Email).delete()
    return True

def save_otp_in_database(email:str,otp: str):
    try:
        db_otp = OTP(email=email, otp=otp)
        db_otp.save()
        return True
    except Exception as e:
        print(e)
        return False

def verify_otp(email: str, otp: str):
    try:
        db_otp = OTP.objects.filter(email=email, otp=otp).first()
        return db_otp if db_otp else False
    except Exception as e:
        print(e)
        return False

def delete_user_otp(email: str):
    OTP.objects.filter(email=email).delete()

def user_otp_expiration_timer(email: str):
    timer = threading.Timer(300, delete_user_otp, args=(email,))
    timer.start()

def sendEmail(recipient:str,subject:str,body:str):
        receiver_email = recipient
        subject = subject
        Body = body
        message = Body
        msg = MIMEMultipart()
        msg['From'] =email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'html'))
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email, password)
            text = msg.as_string()
            server.sendmail(email, receiver_email, text)
            return True
        except Exception as e:
            return {'detail':f'Email could not be sent. Error: {str(e)}'}

def createAccessToken(Email:str):
    encode={'email':Email}
    return jwt.encode(encode,key=SECRET_KEY,algorithm=ALGORITHM)
