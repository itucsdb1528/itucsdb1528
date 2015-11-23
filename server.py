import datetime
import json
import os
import psycopg2 as dbapi2
import re

from flask import Flask
from flask import redirect
from flask import render_template
from flask.helpers import url_for

app = Flask(__name__)

def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn

@app.route('/')
def home():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())

@app.route('/initdatabase')
def initialize_database():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        query = """DROP TABLE IF EXISTS MENSFITNESS"""
        cursor.execute(query)
        
        query = """DROP TABLE IF EXISTS WOMENSFITNESS"""
        cursor.execute(query)
        
        query = """CREATE TABLE MENSFITNESS
        (
        ID   INT              NOT NULL,
        NAME VARCHAR (30)     NOT NULL,
        AGE  INT              NOT NULL,
        ADDRESS  CHAR (25) ,
        SALARY   DECIMAL (18, 2),       
        PRIMARY KEY (ID)
        )"""
        cursor.execute(query)
        
        query = """CREATE TABLE WOMENSFITNESS
        (
        ID   INT              NOT NULL,
        NAME VARCHAR (30)     NOT NULL,
        AGE  INT              NOT NULL,
        ADDRESS  CHAR (25) ,
        SALARY   DECIMAL (18, 2),       
        PRIMARY KEY (ID)
        )"""
        cursor.execute(query)
        
        query = """INSERT INTO MENSFITNESS (ID, NAME, AGE)
        VALUES(001, 'GEORGE ARNOLD', 22)"""
        cursor.execute(query)
        
        query = """INSERT INTO MENSFITNESS (ID, NAME, AGE)
        VALUES(002, 'IVAN DROGO', 26)"""
        cursor.execute(query)
        
        query = """INSERT INTO WOMENSFITNESS (ID, NAME, AGE)
        VALUES(005, 'VICTORIA SCHARZKOPF', 19)"""
        cursor.execute(query)
        
        query = """INSERT INTO WOMENSFITNESS (ID, NAME, AGE)
        VALUES(057, 'ELIZABETH SECRET', 20)"""
        cursor.execute(query)
        
        connection.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    PORT = int(os.getenv('VCAP_APP_PORT', '5000'))
    
    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """user='vagrant' password='vagrant'
                               host='localhost' port=54321 dbname='itucsdb'"""
    
    app.run(host='0.0.0.0', port=int(PORT))