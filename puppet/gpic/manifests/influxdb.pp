class gpic::influxdb {
  meta_bind_address      => "${::fqdn}:8088",
  meta_http_bind_address => "${::fqdn}:8091",
  http_bind_address      => "${::fqdn}:8086",
  class {'influxdb::server':
    collectd_options => {
      enabled => true,
      bind-address => ':25826',
      database => 'foo',
      typesdb => '/usr/share/collectd/types.db',
      batch-size => 1000,
      batch-pending => 5,
      batch-timeout => '1s',
      read-buffer => 0,
    },
  }
}
