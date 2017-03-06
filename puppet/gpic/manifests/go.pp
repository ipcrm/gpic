class gpic::go {

  $packages = ['golang']

  package {$packages:
    ensure => present,
  }


}
