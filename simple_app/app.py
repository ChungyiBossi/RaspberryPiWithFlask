import os
from flask import Flask
from .blueprint import simple_route
from .postgreSQL.session import create_sql_scoped_session, create_engine
from .postgreSQL.tables import LineUser

def create_flask_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)  # load relative configure
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    app.config.from_pyfile('config.py', silent=True)
    # envirenment vars check
    if not (app.config.get('GOOGLE_API_KEY') and app.config.get('LINE_CHANNEL_ACCESS_TOKEN')):
        app.logger.warn("Setup Your GOOGLE API Key and Line Channel ACT as envirenment variable correctly")
    # register blueprint
    app.register_blueprint(simple_route)
    # create db
    app.db_engine = create_engine(url=app.config.get('POSTGRESQL_DB_URL'))

    return app