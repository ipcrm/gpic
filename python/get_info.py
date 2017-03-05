#!/usr/bin/env python
import paramiko
import sys
from influxdb import InfluxDBClient
from influxdb import SeriesHelper

# To be replaced with infile
hosts = ['client1','client2','client3']

# To be replaced with infile
commands = {
    'os':'cat /etc/redhat-release',
    'vendor':'cat /sys/devices/virtual/dmi/id/chassis_vendor',
    'bios_version':'cat /sys/devices/virtual/dmi/id/bios_version',
    'model':'cat /sys/devices/virtual/dmi/id/product_name',
    'asset':'cat /sys/devices/virtual/dmi/id/chassis_asset_tag',
    'memtotal': """cat /proc/meminfo |grep MemTotal|awk '{print $2}'""",
    'cputype': """cat /proc/cpuinfo |grep model\ name|awk -F':' '{print $2}'|sed 's/^ //g'""",
#    'diskinfo': """dmesg|grep logical\ blocks|awk '{print $5,$10,$11,$12}'|tr '\n' ','|sed 's/,$//g'""",
    'ipaddr': """ip addr show|grep inet |grep -v inet6 |grep -v 127.0.0.1|awk '{print $2}'|awk -F '/' '{print $1}'|tr '\n' ','|sed 's/,$//g'"""
}
shell_path='/bin:/usr/bin:/sbin:/usr/sbin'

## InfluxDB connections settings
host = 'localhost'
port = 8086
user = 'root'
password = 'root'
dbname = 'collectd'
myclient = InfluxDBClient(host, port, user, password, dbname)


class ServerInfoHelper(SeriesHelper):
    # Meta class stores time series helper configuration.
    class Meta:
        # The client should be an instance of InfluxDBClient.
        client = myclient
        # The series name must be a string. Add dependent fields/tags in curly brackets.
        series_name = 'snmp_data'
        # Defines all the fields in this time series.
        fields = ['os', 'memtotal', 'vendor', 'asset', 'bios_version', 'cputype', 'model', 'ipaddr']
        # Defines all the tags for the series.
        tags = ['host']
        # autocommit must be set to True when using bulk_size
        autocommit = True

for host in hosts:
  try:
    hostinfo = {}
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username='vagrant', password='vagrant',timeout=5)

    for item, command in commands.iteritems():
      newcommand=("export PATH=\'%s\';" % shell_path) + command
      stdin,stdout,stderr = ssh.exec_command(newcommand)
      hostinfo[item] = stdout.readline()[0:-1]
     
      if item in ['vendor','asset','bios_version','cpu_type','model'] and len(hostinfo[item]) == 0:
        hostinfo[item] = 'N/A'

    print hostinfo

    ServerInfoHelper(host=host, **hostinfo)
  except Exception as e:
    print "Client [%s] - Error: [%s]" % (host,e)


