import json
import logging
import re
import socket
import subprocess
import threading
import time
from tcping import Ping


class Bme280Probe:
    def __init__(self, args, pub_bw9q48, pub_ki8q49, pub_p5p77r, pub_n5lth1, pub_e9cd9k, pub_x2h7dr):
        self.args = args
        self.pub_bw9q48 = pub_bw9q48
        self.pub_ki8q49 = pub_ki8q49
        self.pub_p5p77r = pub_p5p77r
        self.pub_n5lth1 = pub_n5lth1
        self.pub_e9cd9k = pub_e9cd9k
        self.pub_x2h7dr = pub_x2h7dr
        self.active = True

    def is_active(self):
        return self.active

    def close(self, err_msg):
        if self.active:
            logging.warning(f"Bme280Probe closed due to '{err_msg}'")
            self.active = False

    def extract(self, line, regex):
        return re.search(regex, line.strip()).group(1)

    def run_all(self):
        self.run("fly", "read_bme280", self.pub_bw9q48, lambda lines_out: self.parse_read_bme280(lines_out))
        self.run("mosquito", "read_bme280", self.pub_ki8q49, lambda lines_out: self.parse_read_bme280(lines_out))
        self.run("fly", "python3 /opt/pi/dotfiles.py/src/sysinfo.py", self.pub_p5p77r, lambda lines_out: lines_out[0])
        self.run("mosquito", "python3 /opt/pi/dotfiles.py/src/sysinfo.py", self.pub_n5lth1, lambda lines_out: lines_out[0])
        self.run("bee", "python3 /opt/pi/dotfiles.py/src/sysinfo.py", self.pub_e9cd9k, lambda lines_out: lines_out[0])
        self.run("retropie", "python3 /opt/pi/dotfiles.py/src/sysinfo.py", self.pub_x2h7dr, lambda lines_out: lines_out[0])

    def build_command(self, probe_hostname, cmd):
        args = cmd.split(" ")
        if socket.gethostname() == probe_hostname:
            return args
        else:
            return ["ssh", probe_hostname] + args

    def parse_read_bme280(self, lines_out):
        pressure = float(self.extract(lines_out[0], r"(.+?) hPa"))
        humidity = float(self.extract(lines_out[1], r"(.+?) %"))
        temperature = float(self.extract(lines_out[2], r"(.+?) C"))

        values = dict()
        values['pressure'] = pressure
        values['humidity'] = humidity
        values['temperature'] = temperature
        return json.dumps(values)

    def run(self, probe_hostname, cmd, pub, parser):
        try:
            logging.warning("Pinging '" + probe_hostname + "'")
            ping = Ping(probe_hostname, 22)
            ping.ping(3)
        except Exception:
            logging.warning("Cannot ping '" + probe_hostname + "', aborting.")
            return

        command = self.build_command(probe_hostname, cmd)
        process = subprocess.Popen(command,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   stdin=subprocess.PIPE,
                                   universal_newlines=True)
        process.wait()
        lines_out = process.stdout.readlines()
        lines_err = process.stderr.readlines()

        if len(lines_out) == 0 or len(lines_err) > 0:
            logging.info("Got on stdout: " + str(lines_out))
            logging.info("Got on stderr: " + str(lines_err))
            return

        json_payload = parser(lines_out)
        pub.publish(json_payload)

    def read(self):
        try:
            while self.active:
                self.run_all()
                time.sleep(60 * 1)
        except Exception as e:
            self.active = False
            raise e

    def start_reading(self):
        thread = threading.Thread(target=self.read, args=())
        thread.start()
        return thread
