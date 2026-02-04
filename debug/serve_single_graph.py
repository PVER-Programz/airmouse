from flask import Flask, request
import threading, time, json
import matplotlib.pyplot as plt
from collections import deque

app = Flask(__name__)

# Keep recent data points (for a smooth scrolling graph)
MAX_POINTS = 200
x_data = deque(maxlen=MAX_POINTS)
y_data = deque(maxlen=MAX_POINTS)
z_data = deque(maxlen=MAX_POINTS)
timestamps = deque(maxlen=MAX_POINTS)

# Lock for thread safety
from threading import Lock
data_lock = Lock()

@app.route('/gyro', methods=['POST'])
def gyro_data():
    data = request.get_json()
    if data:
        gx = data.get("x", 0)
        gy = data.get("y", 0)
        gz = data.get("z", 0)
        with data_lock:
            x_data.append(gx)
            y_data.append(gy)
            z_data.append(gz)
            timestamps.append(time.time())
    return "OK"

def plot_thread():
    plt.ion()
    fig, ax = plt.subplots()
    line_x, = ax.plot([], [], label='X', color='r')
    line_y, = ax.plot([], [], label='Y', color='g')
    line_z, = ax.plot([], [], label='Z', color='b')
    ax.legend()
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Gyro Value")
    ax.set_title("Real-time Gyroscope Data")

    while True:
        with data_lock:
            if timestamps:
                t0 = timestamps[0]
                t = [ts - t0 for ts in timestamps]
                line_x.set_data(t, x_data)
                line_y.set_data(t, y_data)
                line_z.set_data(t, z_data)
                ax.relim()
                ax.autoscale_view()

        plt.pause(0.05)  # Update every 50ms

# Run Flask in one thread and plot in another
if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)).start()
    plot_thread()
