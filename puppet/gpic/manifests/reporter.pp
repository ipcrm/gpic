class gpic::reporter {

  $packages = ['golang','texlive-latex-bin']

  package {$packages:
    ensure => present,
  }




}
