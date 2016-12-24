import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from rio.app import db, create_app
from rio.models.base import Base


key = 'APP_ENVIRONMENT'
default_env = 'lcl'
if key not in os.environ:
    print("%s is not set, defaulting to %s." % (key, default_env))
    os.environ.setdefault(key, default_env)

env_name = os.environ[key].lower()
assert env_name in ['lcl', 'dev'], '%s must be either "lcl", "dev" or undefined'

print("Environment variable: %s=%s" % (key, env_name))

application = create_app(environment=env_name)
migrate = Migrate(application, Base)
manager = Manager(application)
manager.add_command('db', MigrateCommand)

@manager.command
def test():
	pass

if __name__ == "__main__":
    manager.run()