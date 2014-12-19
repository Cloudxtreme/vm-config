Server configurator
===================

Use python scripts to provisioning of linux server, can be used with Vagrant or generic servers.  

### Run in Vagrant VM

Just run application.

### Run on linux server (DigitalOcean)

To load provisioning script:

    curl https://raw.githubusercontent.com/aiskov/vm-config/develop/loader.py | python

When finished. You will have directory with provisioning scripts, sample of `config.json` which you can change to proper configuration of the server, and installation url. When `config.json` file already changed you can run: 

    python install.py
