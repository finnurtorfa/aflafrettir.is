uWSGI configuration
=====================

This configuration file assumes that you have installed uWSGI under you
*virtualenv* environment and that you are running upstart

    pip install uwsgi

Rename the uwsgi configuration file and the uwsgi upstart configuration file.

    cp uwsgi.ini.example yourapplication_uwsgi.ini
    cp uwsgi_upstart.conf.example uwsgi.conf

Make all necessary modification and Create the uWSGI directory structure as well
as the log directory

    mkdir -p /etc/uwsgi/apps-enabled/
    mkdir -p /var/log/uwsgi

The owner and group owner of the log directory should be the same as the runner of the
uwsgi process(www-data:www-data in our case). Create a symlink to the configuration file

    ln -s yourapplication_uwsgi.ini /etc/uwsgi/apps-enabled
    ln -s uwsgi.conf /etc/init

To start the application and to restart the process when you update your files
just issue the following command:

    touch UWSGI_RELOAD
