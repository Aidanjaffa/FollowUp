import pandas
import smtplib
import time
from email.mime.text import MIMEText

doc = pandas.read_excel("jobs.xlsx")
rows = doc.shape[0]

send_list = []

sender = "xX11shadowman11Xx@gmail.com"
password = "ydaj hvpl bjnw vmtc"

for i, row in doc.iterrows():
    email = row["Email"]
    date = row["Date"]
    company = row["Company"]

    send_list.append([email, date, company])


with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    print("Logged In")
    server.login(sender, password)

    for data in send_list:
        msg = MIMEText(str(data))

        server.sendmail(sender, data[0], msg.as_string())
        print(f"Sent to {data[0]}")



