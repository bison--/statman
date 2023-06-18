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
    last_disk_io_read = 0
    last_disk_io_write = 0

    last_disk_io_read_times = 0
    last_disk_io_write_times = 0

    while True:
        current_disk_io_read = psutil.disk_io_counters().read_bytes
        current_disk_io_write = psutil.disk_io_counters().write_bytes

        current_disk_io_read_times = psutil.disk_io_counters().read_time
        current_disk_io_write_times = psutil.disk_io_counters().write_time

        stats = {
            "cpu": {
                "total": psutil.cpu_percent(),
                "per_cpu": psutil.cpu_percent(percpu=True)
            },
            "memory": psutil.virtual_memory().percent,
            "disk_io_read": current_disk_io_read - last_disk_io_read,
            "disk_io_write": current_disk_io_write - last_disk_io_write,
            "disk_io_read_times": current_disk_io_read_times - last_disk_io_read_times,
            "disk_io_write_times": current_disk_io_write_times - last_disk_io_write_times,
        }

        last_disk_io_read = current_disk_io_read
        last_disk_io_write = current_disk_io_write

        last_disk_io_read_times = current_disk_io_read_times
        last_disk_io_write_times = current_disk_io_write_times

        print(stats)
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
