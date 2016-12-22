from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from rio.app import db, create_app
from rio.models.base import Base

application = create_app(environment='dev')
# application = create_app()
application.config['DEBUG'] = True

migrate = Migrate(application, Base)

manager = Manager(application)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()