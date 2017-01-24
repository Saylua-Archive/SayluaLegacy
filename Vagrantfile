# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/xenial64"
  config.vm.network "forwarded_port", guest: 8080, host: 8080
  config.vm.network "forwarded_port", guest: 8000, host: 8000

  config.vm.provider "virtualbox" do |v|
    v.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/vagrant", "1"]
  end

  config.vm.provision "shell", inline: <<-SHELL
    echo "%% Updating system packages . . ."
    echo "========================================"
    sudo apt-get -qq update
    sudo apt-get -qq upgrade


    # Install and setup MySQL
    echo "%% Installing MySQL . . ."
    echo "========================================"
    DBHOST=localhost
    DBNAME=saylua
    DBUSER=root
    DBPASSWD=rootpass

    debconf-set-selections <<< "mysql-server mysql-server/root_password password $DBPASSWD"
    debconf-set-selections <<< "mysql-server mysql-server/root_password_again password $DBPASSWD"
    sudo apt-get -qq install mysql-server

    echo "%% Setting up MySQL . . ."
    echo "========================================"
    mysql -uroot -p$DBPASSWD -e "CREATE DATABASE $DBNAME"
    mysql -uroot -p$DBPASSWD -e "grant all privileges on $DBNAME.* to '$DBUSER'@'localhost' identified by '$DBPASSWD'"


    # Install Python and dependencies
    echo "%% Installing Python . . ."
    echo "========================================"
    sudo apt-get install -qq python python-pip python-dev libffi-dev
    cd /vagrant/


    # Install Pillow requirements prior to attempting to install pillow.
    echo "%% Installing Python dependencies . . ."
    echo "========================================"
    sudo apt-get -qq install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
    sudo pip install -r requirements.txt -t lib


    # Install Google AppEngine
    echo "%% Installing Google AppEngine . . ."
    echo "========================================"
    sudo apt-get -qq install unzip
    mkdir /vagrant/build
    cd /vagrant/build
    if [ -d build/google_appengine ]; then echo "AppEngine already installed, skipping download."; wget https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.40.zip --quiet ; fi
    unzip google_appengine_1.9.40.zip -n -qq


    # Ensure AppEngine commands are added to PATH
    echo "%% Adding AppEngine to PATH . . ."
    echo "========================================"
    echo "export PATH=$PATH:/vagrant/build/google_appengine/" >> /home/ubuntu/.bashrc


    # Install NodeJS and dependencies
    echo "%% Installing Node.js . . ."
    echo "========================================"
    curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
    sudo apt-get -qq install nodejs


    # Install Global deps
    echo "%% Installing Global Node.js dependencies . . ."
    echo "========================================"
    sudo npm install -g gulp eslint eslint-plugin-react webpack --loglevel=error

    echo "%% Installing Local Node.js dependencies . . ."
    echo "========================================"
    cd /vagrant/
    npm install --loglevel=error

  SHELL
end
