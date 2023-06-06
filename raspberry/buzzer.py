import RPi.GPIO as GPIO
import time
import mysql.connector
from flask import Flask, render_template

app = Flask(__name__)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

alarms = ["09:00:00", "14:00:00", "20:00:00"]

cnx = mysql.connector.connect(
    host = "127.0.0.1",
    user = "pyuser",
    password= "mysql",
    database = "soft"
)

cursor = cnx.cursor()

query = "INSERT INTO medicine VALUES (%s, %s, %s)"
data = ("cold", "09:00", "1")
cursor.execute(query, data)

cnx.commit()

cursor.close()
cnx.close()

def sound_alarm():
    while True:
        current_time = time.strftime("%H:%M:%S", time.localtime())
        if current_time in alarms:
            GPIO.output(11, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(11, GPIO.LOW)
            time.sleep(1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stop_alarm')
def stop_alarm():
    GPIO.output(11, GPIO.LOW)
    return 'Alarm stopped'

if __name__ == '__main__':
    try:

        import threading
        alarm_thread = threading.Thread(target=sound_alarm)
        alarm_thread.start()

        app.run(host='0.0.0.0', port=5000, debug=True)

    except KeyboardInterrupt:
        GPIO.cleanup()