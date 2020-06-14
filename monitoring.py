import psutil
import socket
import http.server
import socketserver
import json
import os
import datetime
from typing import List
import subprocess

# GET ENV or 5 is the default
STATS_TIMEOUT = int(os.environ.get("STATUS_REFRESH_PERIOD", 5))
PORT = 8000


class Monitoring(object):
    def __init__(self):
        self.hostname = socket.gethostname()
        self.disk_usage = self.get_disk_usage()
        self.memory_usage = self.get_memory_usage()
        self.last_generated = datetime.datetime.now()
        self.processes = self.get_processes()

    def get_disk_usage(self) -> float:
        du = subprocess.run(
            "du -s / --exclude=/proc | cut -f1",
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            encoding="utf-8",
        )
        output = int(du.stdout.rstrip("\n")) / 1024
        self.disk_usage = float("%.2f" % output)
        return self.disk_usage

    def get_memory_usage(self) -> float:
        with open("/sys/fs/cgroup/memory/memory.usage_in_bytes") as f:
            mu = int(f.read()) / 1024 ** 2
            self.memory_usage = float("%.2f" % mu)
        return self.memory_usage

    def get_processes(self) -> List[dict]:
        self.processes = [
            p.info for p in psutil.process_iter(["name", "pid", "cpu_percent"])
        ]
        return self.processes

    def display_usage(self) -> dict:
        time_diff = datetime.datetime.now() - self.last_generated
        if time_diff.seconds >= STATS_TIMEOUT:
            self.get_memory_usage()
            self.get_disk_usage()
            self.get_processes()
            self.last_generated = datetime.datetime.now()
        return {
            "last_generated": str(self.last_generated),
            "hostname": self.hostname,
            "memory_usage_in_mb": self.memory_usage,
            "processes_num": len(self.processes),
            "processes": self.processes,
            "disk_usage_in_mb": self.disk_usage,
        }


monitoring = Monitoring()


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        # Setting the header
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = monitoring.display_usage()
        # Writing the HTML contents with UTF-8
        self.wfile.write(bytes(json.dumps(response), "utf-8"))
        return


# Create an object of the above class
handler_object = MyHttpRequestHandler
my_server = socketserver.TCPServer(("", PORT), handler_object)
# Star the server
my_server.serve_forever()
