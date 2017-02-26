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

  hiera('snmp_data').each |$e,$d| {
    collectd::plugin::snmp::data {$e:
      * => $d,
    }
  }

  hiera('snmp_hosts').each |$h,$f| {
    collectd::plugin::snmp::host {$h:
      * => $f
    }
  }

 class { 'collectd::plugin::df':
    mountpoints        => ['/u'],
    fstypes          => ['nfs','tmpfs','autofs','gpfs','proc','devpts'],
    ignoreselected => true,
  }
}
