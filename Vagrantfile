# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

    config.vm.box = "ubuntu/trusty64"

    # Ensure that files in /vagrant are not executable, so that nose will pick up any tests
    config.vm.synced_folder "./", "/vagrant",
        id: "vagrant-root",
        mount_options: ["dmode=775,fmode=664"]

    # Enable provisioning with a shell script. Additional provisioners such as
    # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
    # documentation for more information about their specific syntax and use.
    config.vm.provision "shell", inline: <<-SHELL
        sudo apt-get -y install python-software-properties
        sudo add-apt-repository -y ppa:fkrull/deadsnakes
        sudo apt-get update
        
        sudo apt-get -y install python2.7 python3.2 python3.3 python3.4 python3.5 pypy
        sudo apt-get install -y python-pip python3-pip
                
        sudo pip install setuptools --upgrade
        sudo pip3 install setuptools --upgrade
        sudo pip install tox
    SHELL
end
