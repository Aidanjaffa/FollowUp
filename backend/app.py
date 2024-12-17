from flask import Flask, redirect, render_template, session, request, jsonify
from flask_session import Session
from flask_cors import CORS
import smtplib
import datetime, time
from email.mime.text import MIMEText
import threading
import signal
import requests

stop_thread = False
send_list = []
console_messages = [" ", " "]

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
                        console_messages.append(f"\nSent to {data[0]}")
            time.sleep(1)
email_thread = threading.Thread(target=email)
email_thread.start()

def signal_handler(sig, frame):
    global stop_thread
    print("\nShutting down Flask application...")
    stop_thread = True
    email_thread.join()
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

# default route cannot handle api request so made a different route
@app.route("/")
def index():
    return jsonify({
        "userid" : 4,
        "title" : "flask react application",
        "completed" : False
    })


@app.route("/api", methods=["GET", "POST"])
def api():
    if request.method == "POST":
        # getting json
        data = request.json
        commands = data.split(" ")
        
        match commands[0]:
            case "new":
                try:
                    sendDate = commands[1]
                    send_list.append([commands[2], sendDate])
                    console_messages.append ("New email to " + commands[2] + " at time" + sendDate)
                except IndexError:
                    console_messages.append("not enough args")
                    pass
            case "status":
                console_messages.append(str(send_list))
                pass 
            case "delete":
                try:
                    deleted = int(commands[1])
                    del send_list[deleted]
                    console_messages.append("deleted")
                except IndexError:
                    console_messages.append("data does not exist or you have not specified a target\n")
                    pass
            case "clear":
                console_messages.clear()
                console_messages.append("Messages Cleared!")

        return jsonify({
            "message": console_messages
        })

    return jsonify({
        "userid" : 4,
        "title" : "flask react application",
        "message" : console_messages,
        "completed" : False
    })


