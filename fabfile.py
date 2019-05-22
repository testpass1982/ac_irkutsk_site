from fabric.api import local

def backup():
    print('pulling remote repo...')
    local('git pull')
    print('adding all changes to repo...')
    local('git add .')

    print("enter your comment:")
    comment = input()
    local('git commit -m "{}"'.format(comment))
    print('pushing master...')
    local('git push -u origin master')