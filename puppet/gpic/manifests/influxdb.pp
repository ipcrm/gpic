class gpic::influxdb {
  class {'::influxdb::server':
    meta_bind_address      => "0.0.0.0:8088",
    meta_http_bind_address => "0.0.0.0:8091",
    http_bind_address      => "0.0.0.0:8086",
    admin_bind_address     => "0.0.0.0:8083",
    collectd_options => {
      'enabled' => true,
      'bind-address' => '0.0.0.0:25826',
      'database' => 'collectd',
      'typesdb' => '/usr/share/collectd/types.db',
      'batch-size' => 1000,
      'batch-pending' => 5,
      'batch-timeout' => '1s',
      'read-buffer' => 0,
    },
  }
  contain ::influxdb::server
}
