from database import Database
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import uuid
import datetime

class Alert(object):
    COLLECTION_NAME = 'alerts'
    ALERT_TIMEOUT = 10

    def __init__(self,user_email,price_limit,name,url,price,active,alert_id=None,last_checked=None):
        self.user_email = user_email
        self.price_limit = price_limit
        self.name = name
        self.url = url
        self.price = price
        self.active = active
        self.alert_id = uuid.uuid4().hex if alert_id is None else alert_id
        self.last_checked = datetime.datetime.utcnow() if last_checked is None else last_checked

    @staticmethod
    def load_price(url):
        ua = UserAgent()
        header = {'user-agent': ua.chrome}
        page = requests.get(url,headers=header)
        soup = BeautifulSoup(page.text, 'lxml')
        price = soup.find_all('span', attrs={"id": "priceblock_ourprice"})
        money = price[0].string
        try:
            return float(money[1:])
        except:
            clean_money = money.replace(",","")
            return float(clean_money[1:])


    def save_to_mongo(self):
        #Database.insert(Alert.COLLECTION_NAME, self.json())
        Database.update(Alert.COLLECTION_NAME, {"alert_id": self.alert_id}, self.json())

    def json(self):
        return{
            "user_email":self.user_email,
            "price_limit":self.price_limit,
            "name":self.name,
            "url":self.url,
            "price":self.price,
            "active":self.active,
            "alert_id":self.alert_id,
            "last_checked":self.last_checked
        }


    def create_alert(self):
        pass

    @classmethod
    def find_by_user_email(cls, user_email):
        alerts = Database.find(Alert.COLLECTION_NAME, {'user_email': user_email})
        alerts_list = []
        #items_list = []
        for alert in alerts:
            x = Alert(alert['user_email'],alert['price_limit'],alert['name'],alert['url'],alert['price'],alert['active'],alert['alert_id'],alert['last_checked'])
            alerts_list.append(x)
            #item = Item.get_by_id(alert['item_id'])
            #items_list.append(item)

        return alerts_list


    @staticmethod
    def find_by_id(alert_id):
        alert = Database.find_one(Alert.COLLECTION_NAME, {'alert_id': alert_id})
        print(alert)
        return Alert(alert['user_email'],alert['price_limit'],alert['name'],alert['url'],alert['price'],alert['active'],alert['alert_id'],alert['last_checked'])


    def deactivate(self):
        self.active = False
        self.save_to_mongo()

    def activate(self):
        self.active = True
        self.save_to_mongo()

    def load_item_price(self):
        self.load_price(self.url)
        self.last_checked = datetime.datetime.utcnow()
        self.save_to_mongo()

    def delete(self):
        Database.remove(Alert.COLLECTION_NAME, {'alert_id': self.alert_id})

    @staticmethod
    def find_needing_update(minutes_since_update=1):
        last_updated_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=minutes_since_update)
        needing_update = Database.find(Alert.COLLECTION_NAME,{"last_checked": {"$lte": last_updated_limit}, "active":True})
        alerts_needing_update = []
        for alert in needing_update:
            x = Alert(alert['user_email'],alert['price_limit'],alert['name'],alert['url'],alert['price'],alert['active'],alert['alert_id'],alert['last_checked'])
            alerts_needing_update.append(x)
        return alerts_needing_update

    def send_email_if_price_reached(self):
        if float(self.price) < float(self.price_limit):
            self.send()
            print('sending email to {}'.format(self.user_email))

    def send(self):
        print("calling mailgun api")
        requests.post(
            "https://api.mailgun.net/v3/sandbox22a2125bd425489988f3dac8f5457955.mailgun.org/messages",
            auth=("api", "key-dc8342eaab860ea9ae9ee5767d15d7f2"),

            data={"from": "Mailgun Sandbox <postmaster@sandbox22a2125bd425489988f3dac8f5457955.mailgun.org>",
                  "to": "Jonathan Spivack <{}>".format("spivack.jonathan@gmail.com"),
                  "subject": "Hello Jonathan Spivack",
                  "text": "Congratulations Jonathan Spivack, you just sent an email with Mailgun!  You are truly awesome!"})




