#!/usr/bin/env python

import shutil
import requests
import tempfile
from weasyprint import HTML, CSS
from io import BytesIO
from PIL import Image

baseurl = 'http://admin:admin@localhost:3000/render/dashboard-solo/db/snmp-host-dashboard'

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
    11:  {'width': 700, 'height': 240},
    6:  {'width': 700, 'height': 240},
    0:  {'width': 350, 'height': 153},
}

sourceHTML=open('test.html','r').read()

# To be updated with influxdb query
for server in ['server.example.lan']:
  wrkpath = tempfile.mkdtemp()
  print wrkpath
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

      if graph in [6,11]:
        imn = im.resize((500,220), Image.ANTIALIAS)
        imn.save(f, "PNG")
        imn.close()
      else:
        im.save(f, "PNG")
        im.close()

      g.close()
      

  HTML(string=sourceHTML,base_url=wrkpath).write_pdf('/Users/mcadorette/git/gpic/sandbox/%s.pdf' % (server))
  shutil.rmtree(wrkpath)
