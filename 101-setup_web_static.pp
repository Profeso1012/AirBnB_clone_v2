# 101-setup_web_static.pp
class setup_web_static {
  
  # Ensure nginx is installed and running
  package { 'nginx':
    ensure => installed,
  }

  service { 'nginx':
    ensure     => running,
    enable     => true,
    subscribe  => File['/etc/nginx/sites-available/default'],
  }

  # Create the required directories
  file { '/data/web_static/releases/test/':
    ensure => directory,
    owner  => 'ubuntu',
    group  => 'ubuntu',
    mode   => '0755',
    require => Package['nginx'],
  }

  file { '/data/web_static/shared/':
    ensure => directory,
    owner  => 'ubuntu',
    group  => 'ubuntu',
    mode   => '0755',
    require => Package['nginx'],
  }

  # Create the HTML file with specific content
  file { '/data/web_static/releases/test/index.html':
    ensure  => file,
    content => "<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>\n",
    owner   => 'ubuntu',
    group   => 'ubuntu',
    mode    => '0644',
    require => File['/data/web_static/releases/test/'],
  }

  # Create a symbolic link
  file { '/data/web_static/current':
    ensure => link,
    target => '/data/web_static/releases/test',
    owner  => 'ubuntu',
    group  => 'ubuntu',
    mode   => '0755',
    require => File['/data/web_static/releases/test/index.html'],
  }

  # Change ownership of /data/ directory
  file { '/data/':
    ensure => directory,
    owner  => 'ubuntu',
    group  => 'ubuntu',
    recurse => true,
    require => File['/data/web_static/current'],
  }

  # Configure Nginx
  file { '/etc/nginx/sites-available/default':
    ensure  => file,
    content => template('setup_web_static/nginx_default.erb'),
    notify  => Service['nginx'],
    require => Package['nginx'],
  }

  # Restart Nginx service
  service { 'nginx':
    ensure    => running,
    enable    => true,
    subscribe => File['/etc/nginx/sites-available/default'],
  }
}

include setup_web_static
