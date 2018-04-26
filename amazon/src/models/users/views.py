from flask import Blueprint, session, request, url_for, redirect, render_template
from models.users.user import User
user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/register',methods=['GET','POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if User.register_user(email,password):
            session['email'] = email
            return redirect(url_for(".user_alerts"))
        else:
            return render_template("users/register.html")

    return render_template("users/register.html")


@user_blueprint.route('/alerts')
#@user_decorators.requires_login
def user_alerts():
    user = User.find_by_email(session['email'])
    alerts= user.get_alerts()
    return render_template('users/alerts.html', alerts=alerts)


@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    return redirect(url_for('home'))

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if User.is_login_valid(email,password):
            session['email'] = email
            return redirect(url_for(".user_alerts"))

    return render_template("users/login.html")
