import tkinter as tk
from tkinter import ttk
import logging
import requests

from messaging import ActuatorState
import common

BASE_URL = "http://127.0.0.1:8000"   
def lightbulb_cmd(state, did):
    active = state.get() == "On"          # → True / False
    logging.info("Light-bulb %s is %s", did, active)
    try:
        r = requests.put(
            f"{BASE_URL}/smarthouse/device/{did}/set",
            params={"active": active},     # <-- MUST be a dict!
            timeout=2,
        )
        r.raise_for_status()
    except requests.RequestException as exc:
        logging.error("Could not set light-bulb %s – %s", did, exc)



def init_lightbulb(container, did):

    lb_lf = ttk.LabelFrame(container, text=f'LightBulb [{did}]')
    lb_lf.grid(column=0, row=0, padx=20, pady=20, sticky=tk.W)

    # variable used to keep track of lightbulb state
    lightbulb_state_var = tk.StringVar(None, 'Off')

    on_radio = ttk.Radiobutton(lb_lf, text='On', value='On',
                               variable=lightbulb_state_var,
                               command=lambda: lightbulb_cmd(lightbulb_state_var, did))

    on_radio.grid(column=0, row=0, ipadx=10, ipady=10)

    off_radio = ttk.Radiobutton(lb_lf, text='Off', value='Off',
                                variable=lightbulb_state_var,
                                command=lambda: lightbulb_cmd(lightbulb_state_var, did))

    off_radio.grid(column=1, row=0, ipadx=10, ipady=10)
