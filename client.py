import time
import asyncio

import requests
import dearpygui.dearpygui as dpg

# Initializing the data
cpu_data = []
disk_io_read_data = []
disk_io_write_data = []
gpu_load_data = []
gpu_memory_data = []
memory_data = []




# Function to get data from API
def fetch_data():
    response = requests.get('http://localhost:7001/data')
    data = response.json()

    cpu_data.append(data['cpu']['total'])
    disk_io_read_data.append(data['disk_io_read'])
    disk_io_write_data.append(data['disk_io_write'])
    gpu_load_data.append(data['gpu_0']['load'])
    gpu_memory_data.append(data['gpu_0']['memory'])
    memory_data.append(data['memory'])

    if len(cpu_data) > 500:
        cpu_data.pop(0)
        disk_io_read_data.pop(0)
        disk_io_write_data.pop(0)
        gpu_load_data.pop(0)
        gpu_memory_data.pop(0)
        memory_data.pop(0)

    dpg.set_value('cpu_data_series', [list(range(len(cpu_data))), cpu_data])
    dpg.set_value('disk_io_read_data_series', [list(range(len(disk_io_read_data))), disk_io_read_data])
    dpg.set_value('disk_io_write_data_series', [list(range(len(disk_io_write_data))), disk_io_write_data])
    dpg.set_value('gpu_load_data_series', [list(range(len(gpu_load_data))), gpu_load_data])
    dpg.set_value('gpu_memory_data_series', [list(range(len(gpu_memory_data))), gpu_memory_data])
    dpg.set_value('memory_data_series', [list(range(len(memory_data))), memory_data])

async def main():
    while True:
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, fetch_data)
        await asyncio.sleep(1)

dpg.create_context()
dpg.configure_app(manual_callback_management=True)
dpg.create_viewport()

with dpg.window(label="System Stats"):
    # create plot
    with dpg.plot(label="System Performance Stats", height=400, width=400):
        # optionally create legend
        dpg.add_plot_legend()

        # REQUIRED: create x and y axes
        dpg.add_plot_axis(dpg.mvXAxis, label="Time")
        dpg.add_plot_axis(dpg.mvYAxis, label="Value", tag="y_axis")

        # series belong to a y axis
        dpg.add_line_series([], [], label="CPU", parent="y_axis", tag="cpu_data_series")
        dpg.add_line_series([], [], label="Disk IO Read", parent="y_axis", tag="disk_io_read_data_series")
        #dpg.addSorry for the cutoff, here's the rest of the code:

        # series belong to a y axis
        dpg.add_line_series([], [], label="Disk IO Write", parent="y_axis", tag="disk_io_write_data_series")
        dpg.add_line_series([], [], label="GPU Load", parent="y_axis", tag="gpu_load_data_series")
        dpg.add_line_series([], [], label="GPU Memory", parent="y_axis", tag="gpu_memory_data_series")
        dpg.add_line_series([], [], label="Memory", parent="y_axis", tag="memory_data_series")

dpg.create_viewport(title='System Performance', width=800, height=600)
dpg.setup_dearpygui()

# Fetch the data once before the application starts
asyncio.run(main())

# Add a repeating callback that calls fetch_data every second
#dpg.add_timer(1000, callback=fetch_data)


dpg.show_viewport()


while dpg.is_dearpygui_running():
    jobs = dpg.get_callback_queue() # retrieves and clears queue
    dpg.run_callbacks(jobs)
    dpg.render_dearpygui_frame()


dpg.destroy_context()
