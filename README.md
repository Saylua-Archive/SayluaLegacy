[![Build Status](https://travis-ci.org/LikeMyBread/Saylua.svg?branch=master)](https://travis-ci.org/LikeMyBread/Saylua)
[![Coverage Status](https://coveralls.io/repos/github/LikeMyBread/Saylua/badge.svg)](https://coveralls.io/github/LikeMyBread/Saylua)

## Saylua

## Run Locally
If you are on Windows, it is heavily suggested you use Vagrant.

### Manual
1. Install [Python 2.7](https://www.python.org/downloads/)

      Note: Ensure you have pip 1.4+ installed with pip --version. If you do not, see: https://pip.pypa.io/en/latest/installing/

2. Install [NodeJS](https://nodejs.org/en/download/current/)

3. [Install the AppEngine SDK (Make sure you choose to install the original App Engine SDK for Python)](https://cloud.google.com/appengine/docs/python/download)

4. Install [MySQL Server](https://dev.mysql.com/downloads/mysql/)

5. Clone this repo and move to project directory:

      ```
      git clone git@bitbucket.org:saylua/saylua.git
      cd saylua
      ```

6. Install PIL dependencies zlib and libjpeg.

      Ubuntu users can do the following:

      ```
      sudo apt-get install libjpeg8-dev zlib1g-dev
      ```

      OS X users need only install libjpeg:
      See: https://dzone.com/articles/installing-libjpeg-os-x

8. Install python dependencies locally.
      `pip install -r requirements-dev.txt`
      `pip install -r requirements.txt -t lib`


9. Install NodeJS dependencies.

      `npm install && npm install -g gulp eslint eslint-plugin-inferno mocha webpack`

10. Create the file saylua/config/secure.py based on saylua/config/example_secure.py

11. Run this project locally from the command line:

      `sh run.sh`


### Vagrant
1. Ensure you have [Vagrant](https://www.vagrantup.com/downloads.html), and [VirtualBox](https://www.virtualbox.org/wiki/Downloads) installed.

      Note: VMWare Fusion users do not have to install VirtualBox.

2. Clone this repo and move to project directory:

      ```
      git clone git@bitbucket.org:saylua/saylua.git
      cd saylua
      ```

3. Install and provision project, SSH into VM:

      `vagrant up && vagrant ssh`

4. Run this project locally from the command line:

      ```
      cd /vagrant
      sh run.sh
      ```

Visit the application at [http://localhost:8080](http://localhost:8080)

See [the development server documentation](https://developers.google.com/appengine/docs/python/tools/devserver)
for options when running dev_appserver.

#### Notes:

- By default, the dev_appserver.py will track ALL changes to ALL directories, causing startup issues.
Making the following change reduces startup time exponentially, and gets rid of filewatcher limit problems.

            ## --> ./saylua/build/google_appengine/google/appengine/tools/devappserver2/watcher_common.py

            # Prevent watcher file limit issues.
            _IGNORED_DIRS = ('node_modules', '.git', '.vagrant', 'build', 'lib', 'static/')

            def skip_ignored_dirs(dirs):
                  """Skip directories that should not be watched."""

                  _remove_pred(dirs, lambda d: d.startswith(_IGNORED_PREFIX) or d in _IGNORED_DIRS)

## Authors

Mike Bradley
Noi Sek
Tiffany Zhang
