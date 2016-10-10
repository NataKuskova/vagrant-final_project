from __future__ import with_statement
from fabric.api import *
# from fabric.contrib.console import confirm
import time
from contextlib import contextmanager as _contextmanager
from fabric.colors import red, green


repo = 'https://github.com/NataKuskova/final_project.git'
env.image_search_dir = 'final_project/image_search'
env.image_parser_dir = 'final_project/image_parser'
env.activate_env3 = '. .env/bin/activate'
env.activate_env2 = '. .env2.7/bin/activate'
env.app_dir = '/vagrant'


def install():
    run('sudo apt-get update')

    run('sudo apt-get install software-properties-common '
        'python-software-properties')
    run('sudo add-apt-repository ppa:fkrull/deadsnakes')
    run('sudo apt-get update')
    run('sudo apt-get install python3.5 supervisor')
    with cd('/usr/bin'):
        run('sudo rm python3')
        run('sudo ln -s python3.5 python3')

    run('sudo apt-get install git python-pip python-virtualenv')
    run('sudo apt-get install gcc lxml python-dev python3-dev python3.5-dev '
        'python3-tk redis-server libssl-dev libffi-dev nginx')

    # run('pip install uwsgi')
    run('sudo service nginx start')  # start nginx

    run('sudo cp /vagrant/final_project/image_search/image_search_nginx.conf /etc/nginx/service-available/image_search_nginx.conf')
    run('sudo ln -s /etc/nginx/sites-available/image_search_nginx.conf /etc/nginx/sites-enabled/')
    run('python manage.py collectstatic')
    run('sudo service nginx restart')

    """
    # pip install uwsgi
    # sudo apt-get install nginx
    # sudo service nginx start   # start nginx


    # sudo cp /vagrant/final_project/image_search/image_search_nginx.conf /etc/nginx/service-available/image_search_nginx.conf
    # sudo ln -s /etc/nginx/sites-available/image_search_nginx.conf /etc/nginx/sites-enabled/
    # python manage.py collectstatic
    # sudo service nginx restart
    uwsgi --socket /tmp/image_search.sock --module image_search.wsgi --chmod-socket=666
    """


def clone_repo():
    with cd(env.app_dir):
        run("git clone %s" % repo)


def create_virtuelenv3():
    with cd(env.app_dir):
        run('virtualenv -p /usr/bin/python3 .env')


@_contextmanager
def virtualenv3():
    with cd(env.app_dir):
        with prefix(env.activate_env3):
            yield


def requirements3():
    with virtualenv3():
        with cd(env.app_dir):
            run('pip install -r %s/requirements.txt' % env.image_search_dir)
            # run('pip freeze')


def create_virtuelenv2():
    with cd(env.app_dir):
        run('virtualenv -p /usr/bin/python .env2.7')


@_contextmanager
def virtualenv2():
    with cd(env.app_dir):
        with prefix(env.activate_env2):
            yield


def requirements2():
    with virtualenv2():
        run('pip install -r %s/requirements.txt' % env.image_parser_dir)
        # run('pip freeze')


def runserver():
    # with cd(env.app_dir + '/' + env.image_search_dir):
    with virtualenv3():
        # run('python ' + env.image_search_dir + '/manage.py runserver 0.0.0.0:8000 &')
        # run('uwsgi --socket /tmp/image_search.sock --module image_search.wsgi --chmod-socket=666 -d 1')
        run('uwsgi --ini final_project/image_search/image_search_uwsgi.ini -d uwsgi_logs')


# def run_socketserver():
#     with virtualenv3():
#         run('python %s/search_img/server.py' % env.image_search_dir)


def run_supervisord():
    # run('sudo unlink /tmp/supervisor.sock')
    with virtualenv2():
        run('supervisord -c supervisord.conf')


def supervisord_shutdown():
    with virtualenv2():
        run('supervisorctl shutdown')


def vagrant():
    # change from the default user to 'vagrant'
    env.user = 'vagrant'
    # connect to the port-forwarded ssh
    env.hosts = ['127.0.0.1:2222']

    # find running VM (assuming only one is running)
    result = local('vagrant global-status | grep running', capture=True)
    machineId = result.split()[0]

    # use vagrant ssh key for the running VM
    result = local(
        'vagrant ssh-config {} | grep IdentityFile'.format(machineId),
        capture=True)

    env.key_filename = result.split()[1]


def deploy():
    # run('uname -a')
    # run('vagrant up')
    # run('vagrant reload --provision')
    # vagrant()
    # install()
    # clone_repo()
    # create_virtuelenv3()
    # requirements3()
    # create_virtuelenv2()
    # requirements2()
    runserver()
    run_supervisord()
    print(green("Deployment complete! You can visit the website at "
          "127.0.0.1:8000"))
