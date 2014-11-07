require 'json'

VAGRANTFILE_API_VERSION = '2'

settings = JSON.parse(IO.read('config.json'))

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = 'ubuntu/trusty64'
  config.vm.box_check_update = true

  if settings['vm']['forwarded']
    config.vm.network "forwarded_port", :guest => 80, :host => 8080
  end

  if settings['vm']['private']
    config.vm.network "private_network", :ip => settings['vm']['ip']
  end

  if settings['vm']['public']
    config.vm.network "public_network", :ip => settings['vm']['ip']
  end

  config.vm.synced_folder '.', '/vagrant', :mount_options => %w(dmode=777 fmode=666)

  settings['sharing'].each { |key, value|
    config.vm.synced_folder key, value, :mount_options => %w(dmode=777 fmode=666)
  }

  config.vm.provider 'virtualbox' do |vm|
    vm.name = settings['vm']['name']
    vm.customize [ 'modifyvm', :id, '--memory', '1024' ]
  end

  config.vm.provision :shell, :inline => 'python /vagrant/provision.py'
  config.vm.provision :shell, :inline => 'ifconfig eth1 | grep "inet addr"', :run => :always
  config.vm.provision :shell, :inline => 'service apache2 start', :run => :always
end
