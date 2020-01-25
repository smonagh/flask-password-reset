from app import db, mail
from app.email import send_email
from flask import request, redirect, url_for, render_template, Blueprint
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from app.models import User
import flask_login

app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('login.html'), 200

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        if username and password:
            print(request.values)
            if User.login_user(username, password):
                return redirect(url_for('app_routes.home_page')), 200

        return render_template('login.html'), 400

    return render_template('login.html'), 400

@app_routes.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'GET':
        return render_template('register.html'), 200

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        if username and password and email:
            user_created = User.create_user(username, password, email)

            if user_created:
                return redirect(url_for('app_routes.login'))
            else:
                return render_template('register.html'), 400

        return render_template('register.html'), 400

@app_routes.route('/password_reset', methods=['GET', 'POST'])
def reset():

    if request.method == 'GET':
        return render_template('reset.html')

    if request.method == 'POST':

        email = request.form.get('email')
        user = User.verify_email(email)

        if user:
            send_email(user)

        return redirect(url_for('app_routes.login'))

@app_routes.route('/password_reset_verified/<token>', methods=['GET', 'POST'])
def reset_verified(token):

    user = User.verify_reset_token(token)
    if not user:
        print('no user found')
        return redirect(url_for('app_routes.login'))

    password = request.form.get('password')
    if password:
        user.set_password(password, commit=True)

        return redirect(url_for('app_routes.login'))

    return render_template('reset_verified.html')



@flask_login.login_required
@app_routes.route('/home', methods=['GET'])
def home_page():
    return render_template('home.html'), 200
