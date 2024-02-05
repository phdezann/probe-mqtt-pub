import threading
import logging


class Buffer:
    def __init__(self, args, accumulator, influxdb, killer):
        self.args = args
        self.buffer = []
        self.accumulator = accumulator
        self.influxdb = influxdb
        self.killer = killer

    def copy_and_empty_buffer(self):
        copy = self.buffer.copy()
        self.buffer.clear()
        return copy

    def read(self):
        try:
            while True:
                result = self.accumulator.get()
                if not self.args.influxdb_hostname == "localhost":
                    if len(self.buffer) >= self.args.buffer_size:
                        buffer_copy = self.copy_and_empty_buffer()
                        self.influxdb.push_all(buffer_copy, self.args.influxdb_energy_bucket)
                    else:
                        self.buffer.append(result)
                else:
                    self.influxdb.push_all([result], self.args.influxdb_energy_bucket)
        except Exception as e:
            logging.exception(e)
            self.killer.kill()

    def start_reading(self):
        thread = threading.Thread(target=self.read, args=())
        thread.start()
        return thread
