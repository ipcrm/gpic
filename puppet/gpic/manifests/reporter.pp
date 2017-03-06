class gpic::reporter {

  $packages = ['golang','texlive-latex-bin','texlive-texconfig']

  package {$packages:
    ensure => present,
  }




}
