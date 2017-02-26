class gpic::grafana {

  class { '::grafana':
    admin_password => 'admin',
    secret_key     => 'abc123',
  }

}
