from flask import Flask, render_template, flash
from forms import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate


app = Flask(__name__)


# Create a secret key for CSRF protection
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'

# Create db instance
db = SQLAlchemy(app)

# Create Migrate instance
migrate = Migrate(app, db)



from models.users import User 

# create all tables before running the app

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('Form submitted successfully')
                
    return render_template('name.html', name=name, form=form)


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        user = User(username=name, email = email)
        db.session.add(user)
        db.session.commit()
        flash('User added successfully')
        form.name.data = ''
    return render_template('add_user.html', form=form)










if __name__ == '__main__':
    app.run(debug=True)