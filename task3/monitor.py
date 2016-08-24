#!/usr/bin/python

import psutil as ps
from daemon import Daemon
import sys
import os
import time
from datetime import datetime
import tempfile
import postgresql as psql
import postgresql.driver
import json
import configparser


class MonitorDaemon(Daemon):

    def run(self):
        monitor = Monitor()
        time.sleep(5)
        while True:
            monitor.generate_snapshot()
            time.sleep(monitor.interval)


class Monitor():

    def __init__(self):
        """ monitor's constructor
        parses config file and connects to DB
         """
#       load cfg
        config = configparser.ConfigParser()
        with open("monitor.conf", "r") as f:
            config.readfp(f)

        if config.has_option("monitor", "interval"):
            self.interval = int(config["monitor"]["interval"])
        else:
            print("interval is not set, using default")
            self.interval = 60

        if config.has_option("database", "password"):
            self.password = config["database"]["password"]
        else:
            print("db password is not set")
            sys.exit(1)
        print("Using interval: %d seconds" % self.interval)
#       connect to db
        self.db_conn = psql.driver.connect(
            user="system_snapshot",
            password=self.password,
            host="localhost",
            port=5432,
            database="system_snapshot"
        )

    def generate_snapshot(self):
        """ generate_snapshot
        creates snapshot and puts it to DB
         """
        data = {}
        data['cpu_load'] = ps.cpu_percent(percpu=True)
        data['mem'] = ps.virtual_memory()
        data['disk_io'] = ps.disk_io_counters()
        data['conn_stat'] = ps.net_io_counters(pernic=True)
        ts = time.time()
        data['timestamp'] = datetime.fromtimestamp(
            ts).strftime('%Y-%m-%d %H:%M:%S')
        json_data = json.dumps(data)

        query = self.db_conn.prepare(
            "insert into system_snapshot (data) values ('%s')" % json_data
        )
        query()
        print("insert")


if __name__ == "__main__":
    daemon = MonitorDaemon(tempfile.gettempdir() + '/monitor.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
