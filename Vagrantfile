require 'json'

VAGRANTFILE_API_VERSION = '2'

settings = JSON.parse(IO.read('config.json'))

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = settings['vm']['image']
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

  for script in settings['provision-scripts'] 
    config.vm.provision :shell, :inline => script
  end

  for script in settings['run-scripts'] 
    config.vm.provision :shell, :inline => script, :run => :always
  end
  
  if settings['vm']['private'] || settings['vm']['public'] 
    config.vm.provision :shell, :inline => 'ifconfig eth1 | grep "inet addr"', :run => :always
  end
end
