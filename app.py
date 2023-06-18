from flask import Flask, render_template
from flask_socketio import SocketIO
import psutil
import GPUtil
import time
import eventlet

import conf_loader as conf

eventlet.monkey_patch()  # Required for WebSocket communication in eventlet.

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')


def background_thread():
    while True:
        stats = {
            "cpu": {
                "total": psutil.cpu_percent(),
                "per_cpu": psutil.cpu_percent(percpu=True)
            },
            "memory": psutil.virtual_memory().percent,
            "disk_io": psutil.disk_io_counters().read_bytes + psutil.disk_io_counters().write_bytes,
        }

        GPUs = GPUtil.getGPUs()
        for i, gpu in enumerate(GPUs):
            stats[f"gpu_{i}"] = {
                "memory": gpu.memoryUtil * 100,
                "load": gpu.load * 100,
            }

        socketio.emit('new_stats', stats, namespace='/test')
        time.sleep(1)  # update every second


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect', namespace='/test')
def test_connect():
    print('Client connected')
    eventlet.spawn(background_thread)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=conf.PORT)
