#!/bin/bash
rpm -Uvh https://yum.puppetlabs.com/puppetlabs-release-pc1-el-7.noarch.rpm
yum clean all
yum install -y puppet-agent

export PATH=$PATH:/opt/puppetlabs/bin

while read line 
do
  $line
done < /git/puppet/modules.text
/opt/puppetlabs/bin/puppet apply --modulepath="$(/opt/puppetlabs/bin/puppet config print modulepath):/git/puppet" -e 'include gpic' --hiera_config /git/puppet/hiera.yaml
/opt/puppetlabs/bin/puppet apply --modulepath="$(/opt/puppetlabs/bin/puppet config print modulepath):/git/puppet" -e 'include gpic' --hiera_config /git/puppet/hiera.yaml
#curl -H "Content-Type: application/json" -H "Accept: application/json" -X POST http://admin:admin@localhost:3000/api/datasources -d @/git/files/influxdb.datasource.json
#curl -H "Content-Type: application/json" -H "Accept: application/json" -X POST http://admin:admin@localhost:3000/api/dashboards/db -d @/git/files/snmp_host_dashboard.json
