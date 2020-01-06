from app import create_app
from waitress import serve
from paste.translogger import TransLogger


if __name__ == '__main__':
    app = create_app()
    # serve(app, host=app.config['HOST'], port=app.config['PORT'])
    # serve(app, host=app.config['HOST'], port=app.config['PORT'])
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
