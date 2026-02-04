from flask import Flask, request
import threading, time, json
import matplotlib.pyplot as plt
from collections import deque
from threading import Lock

app = Flask(__name__)

# Store recent gyro readings
MAX_POINTS = 200
x_data = deque(maxlen=MAX_POINTS)
y_data = deque(maxlen=MAX_POINTS)
z_data = deque(maxlen=MAX_POINTS)
timestamps = deque(maxlen=MAX_POINTS)
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
    fig, axs = plt.subplots(4, 1, figsize=(8, 10), sharex=True)

    # Axes labels
    axs[0].set_title("All Axes Combined")
    axs[1].set_title("X Axis")
    axs[2].set_title("Y Axis")
    axs[3].set_title("Z Axis")

    for ax in axs:
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Gyro Value")
        ax.grid(True)

    # Plot lines
    line_all_x, = axs[0].plot([], [], color='r', label='X')
    line_all_y, = axs[0].plot([], [], color='g', label='Y')
    line_all_z, = axs[0].plot([], [], color='b', label='Z')
    axs[0].legend()

    line_x, = axs[1].plot([], [], color='r')
    line_y, = axs[2].plot([], [], color='g')
    line_z, = axs[3].plot([], [], color='b')

    plt.tight_layout()

    while True:
        with data_lock:
            if timestamps:
                t0 = timestamps[0]
                t = [ts - t0 for ts in timestamps]

                # Update all graphs
                line_all_x.set_data(t, x_data)
                line_all_y.set_data(t, y_data)
                line_all_z.set_data(t, z_data)

                line_x.set_data(t, x_data)
                line_y.set_data(t, y_data)
                line_z.set_data(t, z_data)

                # Adjust view
                for ax in axs:
                    ax.relim()
                    ax.autoscale_view()

        plt.pause(0.05)  # Update every 50 ms

if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)).start()
    plot_thread()
