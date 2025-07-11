import atexit
import queue
import threading
from datetime import datetime
from pathlib import Path

import orjson

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


class JsonlLogger:
    def __init__(self, log_dir=LOG_DIR):
        self._log_dir = Path(log_dir)
        self._queue = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()
        atexit.register(self.close)

    def log(self, data: dict):
        self._queue.put(data)

    def _worker(self):
        while not self._stop_event.is_set():
            try:
                data = self._queue.get(timeout=1)
            except queue.Empty:
                continue

            date_str = datetime.now().strftime("%Y-%m-%d")
            log_path = self._log_dir / f"{date_str}.jsonl"
            with log_path.open("ab") as f:
                f.write(orjson.dumps(data))
                f.write(b"\n")

    def close(self):
        self._stop_event.set()
        self._thread.join()


jsonl_logger = JsonlLogger()
