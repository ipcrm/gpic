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
