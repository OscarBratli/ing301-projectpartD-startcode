import logging
import threading
import time
import requests

from messaging import ActuatorState
import common

BASE_URL = "http://127.0.0.1:8000"                        # adjust if needed


class Actuator:
    def __init__(self, did: str):
        self.did = did
        self.state = ActuatorState("False")                # helper class
        self._stop = threading.Event()                     # clean shutdown

    # ------------------------------------------------------------
    # 1) “Hardware” simulator – already provided in the starter
    # ------------------------------------------------------------
    def simulator(self):
        logging.info("Actuator %s simulator starting", self.did)
        while not self._stop.is_set():
            logging.info("Actuator %s: %s", self.did, self.state.state)
            time.sleep(common.LIGHTBULB_SIMULATOR_SLEEP_TIME)

    # ------------------------------------------------------------
    # 2) HTTP client – poll the cloud, update `self.state`
    # ------------------------------------------------------------
    def client(self):
        logging.info("Actuator-client %s starting", self.did)
        url = f"{BASE_URL}/smarthouse/actuator/{self.did}/current"

        while not self._stop.is_set():
            try:
                r = requests.get(url, timeout=2)
                r.raise_for_status()
                active = r.json()["active"]               # bool
                self.state.set_state(str(active))          # keep it as "True"/"False"
                logging.debug("Polled state for %s → %s", self.did, active)
            except requests.RequestException as exc:
                logging.error("Polling actuator %s failed – %s", self.did, exc)

            time.sleep(common.LIGHTBULB_CLIENT_SLEEP_TIME)

        logging.info("Actuator-client %s finishing", self.did)

    # ------------------------------------------------------------
    # 3) helper to start both threads
    # ------------------------------------------------------------
    def run(self):
        sim_thread = threading.Thread(target=self.simulator, daemon=True)
        cli_thread = threading.Thread(target=self.client,    daemon=True)
        sim_thread.start()
        cli_thread.start()
        return sim_thread, cli_thread        # optionally let caller keep the handles

    # optional – lets outside code stop both loops if ever required
    def stop(self):
        self._stop.set()

