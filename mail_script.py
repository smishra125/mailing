import requests
from flask import Flask
from flask_pymongo import PyMongo
import simplejson as json
from flask_cors import CORS
from flask import request, jsonify

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/parserdb"
mongo = PyMongo(app)
CORS(app)

def mail(db_data):
    url = "http://13.233.236.200:8080/service-email/MailService"
    # print(db_data)

    payload = "{\n\t\"user\":\"whirlybirdmailer\",\n\t\"password\":\"monster@123\",\n\t\"to\":[\"{{email}}\"],\n\t\"cc\":[],\n\t\"bcc\":[],\n\t\"subject\":\"mail for the site\",\n\t\"message_body\":\"<h2>Dear team,</h2><p>Please find the Daily Generation details as below :<p><table><tr><th>Plant Name</th><th>Capacity</th><th>Lifetime Generation</th><th>Today's Energy</th></tr>{{table_data}}</table>\n<p>Thank You</p><p>The SolarPro Team</p>\n\"\n}"

    table_data_str = ""
    new_email = ""

    for row in db_data:
        table_data_str += f"<tr><td>{row['Plant_name']}</td><td>{row['Capacity']}</td><td>{row['Lifetime_Generation']}</td><td>{row['Today_energy']}</td></tr>"
    payload = payload.replace("{{table_data}}", table_data_str)

    try:
        for add in db_data:
            new_email = f"{add['user_email']}"
        payload = payload.replace("{{email}}", new_email)
    except KeyError:
        pass

    headers = {
      'Content-Type': 'application/json',
      'Content-Type': 'text/plain'
    }

    Postresponse = requests.request("POST", url, headers=headers, data = payload)
    # print(Postresponse.text.encode('utf8'))

m_user = list(mongo.db.m_user.find({}, {'_id': 0, "user_id" : 1, "user_pass" : 2, "user_name" : 3, "accessible_sites" : 4, "user_email" : 5 }))
for user in m_user:
    response = {}
    user_response = []
    response.update(user)
    for site in user["accessible_sites"]:
        plant_record = list(mongo.db.plant_laststatus.find({"site_id": {"$in": [site]}}, {'_id': 0, "p_today_energy": 1, "p_total_energy": 2}).sort("record_time", -1).limit(1))
        sites = list(mongo.db.m_site.find({"site_id": {"$in": [site]}}, {'_id': 0, "site_id": 1, "site_name": 2, "customer_id": 3, "plant_capacity": 4}))

        for plant in plant_record:
            today_energy = plant.get('p_today_energy')
            total_energy = plant.get('p_total_energy')
            response.update({"Today_energy": today_energy})
            response.update({"Lifetime_Generation": total_energy})
        for site in sites:
            site_name = site.get('site_name')
            site_capacity = site.get('plant_capacity')
            response.update({"Plant_name": site_name})
            response.update({"Capacity": site_capacity})
    user_response.append(response)
    mail(user_response)
    # print(user_response)


