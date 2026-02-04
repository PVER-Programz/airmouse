from flask import Flask, request
import os

app = Flask(__name__)
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.route('/gyro', methods=['POST'])
def gyro_data():
    data = request.get_json()
    if data:
        # Extract gyroscope values
        gx = data.get("x")
        gy = data.get("y")
        gz = data.get("z")
        print(f"Gyroscope -> X:{gx}, Y:{gy}, Z:{gz}")
        # os.system("cls")
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)