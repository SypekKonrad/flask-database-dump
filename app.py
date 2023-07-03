from flask import Flask
from flask_crontab import Crontab
from flask_mail import Mail, Message
from datetime import datetime
import os, subprocess


app = Flask(__name__)

crontab = Crontab(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'example@example.com'
app.config['MAIL_PASSWORD'] = 'example'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@crontab.job(hour=0, minute=0) # scheduled flask-crontab to perform dump of database everyday at midnight
@app.route("/")
def dumpdata():
    os.chdir('/path/to/your/database') # change directory to root of your project/database
    x = subprocess.call(['/path/to/your/python/project/venv', 'manage.py', 'dumpdata', '-o', # 
                     '/path/to/save/YourDB.json'])

    msg = Message(subject='database backup',
                  sender='example@example.com',
                  recipients=['example@example.com',]
                  )
    msg.body = 'wygenerowano' + ' ' + str(datetime.now())

    with app.open_resource('/path/to/save/YourDB.json') as fp:
        msg.attach('YourDB.json', 'YourDB/json', fp.read())

    mail.send(msg)
    


