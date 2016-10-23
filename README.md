## Saylua

## Run Locally
If you are on Windows, it is heavily suggested you use Vagrant.

### Manual
1. Install [Python 2.7](https://www.python.org/downloads/)
   Note: Ensure you have pip 1.4+ installed with pip --version. If you do not, see: https://pip.pypa.io/en/latest/installing/

2. Install [NodeJS](https://nodejs.org/en/download/current/)

3. [Install the AppEngine SDK (Make sure you choose to install the original App Engine SDK for Python)](https://cloud.google.com/appengine/docs/python/download)

4. Clone this repo and move to project directory:

   ```
   git clone git@bitbucket.org:saylua/saylua.git
   cd saylua
   ```

5. Install PIL dependencies zlib and libjpeg.
   ```
   # Ubuntu users can do the following:
   sudo apt-get install libjpeg8-dev zlib1g-dev

   # OS X users need only install libjpeg:
   # https://dzone.com/articles/installing-libjpeg-os-x
   ```

5. Install python dependencies locally.

   ```
   pip install -r requirements.txt -t lib
   ```

6. Install NodeJS dependencies.

   ```
   npm install && npm install -g gulp
   ```

7. Run this project locally from the command line:

   ```
   sh run.sh
   ```

### Vagrant
1. Ensure you have [Vagrant](https://www.vagrantup.com/downloads.html), and [VirtualBox](https://www.virtualbox.org/wiki/Downloads) installed.
   Note: VMWare Fusion users do not have to install VirtualBox.

2. Clone this repo and move to project directory:

   ```
   git clone git@bitbucket.org:saylua/saylua.git
   cd saylua
   ```

3. Install and provision project, SSH into VM:

   ```
   vagrant up && vagrant ssh
   ```

4. Run this project locally from the command line:

   ```
   cd /vagrant
   sh run.sh
   ```

Visit the application at [http://localhost:8080](http://localhost:8080)

See [the development server documentation](https://developers.google.com/appengine/docs/python/tools/devserver)
for options when running dev_appserver.

## Author
Tiffany Zhang
