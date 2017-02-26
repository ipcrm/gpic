class gpic::collectd {

  contain ::collectd
  class { 'collectd::plugin::network':
    timetolive    => '70',
    maxpacketsize => '42',
    forward       => false,
    reportstats   => true,
    servers       => { 'localhost' =>
      {
        'port' => '25826',
      },
    },
  }

  class {'collectd::plugin::snmp':
    data  => hiera('snmp_data'),
    hosts => hiera('snmp_hosts'),
  }

}
