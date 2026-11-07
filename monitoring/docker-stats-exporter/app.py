#!/usr/bin/env python3
import time
import threading
import logging

from prometheus_client import start_http_server, Gauge
import docker

logging.basicConfig(level=logging.INFO)

# Метрики
RX = Gauge('docker_container_network_receive_bytes_total', 'Cumulative network bytes received by container', ['container', 'id', 'service'])
TX = Gauge('docker_container_network_transmit_bytes_total', 'Cumulative network bytes transmitted by container', ['container', 'id', 'service'])


def collect_loop(poll_interval=5):
    client = docker.from_env()
    while True:
        try:
            # ИСПРАВЛЕНИЕ: убираем скобки после containers и добавляем .list()
            containers = client.containers.list(all=True)
            for c in containers:
                try:
                    stats = c.stats(stream=False)
                    networks = stats.get('networks') or {}
                    rx = 0
                    tx = 0
                    for iface in networks.values():
                        rx += iface.get('rx_bytes', 0) or 0
                        tx += iface.get('tx_bytes', 0) or 0

                    name = c.name
                    cid = c.id[:12]

                    labels = c.attrs.get('Config', {}).get('Labels', {}) or {}
                    service = labels.get('com.docker.compose.service', '')

                    RX.labels(container=name, id=cid, service=service).set(rx)
                    TX.labels(container=name, id=cid, service=service).set(tx)
                except Exception:
                    logging.exception('Error collecting stats for container %s', getattr(c, 'name', '<unknown>'))
        except Exception:
            logging.exception('Error listing containers')

        time.sleep(poll_interval)


def main():
    start_http_server(9126)
    t = threading.Thread(target=collect_loop, daemon=True)
    t.start()
    logging.info('docker-stats-exporter running on :9126')
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()