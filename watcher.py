import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, file_to_watch, script_to_run):
        self.file_to_watch = file_to_watch
        self.script_to_run = script_to_run

    def on_modified(self, event):
        if event.src_path.endswith(self.file_to_watch):
            print(f"{self.file_to_watch} has been modified. Re-running {self.script_to_run}...")
            subprocess.run(["python", self.script_to_run])

if __name__ == "__main__":
    # File and script to monitor
    file_to_watch = "input.txt"
    script_to_run = "main.py"

    # Set up the observer
    event_handler = FileChangeHandler(file_to_watch, script_to_run)
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=False)  # Monitor current directory
    observer.start()

    try:
        print(f"Watching for changes in {file_to_watch}...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
