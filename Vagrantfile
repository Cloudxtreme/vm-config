VAGRANTFILE_API_VERSION = '2'

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = 'ubuntu/trusty64'
  config.vm.box_check_update = true

  config.vm.network "forwarded_port", :guest => 80, :host => 8080
  config.vm.network "private_network", :ip => "192.168.33.11"
  #config.vm.network "public_network", :ip => "192.168.33.11"

  config.vm.synced_folder '.', '/vagrant', mount_options: ['dmode=777','fmode=666']
  config.vm.synced_folder './www', '/var/www', mount_options: ['dmode=777','fmode=666']
  config.vm.synced_folder './log', '/var/log', mount_options: ['dmode=777','fmode=666']

  config.vm.provider 'virtualbox' do |vm|
    vm.name = 'LAMP'
    vm.customize [ 'modifyvm', :id, '--memory', '1024' ]
  end

  config.vm.provision :shell, :inline => 'python /vagrant/provision.py'
  config.vm.provision :shell, :inline => 'ifconfig eth1 | grep "inet addr"', :run => :always
  config.vm.provision :shell, :inline => 'service apache2 start', :run => :always
end
