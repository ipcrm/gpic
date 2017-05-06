class gpic::python {

  $packages = ['python-pip','python-cffi','python-devel','python-paramiko','pango-devel']

  package {$packages:
    ensure => present,
    notify => Exec['run pip'],
  }

  exec {'run pip':
    path        => $::path,
    command     => 'pip install -r /git/python/requirements.txt',
    refreshonly => true,
  }

  include ::apache

  cron { 'get_info':
    command => '/bin/python /git/python/get_info.py &>> /var/log/get_info.py.log',
    user    => 'root',
    hour   => ['*'],
    minute => '00',
  }

  cron { 'get_disk_info':
    command => '/bin/python /git/python/get_disk_info.py &>> /var/log/get_disk_info.py.log',
    user    => 'root',
    hour   => ['*'],
    minute => '*/5',
  }

  cron { 'get_images':
    command => '/bin/python /git/python/getimages.py &>> /var/log/getimages.py.log',
    user    => 'root',
    hour   => ['07'],
    minute => '00',
  }

  cron { 'package_report':
    command => '/bin/python /git/python/package_report.py &>> /var/log/package_report.py.log',
    user    => 'root',
    hour   => ['07'],
    minute => '00',
  }
  

}
