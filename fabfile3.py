from __future__ import with_statement
from fabric.api import run, env, cd, roles, parallel

env.roledefs = {
    'web': ['web@127.0.0.1'],
    'erp': ['erp@127.0.0.1'],
    'agency': ['agency@127.0.0.1'],
}
env.password = 'web'
env.port = 11235

PROJECT_DIR = 'workspace/youlun'


@parallel
@roles('web', 'erp', 'agency')
def pull_code():
    with cd(PROJECT_DIR):
        run('git pull origin master')


@parallel
@roles('web', 'erp', 'agency')
def update_virtualenv():
    with cd(PROJECT_DIR):
        run('pip install -r requirements.txt')


@parallel
@roles('web', 'erp', 'agency')
def collectstatic():
    with cd(PROJECT_DIR):
        run('echo "python manage.py collectstatic"')


@parallel
@roles('web', 'erp', 'agency')
def migrations():
    with cd(PROJECT_DIR):
        run('python manage.py migrate')


@parallel
@roles('web', 'erp', 'agency')
def reload_service():
    run('touch {}-uwsgi.ini'.format(env.user))
