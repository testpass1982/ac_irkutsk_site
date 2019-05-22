from fabric.api import * 
from fabric.colors import green

# env.use_ssh_config = False
# env.disable_known_hosts = True
# from fabric import Connection
# https://micropyramid.com/blog/automate-django-deployments-with-fabfile/
import json


try:
    with open("secret.json") as secret_file:
        secret = json.load(secret_file)
        env.update(secret)
except FileNotFoundError:
    print('***ERROR: no secret file***')

def test():
    # get_secret()
    run('ls -la')
    run('uname -a')

def backup():
    print(green('pulling remote repo...'))
    local('git pull')
    print(green('adding all changes to repo...'))
    local('git add .')

    print(green("enter your comment:"))
    comment = input()
    local('git commit -m "{}"'.format(comment))
    print(green('pushing master...'))
    local('git push -u origin master')

def migrate():
    local('python manage.py makemigrations')
    local('python manage.py migrate')

def deploy():
    local("python manage.py test")
    local('pip freeze > requirements.txt')
    local('git pull')
    # local('git add -p && git commit')
    
    print(green("enter your comment:"))
    comment = input()
    local('git commit -m "{}"'.format(comment))
    local('git push -u origin master')
    #switch_debug("True", "False")
    local('python manage.py collectstatic --noinput')
    #switch_debug("False", "True")
