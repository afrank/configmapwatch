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
        self._handler = self.ReadConfig(self)
        self._observer = Observer()
        self._observer.schedule(self._handler,self.cfg_vol,recursive=True)
        self._observer.start()
    def _load_config(self):
        self._config = json.load(open(f"{self.cfg_vol}/{self.cfg_file}"))
    def __iter__(self):
        return iter(self._config.items())
    @property
    def config(self):
        return _config
    class ReadConfig(FileSystemEventHandler):
        def __init__(self,outer):
            super(FileSystemEventHandler).__init__()
            self.outer = outer
        def dispatch(self, event):
            if "config.json" in event.src_path and event.event_type == 'deleted':
                logging.info(f"detected a config change; re-reading config.json.")
                self.outer._load_config()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
    cfg = Config()
    while True:
        logging.info("Here is my config:")
        logging.info(dict(cfg))
        time.sleep(3)
    observer.join()
