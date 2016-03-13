from bears.configfiles.PuppetLintBear import PuppetLintBear
from tests.LocalBearTestHelper import verify_local_bear

good_file = """# == Class: puppet::config
#
# Manage the pupppet configuration files.
#
# === Authors
#
# David Wagner <dwagner@allegheny.edu>
#
{
  include puppet::params

  file { '/etc/puppet/puppet.conf':
    ensure  => present,
    content => template('puppet/puppet.conf.erb'),
    owner   => 'puppet',
    group   => 'puppet',
    require => Class['puppet::install'],
  }

  file { '/etc/puppet/auth.conf':
    ensure  => present,
    content => template('puppet/auth.conf.erb'),
    owner   => 'puppet',
    group   => 'puppet',
    require => Class['puppet::install'],
  }

  file { '/etc/default/puppet':
    ensure  => present,
    content => template('puppet/puppet.erb'),
    owner   => 'root',
    group   => 'root',
    require => Class['puppet::install'],
  }
}
""".splitlines(True)

bad_file = """# == Class: puppet::config
#
# Manage the pupppet configuration files.
#
# === Authors
#
# David Wagner <dwagner@allegheny.edu>
#
{
  include puppet::params

  file { '/etc/puppet/puppet.conf':
    ensure   => present,
    content  => template('puppet/puppet.conf.erb'),
    owner    => 'puppet',
    group    => 'puppet',
    require  => Class['puppet::install'],
  }

  file { '/etc/puppet/auth.conf':
    ensure  => present,
    content => template('puppet/auth.conf.erb'),
    owner   => 'puppet',
    group   => 'puppet',
    require => Class['puppet::install'],
  }

  file { '/etc/default/puppet':
    ensure  => present,
    content => template('puppet/puppet.erb'),
    owner   => 'root',
    group   => 'root',
    require => Class['puppet::install'],
  }
}
""".splitlines(True)

bad_file_cli_opts = """# == Class: puppet::config
#
# Manage the pupppet configuration files.
#
# === Authors
#
# David Wagner <dwagner@allegheny.edu>
#
class puppet::config {
  include puppet::params

  file { '/etc/puppet/puppet.conf':
    ensure  => present,
    content => template('puppet/puppet.conf.erb'),
    owner   => 'puppet',
    group   => 'puppet',
    require => Class['puppet::install'],
  }

  file { '/etc/puppet/auth.conf':
    ensure  => present,
    content => template('puppet/auth.conf.erb'),
    owner   => 'puppet',
    group   => 'puppet',
    require => Class['puppet::install'],
  }

  file { '/etc/default/puppet':
    ensure  => present,
    content => template('puppet/puppet.erb'),
    owner   => 'root',
    group   => 'root',
    require => Class['puppet::install'],
  }
}
""".splitlines(True)

good_file_cli_opts = """# == Class: puppet::config
#
# Manage the pupppet configuration files.
#
# === Authors
#
# David Wagner <dwagner@allegheny.edu>
#
class puppet::config {
  include puppet::params

  file { '/etc/puppet/puppet.conf':
    ensure  => present,
    content => template('puppet/puppet.conf.erb'),
    owner   => 'puppet',
    group   => 'puppet',
    require => Class['puppet::install'],
  }

  file { '/etc/puppet/auth.conf':
    ensure  => present,
    content => template('puppet/auth.conf.erb'),
    owner   => 'puppet',
    group   => 'puppet',
    require => Class['puppet::install'],
  }

  file { '/etc/default/puppet':
    ensure  => present,
    content => template('puppet/puppet.erb'),
    owner   => 'root',
    group   => 'root',
    require => Class['puppet::install'],
  }
}
""".splitlines(True)

PuppetLintBearTest = verify_local_bear(PuppetLintBear,
                                       valid_files=(good_file,),
                                       invalid_files=(bad_file,))

puppetLintBearWithSettings = verify_local_bear(PuppetLintBear,
                                               valid_files=(good_file_cli_opts,bad_file_cli_opts),
                                               invalid_files=(),
                                               settings={
                                                  "puppet_cli_options":
                                                  "--no-autoloader_layout-check"
                                                })
