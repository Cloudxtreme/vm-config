VAGRANTFILE_API_VERSION = '2'

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = 'ubuntu/trusty64'
  config.vm.box_check_update = true

  config.vm.network "private_network", ip: "192.168.33.11"

  config.vm.synced_folder '.', '/vagrant'
  config.vm.synced_folder './www', '/var/www'
  config.vm.synced_folder './log', '/var/log'

  config.vm.provider 'virtualbox' do |vm|
    vm.name = 'LAMP'
    vm.customize ['modifyvm', :id, '--memory', '1024']
  end

  config.vm.provision :shell, :inline => 'python /vagrant/provision.py'
  config.vm.provision :shell, :inline => 'ifconfig eth1 | grep "inet addr"', :run => :always
end
