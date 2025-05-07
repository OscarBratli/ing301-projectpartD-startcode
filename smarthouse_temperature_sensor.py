import logging
import threading
import time
import math
import requests

from messaging import SensorMeasurement
import common

import logging, threading, time, math, requests
                                       

BASE_URL = "http://127.0.0.1:8000"                      # adjust if needed


class Sensor:
    def __init__(self):
        self._stop = threading.Event()      # lar oss stoppe begge trådene ryddig

    # -------------------------------------------------------------
    #  A.  simulerer selve sensoren (lokalt)
    # -------------------------------------------------------------
    def simulator(self):
        while not self._stop.is_set():
            logging.info("🔧  Simulator: gjør måling …")
            time.sleep(1)

    # -------------------------------------------------------------
    #  B.  snakker med sky-tjenesten
    # -------------------------------------------------------------
    def client(self):
        while not self._stop.is_set():
            logging.info("🌍  Client: sender / henter data …")
            time.sleep(3)

    # -------------------------------------------------------------
    #  C.  starter begge A og B i hver sin tråd
    # -------------------------------------------------------------
    def run(self):
        sim_thread   = threading.Thread(target=self.simulator, daemon=True)
        http_thread  = threading.Thread(target=self.client,    daemon=True)

        sim_thread.start()
        http_thread.start()

        # om dere vil kunne vente på at de blir ferdige en gang:
        return sim_thread, http_thread

    def stop(self):
        self._stop.set()                    # signalerer begge løkker om å avslutte