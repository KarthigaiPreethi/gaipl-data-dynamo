from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///platform.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def dashboard():
    return render_template('resources/dashboard.html')

@app.route('/infrastructure')
@login_required
def infrastructure():
    return render_template('resources/infrastructure.html')

@app.route('/monitoring')
@login_required
def monitoring():
    return render_template('resources/monitoring.html')

@app.route('/deployments')
@login_required
def deployments():
    return render_template('resources/deployments.html')

@app.route('/tickets')
@login_required
def tickets():
    return render_template('resources/tickets.html')

@app.route('/chatbot')
@login_required
def chatbot():
    return render_template('resources/chatbot.html')

@app.route('/ai-insights')
@login_required
def ai_insights():
    return render_template('resources/ai_insights.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and password == user.password:
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('resources/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            test_user = User(username='admin', password='admin')
            db.session.add(test_user)
            db.session.commit()
    app.run(debug=True)