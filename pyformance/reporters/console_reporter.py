# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import socket
import time
import datetime
from .reporter import Reporter


class ConsoleReporter(Reporter):
    
    def __init__(self, registry=None, reporting_interval=30, stream=sys.stderr):
        super(ConsoleReporter, self).__init__(registry, reporting_interval)
        self.stream = stream

    def report_now(self, registry=None):
        metrics = self._collect_metrics(registry or self.registry)
        for line in metrics:
            print(line, file=self.stream)
            
    def _collect_metrics(self, registry, timestamp=None):
        timestamp = timestamp or int(round(time.time()))
        dt = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=timestamp)
        metrics = registry.dump_metrics()
        metrics_data = [ "== %s ===================================" % dt.strftime("%Y-%m-%d %H:%M:%S")]
        for key in metrics.keys():
            values = metrics[key]
            metrics_data.append("%s:" %  key)
            for value_key in values.keys():
                metrics_data.append("%20s = %s" % (value_key, values[value_key]))
        metrics_data.append("")
        return metrics_data


