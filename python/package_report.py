#!/usr/bin/env python

import requests
import time
from influxdb import InfluxDBClient

baseurl = 'http://admin:admin@localhost:3000/render/dashboard-solo/db/snmp-host-dashboard'
pkgreport = '/var/www/html/pkgreport.%s.csv' % (time.time())

try:
  csv = open(pkgreport, 'w')
  client = InfluxDBClient('localhost', 8086, 'root', 'root', 'collectd')
  result = client.query('SELECT host,last(packages) from snmp_data group by host')

  for i in result:
    server = i[0]['host']
    packages = ','.join(sorted(i[0]['last'].split(','),key=lambda s: s.lower()))
    csv.write("%s,%s\n" % (server,packages))

  csv.close()
except:
  raise
