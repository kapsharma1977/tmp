

from . import create_app, g#, db, request
from flask_mongoengine import MongoEngine
# Start development web server
if __name__ == '__main__':
    app = create_app()
    def get_db():
        if 'db' not in g:
            g.db = MongoEngine()
            g.db.init_app(app)
        return g.db   
    # @app.before_request
    # def before_request():
    #     g.db = db.init_app(app) #connect_db()
    # @app.teardown_appcontext
    # def teardown_db(exception):
    #     db = g.pop('db', None)
    #     if db is not None:
    #         db.close()
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('cert.pem', 'key.pem'))