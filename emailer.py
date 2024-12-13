import pandas
import smtplib
import datetime, time
from email.mime.text import MIMEText

doc = pandas.read_excel("jobs.xlsx")
rows = doc.shape[0]

send_list = [["xx11shadowman11Xx@gmail.com", "2024-12-13 15:22:00", "Aidan"]]

sender = "xX11shadowman11Xx@gmail.com"
password = "ydaj hvpl bjnw vmtc"

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    print("Logged In")
    server.login(sender, password)

    while len(send_list) != 0:
        for data in send_list:
            msg = MIMEText(str(data))
            date = data[1]
            current = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"waiting to send to {data[0]} at time {date}. Current Time: {current} ")

            if str(date) < current:
                server.sendmail(sender, data[0], msg.as_string())
                send_list.remove(data)
                print(f"Sent to {data[0]}")
        time.sleep(1)


