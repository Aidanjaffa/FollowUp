from flask import Flask, redirect, render_template, session, request, jsonify
from flask_session import Session
from flask_cors import CORS
import smtplib
import datetime, time
from email.mime.text import MIMEText
import threading
import signal

stop_thread = False
send_list = []

message = "Hi My name is aidan, i made an application with you, i just wanted to follow up on my application and see how everything is going"

sender = "xX11shadowman11Xx@gmail.com"
password = "ydaj hvpl bjnw vmtc"
lock = threading.Lock()


app = Flask(__name__)
CORS(app)

app.config["SESSION_PERMANENT"] = False  # Session will be cleared when user closes their browser
app.config["SESSION_TYPE"] = "filesystem"  # Session data will be stored on the file system
app.config["SECRET_KEY"] = "test"
app.config["UPLOAD_FOLDER"] = "static/files"
Session(app)

def email():
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        print("Logged In")
        server.login(sender, password)

        while not stop_thread:
            with lock:
                for data in send_list:
                    msg = MIMEText(message)
                    msg["subject"] = "Application follow up"
                    date = data[1]
                    current = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                    #print(f"waiting to send to {data[0]} at time {date}. Current Time: {current} ")

                    if int(date) < int(current):
                        server.sendmail(sender, data[0], msg.as_string())
                        send_list.remove(data)
                        print(f"\nSent to {data[0]}")
            time.sleep(1)
email_thread = threading.Thread(target=email)
email_thread.start()

def signal_handler():
    global stop_thread
    print("\nShutting down Flask application...")
    stop_thread = True
    email_thread.join()
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.form.get("command")
        commands = data.split(" ")
        print(commands)
    
        match commands[0]:
            case "new":
                try:
                    sendDate = commands[1]
                    send_list.append([commands[2], sendDate])
                    print (send_list)
                except IndexError:
                    print("Err: not enough arguments")
            case "status":
                for item in send_list:
                    print(f"Pending Delivery To {item[0]}, Delivery Time: {item[1]}, Current Time: {datetime.datetime.now().strftime('%Y%m%d%H%M%S')}")
            case "delete":
                try:
                    for item in send_list:
                        print (item)
                    deleted = int(commands[1])
                    del send_list[deleted]
                except IndexError:
                    print("Err: data does not exist or have not specified target")

    return render_template("index.html")


@app.route("/api")
def api():
    return jsonify({
        "userid" : 4,
        "title" : "flask react application",
        "completed" : False
    })


