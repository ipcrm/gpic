class gpic::reporter {

  $packages = ['golang','texlive-latex-bin','texlive-texconfig','texlive-collection-fontsrecommended.noarch']

  package {$packages:
    ensure => present,
    notify => Exec['rehash-texconfig'],
  }

  exec {'rehash-texconfig':
    path        => $::path,
    command     => 'texconfig rehash',
    refreshonly => true,
  }

}
