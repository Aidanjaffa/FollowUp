import smtplib
import datetime, time
from email.mime.text import MIMEText
import threading

send_list = [["x@gmail.com", "2099-12-13 16:27:00", "Aidan"]]

message = "Hi My name is aidan, i made an application with you, i just wanted to follow up on my application and see how everything is going"

sender = "xX11shadowman11Xx@gmail.com"
password = "ydaj hvpl bjnw vmtc"

lock = threading.Lock()

def new_data():
    date = input("Input sending date: ")
    email = input("Input Recipient Email: ")
    name = input("Input company name: ")

    with lock:
        send_list.append([email, date, name])
        print ("New Data Added")

def email():
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        print("Logged In")
        server.login(sender, password)

        while len(send_list) != 0:
            with lock:
                for data in send_list:
                    msg = MIMEText(message)
                    msg["subject"] = "Application follow up"
                    date = data[1]
                    current = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    if str(date) < current:
                        server.sendmail(sender, data[0], msg.as_string())
                        send_list.remove(data)
                        print(f"\nSent to {data[0]}")
            time.sleep(1)


email_thread = threading.Thread(target=email)
email_thread.start()
time.sleep(0.5)
while True:
    command = input("=> ")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    match command:
        case "new":
            new_data()
        case "status":
            for item in send_list:
                print(f"Pending Delivery To {item[0]}, Delivery Time: {item[1]}, Current Time: {now}")
        case "time":
            print(now)
        case "delete":
            for item in send_list:
                print (item)
            deleted = int(input("delete: "))
            del send_list[deleted]