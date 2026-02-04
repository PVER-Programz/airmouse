import requests, json, random, time

SERVER_URL = "http://localhost:5000/keyboard"  # 🔹 Replace with your PC’s IP

# while True:
    # Generate fake gyroscope readings
data = "volumedown"

try:
    # Send POST request
    response = requests.post(SERVER_URL, json=data, timeout=1)
    print(f"Sent: {data} | Status: {response.status_code}")
except Exception as e:
    print("Error:", e)

# Adjust frequency — 0.1s = 10 samples/sec
# time.sleep(0.1)
