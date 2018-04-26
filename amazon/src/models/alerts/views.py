from flask import Blueprint, render_template, request, session, url_for, redirect
from models.alerts.alert import Alert
import models.users.decorators as user_decorators

alert_blueprint = Blueprint('alerts', __name__)


@alert_blueprint.route('/')
def index():
    return "This is the alerts index"


@alert_blueprint.route('/new', methods=['GET','POST'])
@user_decorators.requires_login
def create_alert():
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        price_limit = float(request.form['price_limit'])

        # print(name)
        # print(url)
        # print(price_limit)

        price_from_amazon = Alert.load_price(url)

        # item = Item(name,url,price_limit)
        # item.save_to_mongo()
        # _id = item.get_id()
        #print(_id)
        alert = Alert(session['email'],price_limit,name,url,price_from_amazon,active=True,last_checked=None)
        print("alert created")
        alert.save_to_mongo()
        return redirect(url_for('users.user_alerts'))

    return render_template('alerts/new_alert.html')


@alert_blueprint.route('/<string:alert_id>')
def get_alert_page(alert_id):
    alert = Alert.find_by_id(alert_id)
    print(alert)
    return render_template('alerts/alert.html', alert=alert)

@alert_blueprint.route('/deactivate/<string:alert_id>')
def deactivate_alert(alert_id):
    alert = Alert.find_by_id(alert_id)
    alert.deactivate()
    print('in deactivate')
    return redirect(url_for('users.user_alerts'))

@alert_blueprint.route('/activate/<string:alert_id>')
def activate_alert(alert_id):
    alert = Alert.find_by_id(alert_id)
    alert.activate()
    print('in activate')
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/edit/<string:alert_id>', methods=['GET','POST'])
def edit_alert(alert_id):
    alert = Alert.find_by_id(alert_id)
    if request.method == 'POST':
        print('post')
        price_limit = float(request.form['price_limit'])
        alert.price_limit = price_limit
        alert.save_to_mongo()
        return redirect(url_for('users.user_alerts'))


    return render_template('alerts/edit_alert.html', alert=alert)


@alert_blueprint.route('/check_price/<string:alert_id>')
def check_alert_price(alert_id):
    alert = Alert.find_by_id(alert_id)
    alert.load_item_price()
    return redirect(url_for('users.user_alerts'))

@alert_blueprint.route('/delete/<string:alert_id>')
def delete_alert(alert_id):
    alert = Alert.find_by_id(alert_id)
    alert.delete()
    return redirect(url_for('users.user_alerts'))























