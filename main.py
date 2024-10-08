import logging
import sys
from argparse import ArgumentParser

from probe import Probe
from logger import configure_logger
from mqtt.mqtt_monitor import MqttClientMonitor, TerminationStatus
from mqtt.mqtt_pub import MqttPub


def main():
    configure_logger(logging.INFO)

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
    pub_e9cd9k = MqttPub(monitor, args.mqtt_hostname, args.mqtt_port, "sysinfo/probe_E9CD9K/SENSOR", 2)
    pub_x2h7dr = MqttPub(monitor, args.mqtt_hostname, args.mqtt_port, "sysinfo/probe_X2H7DR/SENSOR", 2)
    pub_x4i8kf = MqttPub(monitor, args.mqtt_hostname, args.mqtt_port, "sysinfo/probe_X4I8KF/SENSOR", 2)
    pub_lr24ye = MqttPub(monitor, args.mqtt_hostname, args.mqtt_port, "sysinfo/probe_LR24YE/SENSOR", 2)

    pub_bw9q48.start()
    pub_ki8q49.start()
    pub_p5p77r.start()
    pub_n5lth1.start()
    pub_e9cd9k.start()
    pub_x2h7dr.start()
    pub_x4i8kf.start()
    pub_lr24ye.start()

    logging.info("Mqtt publishers are now ready")
    probe = Probe(args, pub_bw9q48, pub_ki8q49, pub_p5p77r, pub_n5lth1, pub_e9cd9k, pub_x2h7dr, pub_x4i8kf, pub_lr24ye)
    monitor.register_client(probe)
    probe.start_reading()

    termination_status = monitor.wait_for_termination()
    monitor.close_all_clients(termination_status)

    if termination_status == TerminationStatus.NORMAL_TERMINATION:
        sys.exit(0)
    elif termination_status == TerminationStatus.ABNORMAL_TERMINATION:
        sys.exit(1)


if __name__ == "__main__":
    main()
