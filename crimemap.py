import json
from flask import Flask
from flask import render_template
from flask import request

# This section checks if is in development enviroment or production

import dbconfig

if dbconfig.test:
    from mockdbhelper import MockDBHelper as DBHelper
else:
    from dbhelper import DBHelper


app = Flask(__name__)
DB = DBHelper()

@app.route('/')
def home():
    crimes = DB.get_all_crimes()
    crimes = json.dumps(crimes)
    return render_template('home.html', crimes=crimes)

@app.route('/submitcrime', methods=['POST'])
def submitcrime():
    category = request.form.get('category')
    date = request.form.get('date')
    latitude = float(request.form.get('latitude'))
    longitude = float(request.form.get('longitude'))
    description = request.form.get('description')
    DB.add_crime(category, date, latitude, longitude, description)
    return home()

@app.route('/clear')
def clear():
    try:
        DB.clear_all()
    except Exception as e:
        print(e)
    return home()

if __name__=='__main__':
    app.run(port = 5000, debug = True)
