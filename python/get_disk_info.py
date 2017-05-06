#!/usr/bin/env python
import paramiko
import sys

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

for host in hosts:
  try:
    hostinfo = {}
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username='vagrant', password='vagrant',timeout=5)

    for item, command in commands.iteritems():
      newcommand=("export PATH=\'%s\';" % shell_path) + command
      stdin,stdout,stderr = ssh.exec_command(newcommand)

      #df -Pkl / | sed 1d
      hostinfo[item] = stdout.readlines()



    print hostinfo
     
  except Exception as e:
    print "Client [%s] - Error: [%s]" % (host,e)

