import os
import smtplib
from email.message import EmailMessage

def send_mail(subject, content):
  message = EmailMessage()
  message.set_content(content)
  message['Subject'] = subject
  message['From'] = os.getenv("EMAIL_FROM")
  message['To'] = os.getenv("EMAIL_TO")
  
  u = os.getenv('CREDENTIAL_MAIL')
  p = os.getenv('CREDENTIAL_PASS')
  s = smtplib.SMTP('smtp.gmail.com', 587)
  s.starttls()
  s.login(u, p)
  s.send_message(message)
  s.quit()

