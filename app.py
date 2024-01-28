from flask import Flask
from apps import app as APP,init

app = Flask(__name__,static_url_path='', static_folder='templates',template_folder='templates')
app.secret_key = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'

app.register_blueprint(APP)
init(app)

if __name__ == "__main__":
    app.run(debug=True)