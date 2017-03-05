class gpic::python {

  $packages = ['python-pip','python-cffi','python-devel','python-paramiko']

  package {$packages:
    ensure => present,
    notify => Exec['run pip'],
  }

  exec {'run pip':
    path        => $::path,
    command     => 'pip install -r /git/python/requirements.txt',
    refreshonly => true,
  }

}
