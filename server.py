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

@app.route('/mensfitness') 
def mensfitness_page():
    return render_template('mensfitness.html') 

@app.route('/womensfitness') 
def womensfitness_page():
    return render_template('womensfitness.html') 

@app.route('/nutritionprograms') 
def nutritionprograms_page():
    return render_template('nutritionprograms.html') 

@app.route('/fitnessmachines') 
def fitnessmachines_page():
    return render_template('fitnessmachines.html') 

@app.route('/fitnessawards') 
def fitnessawards_page():
    return render_template('fitnessawards.html') 
    
@app.route('/ftypes') 
def ftypes_page():
    return render_template('ftypes.html')

@app.route('/frecords') 
def frecords_page():
    return render_template('frecords.html')

@app.route('/fdiet') 
def fdiet_page():
    return render_template('frecords.html')

@app.route('/muinf') 
def muinf_page():
    return render_template('frecords.html')

@app.route('/ffitnessers') 
def ffitnessers_page():
    return render_template('frecords.html')

@app.route('/initdatabase')
def initialize_database():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        query = """DROP TABLE IF EXISTS MENSFITNESS"""
        cursor.execute(query)
        
        query = """DROP TABLE IF EXISTS WOMENSFITNESS"""
        cursor.execute(query)
        
        query = """DROP TABLE IF EXISTS FITNESSTYPES"""
        cursor.execute(query)
        
        query = """DROP TABLE IF EXISTS DIETT"""
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
        
        query = """CREATE TABLE MENSFITNESS
        (
        ID   INT              NOT NULL,
        NAME VARCHAR (30)     NOT NULL,
        AGE  INT              NOT NULL,
        ADDRESS  CHAR (25) ,
        SALARY   DECIMAL (18, 2),
        WOMANRIVAL_ID INT,      
        PRIMARY KEY (ID),
        FOREIGN KEY (WOMANRIVAL_ID) REFERENCES WOMENSFITNESS(ID)
        )"""
        cursor.execute(query)
        
        query = """CREATE TABLE DIETT
        (
        DID   INT             NOT NULL,
        DNAME VARCHAR (30)             ,
        DAGE  INT                      ,
        DIETFROM  CHAR (25) ,
        DIETSTART  VARCHAR (30),       
        PRIMARY KEY (DID)
        )"""
        cursor.execute(query)
        
        query = """CREATE TABLE FITNESSTYPES
        (
        FTID   INT              NOT NULL ,
        RECOMMENDED_DIET INT,
        FTNAME VARCHAR (30),
        FTAGE  INT,
        FTFEES   DECIMAL (18, 2),       
        FOREIGN KEY (RECOMMENDED_DIET) REFERENCES DIETT (DID)
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
        
        query = """INSERT INTO DIETT (DID, DNAME, DAGE, DIETSTART)
        VALUES(1000, 'GEORGE ARNOLD', 22, '2 FEB' )"""
        cursor.execute(query)
        
        query = """INSERT INTO DIETT (DID, DNAME, DAGE, DIETSTART)
        VALUES(2000, 'GEORGE CLONI', 32, '10 FEB' )"""
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