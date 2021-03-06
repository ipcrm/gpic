#!/usr/bin/env python
import paramiko
import sys
from influxdb import InfluxDBClient
from influxdb import SeriesHelper

# Read hosts from file
try:
  with open('/etc/gpic_hosts') as f:
    hosts = f.read().splitlines()
except Exception as e:
    print "Errror: [%s]" % (e)
    raise

# To be replaced with infile
commands = {
    'mounts':"""cat /proc/mounts|awk '{print $1,$2,$3}'|egrep 'xfs|ext'"""
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
    class Meta:
        client = myclient
        series_name = 'ssh_data'
        fields = ['total', 'free', 'used','prc']
        tags = ['host']
        autocommit = True

for host in hosts:
  try:
    diskinfo = {
        'total': 0,
        'used': 0,
        'free': 0,
    }

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username='vagrant', password='vagrant',timeout=5)

    for item, command in commands.iteritems():
      newcommand=("export PATH=\'%s\';" % shell_path) + command
      stdin,stdout,stderr = ssh.exec_command(newcommand)

      for line in stdout.readlines():
        _,mount,_ = line.replace('\n', '').split()

        #df -Pkl / | sed 1d
        command=("export PATH=\'%s\';" % shell_path) + ("df -Pkl %s | sed 1d") % mount
        stdin,stdout,stderr = ssh.exec_command(command)

        #/dev/mapper/centos-root    19351552 1219072  18132480       7% /
        _,total,used,avail,_,_ = stdout.readlines()[0].replace('\n','').split()

        diskinfo['total']   = diskinfo['total'] + int(total)
        diskinfo['used']    = diskinfo['used'] + int(used)
        diskinfo['free']    = diskinfo['free'] + int(avail)

    diskinfo['prc'] = 100 * ( float(diskinfo['used'])/float(diskinfo['total']) )
    ServerInfoHelper(host=host, **diskinfo)
  except Exception as e:
    print "Client [%s] - Error: [%s]" % (host,e)

