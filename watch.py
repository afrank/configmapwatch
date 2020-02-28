import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json

class Config:
    def __init__(self, cfg_vol='/opt/config', cfg_file='config.json'):
        self._config = {}
        self.cfg_vol = cfg_vol
        self.cfg_file = cfg_file
        self._load_config()
        self._handler = FileSystemEventHandler()
        # I use on_deleted because the last thing that happens when a config is updated is the old one is deleted
        self._handler.on_deleted = self._event_handler
        self._observer = Observer()
        self._observer.schedule(self._handler,self.cfg_vol,recursive=True)
        self._observer.start()
    def _event_handler(self,event):
        if "config.json" in event.src_path:
            logging.info(f"detected a config change; re-reading config.json.")
            self._load_config()
    def _load_config(self):
        self._config = json.load(open(f"{self.cfg_vol}/{self.cfg_file}"))
    def __iter__(self):
        return iter(self._config.items())
    def __del__(self):
        self._observer.stop()
        self._observer.join()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
    cfg = Config()
    while True:
        logging.info(dict(cfg))
        time.sleep(3)
