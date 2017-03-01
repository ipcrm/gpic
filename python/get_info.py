#!/usr/bin/env python
import paramiko

# To be replaced with infile
hosts = ['client1']

# To be replaced with infile
commands = {
    'os':'cat /etc/redhat-release',
    'vendor':'cat /sys/devices/virtual/dmi/id/chassis_vendor',
    'bios_version':'cat /sys/devices/virtual/dmi/id/bios_version',
    'model':'cat /sys/devices/virtual/dmi/id/product_name',
    'asset':'cat /sys/devices/virtual/dmi/id/chassis_asset_tag',
    'memtotal': """cat /proc/meminfo |grep MemTotal|awk '{print $2}'""",
    'cputype': """cat /proc/cpuinfo |grep model\ name|awk -F':' '{print $2}'|sed 's/^ //g'""",
    'diskinfo': """dmesg|grep logical\ blocks|awk '{print $5,$10,$11,$12}'|tr '\n' ','|sed 's/,$//g'"""
}

for host in hosts:
  hostinfo = {}
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  ssh.connect(host, username='vagrant', password='vagrant')

  for item, command in commands.iteritems():
    stdin,stdout,stderr = ssh.exec_command(command)
    hostinfo[item] = stdout.readline()[0:-1]

  print hostinfo




