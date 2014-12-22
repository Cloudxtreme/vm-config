require 'json'

VAGRANTFILE_API_VERSION = '2'

settings = JSON.parse(IO.read('config.json'))
Dir.mkdir './log' unless Dir.exists? './log'

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.box = settings['vm']['image']
    config.vm.box_check_update = true

    if settings['vm']['forwarding']
        settings['vm']['forwarding'].each { |forward|
            if forward.is_a? String
                config.vm.network "forwarded_port", :guest => forward, :host => forward
            else
                config.vm.network "forwarded_port", :guest => forward['guest'], :host => forward['host']
            end
        }
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
        vm.customize ['modifyvm', :id, '--memory', '1024']
    end

    if settings['provision-scripts']
        config.vm.provision :shell, :inline => '[ -d "scripts" ] || ln -s /vagrant/scripts'

        settings['provision-scripts'].each { |script|
            config.vm.provision :shell, :inline => script
            config.vm.provision :shell, :inline => script
        }
    end

    if settings['run-scripts']
        settings['run-scripts'].each { |script|
            config.vm.provision :shell, :inline => script, :run => :always
        }
    end

    if settings['vm']['private'] || settings['vm']['public']
        config.vm.provision :shell, :inline => 'ifconfig eth1 | grep "inet addr"', :run => :always
    end
end
