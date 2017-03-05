class gpic::python {

  $packages = ['python-pip']

  package {$packages:
    ensure => present,
  }

  python::requirements { '/git/python/requirements.txt' : }

}
