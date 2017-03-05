class gpic::python {

  $packages = ['python-pip']

  package {$packages:
    ensure => present,
  }

}
