Server configurator
===================

Use python scripts to provisioning of linux server, can be used with Vagrant or generic servers.  

*NB: Scripts written for systems based on apt-get package manager (mainly Ubuntu)*

### Run in Vagrant VM (Vagrant mode)

Just clone repository application, edit `config.json` to configure VM and run:

    vagrant up

### Run on linux server (Standalone mode as example DigitalOcean)

To load provisioning script:

    curl https://raw.githubusercontent.com/aiskov/vm-config/master/loader.py | python

When finished. You will have directory with provisioning scripts, sample of `config.json` which you can change to proper configuration of the server, and installation url. When `config.json` file already changed you can run: 

    python provision.py

Provisioning will add script which will be run on server start or manually:

    python run.py

### Configuration

* name - Name (In VM used as VM name, in standalone as host name)
* location - Name of location to set time
* locale - code of locale and encoding for use in console

* cron-records - List of cron records
* provision-scripts - List of scripts for provisioning (installation)
* run-scripts - List of scripts run on start-up

#### Sample of standalone configuration

        {
            "name": "VM-Name",
            "location": "Europe/Warsaw",
            "locale": "en_US.UTF-8",

            "cron-records": [
                "0 12,20 * * * root python script/daily-backup.py",
                "0 0 * * 0 root python script/weekly-backup.py",
                "0 0 1 * * root python script/monthly-cleanup.py"
            ],

            "provision-scripts": [
                "python scripts/common.py",
                "python scripts/nginx-balancer.py"
            ],

            "run-scripts": [
                "echo 'Run application.'"
            ]
        }

#### Configuration available only in VM

* vm.image - Vagrant image name as example: ubuntu/trusty64
* vm.ip - Ip used for private networking
* vm.forwarding - List of ports for forwarding
* vm.private - Is visible for private networking
* vm.public - Is visible for public networking

* sharing - Shared folders as object `<key-host_folder>:<value-guest_folder>`

        {
            "name": "VM-Name",
            "location": "Europe/Warsaw",
            "locale": "en_US.UTF-8",

            "vm": {
                "image": "ubuntu/trusty32",

                "ip": "192.168.33.11",
                "forwarded": true,
                "private": false,
                "public": false
            },

            "provision-scripts": [
                "python scripts/common.py",
                "python scripts/nginx-balancer.py"
            ],

            "run-scripts": [
                "echo 'Run application.'"
            ]
        }

Useful links
============

* https://www.vagrantup.com/downloads
* https://www.virtualbox.org/wiki/Downloads 
