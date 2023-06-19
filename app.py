from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import psutil
import GPUtil
import time
import eventlet

import conf_loader as conf

eventlet.monkey_patch()  # Required for WebSocket communication in eventlet.

app = Flask(__name__, static_url_path='/assets', static_folder='assets')
socketio = SocketIO(app, async_mode='eventlet')

latest_stats = None  # Added: a global variable to hold the latest stats


def background_thread():
    global latest_stats  # Added: we'll update this global variable

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
            "disk_io_read_times": current_disk_io_read_times - last_disk_io_read_times if latest_stats else 0,
            "disk_io_write_times": current_disk_io_write_times - last_disk_io_write_times if latest_stats else 0,
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

        latest_stats = stats  # Added: store the latest stats

        socketio.emit('new_stats', stats, namespace='/data')
        time.sleep(conf.REFRESH_TIME)  # update every second


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data', methods=['GET'])  # Added: new HTTP endpoint
def data():
    return jsonify(latest_stats)  # Return the latest stats as JSON


@socketio.on('connect', namespace='/data')
def data_connect():
    print('Client connected')
    eventlet.spawn(background_thread)


if __name__ == '__main__':
    eventlet.spawn(background_thread)  # start the background thread when the server starts
    socketio.run(app, host=conf.HOST, port=conf.PORT)
