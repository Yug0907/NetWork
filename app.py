from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#flask and sqlalchemy database
app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

#database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


#home page
@app.route('/')
def home():
    return render_template('home.html')


# Sign up page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name=name, email=email, password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except:
            db.session.rollback()
            return redirect(url_for('signup'))

    return render_template('signup.html')  



#login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email, password=password).first()
        
        if user:
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('login'))

    return render_template('login.html')  


#dashboard page
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


#running the application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()    
    app.run(debug=True)
