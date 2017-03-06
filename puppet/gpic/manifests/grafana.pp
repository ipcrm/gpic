class gpic::grafana {

  $gpackages = [
    'freetype',
    'zlib',
    'zlib-devel',
    'freetype-devel',
    'freetype-demos',
    'libfontenc',
    'libXfont',
    'urw-fonts',
  ]

  package {$gpackages:
    ensure => present,
  }

  class { '::grafana':
    admin_password => 'admin',
    secret_key     => 'abc123',
    require        => Package[$gpackages],
  }

}
