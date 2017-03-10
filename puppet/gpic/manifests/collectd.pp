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



  Collectd::Plugin::Snmp::Host {
    version   => '2',
    community => 'secret',
    interval  => 300
  }

  hiera('snmp_hosts').each |$h,$f| {
    collectd::plugin::snmp::host {$h:
      * => $f
    }
  }

  $gpic_hosts = keys(hiera('snmp_hosts'))

  file {'/etc/gpic_hosts':
    ensure  => present,
    owner   => root,
    group   => root,
    mode    => '0444',
    content => template('gpic/gpic_hosts.erb'),
  }

 class { 'collectd::plugin::df':
    mountpoints        => ['/u'],
    fstypes          => ['nfs','tmpfs','autofs','gpfs','proc','devpts'],
    ignoreselected => true,
  }
}
