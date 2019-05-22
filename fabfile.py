from fabric.api import local
from fabric.colors import green
# https://micropyramid.com/blog/automate-django-deployments-with-fabfile/

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

def migrate():
    local('python manage.py makemigrations')
    local('python manage.py migrate')