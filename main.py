import logging
import sys
from argparse import ArgumentParser

from bme280_probe import Bme280Probe
from mqtt.mqtt_monitor import MqttClientMonitor, TerminationStatus
from mqtt.mqtt_pub import MqttPub


def main():
    parser = ArgumentParser()
    parser.add_argument("--mqtt-hostname")
    parser.add_argument("--mqtt-port", type=int)
    parser.add_argument("--mqtt-username")
    parser.add_argument("--mqtt-password")
    args = parser.parse_args()

    monitor = MqttClientMonitor()
    pub_bw9q48 = MqttPub(monitor, args.mqtt_hostname, args.mqtt_port, "weather/probe_BW9Q48/SENSOR", 2)
    pub_ki8q49 = MqttPub(monitor, args.mqtt_hostname, args.mqtt_port, "weather/probe_KI8Q49/SENSOR", 2)
    pub_p5p77r = MqttPub(monitor, args.mqtt_hostname, args.mqtt_port, "sysinfo/probe_P5P77R/SENSOR", 2)
    pub_n5lth1 = MqttPub(monitor, args.mqtt_hostname, args.mqtt_port, "sysinfo/probe_N5LTH1/SENSOR", 2)
    pub_bw9q48.start()
    pub_ki8q49.start()
    pub_p5p77r.start()
    pub_n5lth1.start()

    logging.info("Mqtt publishers are now ready")
    bme280_probe = Bme280Probe(args, pub_bw9q48, pub_ki8q49, pub_p5p77r, pub_n5lth1)
    monitor.register_client(bme280_probe)
    bme280_probe.start_reading()

    status = monitor.wait_for_termination()
    termination_status = monitor.close_all_clients(status)

    if termination_status == TerminationStatus.NORMAL_TERMINATION:
        sys.exit(0)
    elif termination_status == TerminationStatus.ABNORMAL_TERMINATION:
        sys.exit(1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    main()
