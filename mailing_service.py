import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

# import cv2
# import os


import getpass #패스 워드 

def Requirements_sending_mail(count, mail_count, file_name,first_send_time):
    time_1 = time.time()
    
    print("time1 init", time_1)

    if count ==1:
        time_1 = time.time()
    if count ==5:
        time_2 = time.time()
        if time_2 - time_1 > 2 :
            count =0
            print("초기화")

        else:
                        
            
            if mail_count==0 :
                mail_send(file_name)
                print('메일이 발송되었습니다.-처음임!! ㅋㄷ')
                mail_count +=1
                first_send_time = time_2
                                
            elif int(time_2 - first_send_time) >= 60 :
                mail_send(file_name)
                print('메일이 발송되었습니다.-1분')
                first_send_time = time_2
            else : 
                print("1분 경과 후 재발송 됩니다.")

            count =0 
            print("초기화2")
    return count, mail_count,first_send_time


def mail_send(file_name):
    SMTP_SERVER = 'smtp.naver.com'
    SMTP_SSL_PORT = 587
    #sender_email = "메일명@naver.com" 보내는 사람 네이버 이메일
    sender_email = "메일명@naver.com"
    #password = getpass.getpass("Passward:asdfsdfasdf2")
    password = "12314asdf82"
    

    
    #receiver_email = "메일명@naver.com" 받는 사람 네이버 이메일
    receiver_email = "메일명@naver.com"
    
    file = file_name.split('/')[-1]
    #file = file_size(file_path, file)
    
    
    #이메일 카운터 
    

    #이메일 헤더 만들기 
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = 'hornet' + str(time.ctime())
    body = "a hornet has appeared at your apiary(beehouse)"
    msg.attach(MIMEText(body, 'plain'))

    #첨부파일 추가 
    attach_file = open(file_name,"rb")
    file_data = MIMEBase("application", "png")
    file_data.set_payload((attach_file).read())
    encoders.encode_base64(file_data)

    #파일이름 지정된 report header를 추가 
    file_data.add_header("Content-Disposition", "attachment", filename=file)
    msg.attach(file_data)

    #SMTP 세션 생성하여 이메일 전송
    session = smtplib.SMTP(SMTP_SERVER, SMTP_SSL_PORT)
    session.starttls() #tls사용
    session.login(sender_email, password)
    text = msg.as_string()
    print("mail : a hornet has appeared at your apiary(beehouse) ")
    session.sendmail(sender_email, receiver_email, text)
    session.quit()




