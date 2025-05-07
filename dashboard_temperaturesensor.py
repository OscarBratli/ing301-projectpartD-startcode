import tkinter as tk
from tkinter import ttk
import logging, requests
from messaging import SensorMeasurement

BASE_URL = "http://127.0.0.1:8000"


def refresh_btn_cmd(temp_widget, did):
    logging.info("Temperature refresh")
    try:
        r = requests.get(f"{BASE_URL}/smarthouse/sensor/{did}/current", timeout=2)
        r.raise_for_status()
        value = r.json()["value"]
        
        sensor_measurement = SensorMeasurement(init_value=value)
    except requests.RequestException as exc:
        logging.error("Could not refresh temperature for %s – %s", did, exc)
        sensor_measurement = SensorMeasurement(init_value="N/A")

    temp_widget.config(state="normal")
    temp_widget.delete("1.0", "end")
    temp_widget.insert("1.0", str(sensor_measurement.value))
    temp_widget.config(state="disabled")


def init_temperature_sensor(container, did):
    ts_lf = ttk.LabelFrame(container, text=f"Temperature sensor [{did}]")
    ts_lf.grid(column=0, row=1, padx=20, pady=20, sticky=tk.W)

    temp = tk.Text(ts_lf, height=1, width=10, state="disabled")
    temp.grid(column=0, row=0, padx=20, pady=20)

    refresh_button = ttk.Button(
        ts_lf, text="Refresh", command=lambda: refresh_btn_cmd(temp, did)
    )
    refresh_button.grid(column=1, row=0, padx=20, pady=20)