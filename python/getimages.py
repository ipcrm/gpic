#!/usr/bin/env python

import shutil
import requests
import tempfile
import time
import os
from weasyprint import HTML, CSS
from io import BytesIO
from PIL import Image
from influxdb import InfluxDBClient

servers = []
baseurl = 'http://admin:admin@localhost:3000/render/dashboard-solo/db/snmp-host-dashboard'
targetdir = '/tmp/reports/'
reportzip = '/tmp/report'

try:
  if not os.path.exists(targetdir):
    os.makedirs(targetdir)
except:
  raise

try:
  client = InfluxDBClient('localhost', 8086, 'root', 'root', 'collectd')
  result = client.query('SHOW TAG VALUES FROM "snmp_value" WITH KEY = "host"')

  for i in result:
    for j in i:
      servers.append(j['value'])
except:
  raise

#6 - Details
#11 - Details Part 2
#9 - Uptime
#10 - Average Load
#7 - Load Info
#8 - CPU Info
#3 - Memory Info
#4 - Swap Info
#1 - Disk Info
#2 - Disk Util %

#Set defaults for rendering
render = {
    11:  {'width':475, 'height': 238},
    6:  {'width':475, 'height': 238},
    9:  {'width':475, 'height': 238},
    10:  {'width':475, 'height': 238},
    0:  {'width':475, 'height': 275},
}

sourceHTML=open('test.html','r').read()

# To be updated with influxdb query
for server in servers:
  start = time.time()
  wrkpath = tempfile.mkdtemp()
  for graph in [1,2,3,4,6,7,8,9,10,11]:
    # Generate a tmp path
    # Set defaults if nothing custom
    if not graph in render.keys():
      render[graph] = render[0]

    options = "?from=now-6h&panelId=%s&theme=light&to=now&var-host=%s&width=%s&height=%s" % (graph,server,render[graph]['width'],render[graph]['height'])
    #options = "?from=now-6h&panelId=%s&theme=dark&to=now&var-host=%s&width=%s&height=%s" % (graph,server,render[graph]['width'],render[graph]['height'])
    url = baseurl + options

    with open("%s/image%s.png" % (wrkpath,graph), 'wb') as f:
      g = BytesIO()
      response = requests.get(url, stream=True)
      shutil.copyfileobj(response.raw, g)
      del response

      im = Image.open(g)

      if graph in [111]:
        imn = im.resize((375,275), Image.ANTIALIAS)
        imn.save(f, "PNG")
        imn.close()
      else:
        im.save(f, "PNG")
        im.close()

      g.close()
  end = time.time()
      
  HTML(string=sourceHTML,base_url=wrkpath).write_pdf('%s/%s.pdf' % (targetdir,server))
  shutil.rmtree(wrkpath)
  print 'Server: %s took %ss to process' % (server,end-start)

# Create ZIP file of reports
shutil.make_archive(reportzip,'zip','/tmp/', targetdir)
