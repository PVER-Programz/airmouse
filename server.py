from flask import Flask, request
import pyautogui as pag
import time as t

app = Flask(__name__)
debugMode=False

if not debugMode:
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

@app.route('/gyro', methods=['POST'])
def gyro_data():
    data = request.get_json()
    if data:
        gx = int(data.get("x"))
        gy = int(data.get("y"))
        gz = int(data.get("z"))
        # print(f"Gyro -> X:{gx}, Y:{gy}, Z:{gz}")
        try:
            pag.move(-gz*2, -gx)
            return "System OK"
        except pag.FailSafeException:
            return "Failsafe Error"

@app.route('/button', methods=['POST'])
def button_data():
    data=request.get_json()
    button = data.get("button")
    control = data.get("control")
    if control=="up":
        pag.mouseUp(button=button)
    elif control=="down":
        pag.mouseDown(button=button)
    return "System OK ig"

@app.route('/keyboard', methods=['POST'])
def keyboard():
    data=request.get_json()
    print(type(data),data)
    pag.hotkey(*list(data.values()))
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
