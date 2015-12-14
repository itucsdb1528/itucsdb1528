import datetime
import json
import os
import psycopg2 as dbapi2
import re

from flask import request
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

@app.route('/mensfitness', methods=['GET', 'POST']) 
def mensfitness_page():    
    
    if request.method == 'GET':
        menfitnesses = get_menfitness()
    
    if 'menfitness_add' in request.form:
        ido = request.form['ID']
        name = request.form['NAME']
        age = request.form['AGE']
        height = request.form['HEIGHT']
        weight = request.form['WEIGHT']
        favmachine = request.form['FAV_MACHINE']
        award = request.form['LAST_AWARD']
        program = request.form['NUT_PROGRAM']

        add_menfitness(ido, name, age, height, weight, favmachine, award, program)
        
        menfitnesses = get_menfitness()
    
    print(menfitnesses)
    return render_template('mensfitness.html', menfitnesser = menfitnesses) 

@app.route('/womensfitness', methods=['GET', 'POST']) 
def womensfitness_page():
        
    if 'womenfitness_add' in request.form:
        ido = request.form['ID']
        name = request.form['NAME']
        age = request.form['AGE']
        height = request.form['HEIGHT']
        weight = request.form['WEIGHT']
        favmachine = request.form['FAV_MACHINE']
        award = request.form['LAST_AWARD']
        program = request.form['NUT_PROGRAM']

        add_menfitness(ido, name, age, height, weight, favmachine, award, program)
    
    return render_template('womensfitness.html') 

@app.route('/nutritionprograms', methods=['GET', 'POST']) 
def nutritionprograms_page():

    if 'nutritionprograms_add' in request.form:
        ido = request.form['ID']
        name = request.form['NAME']
        calories = request.form['CALORIES']

        add_nutritionprogram(ido, name, calories)

    return render_template('nutritionprograms.html') 

@app.route('/fitnessmachines', methods=['GET', 'POST']) 
def fitnessmachines_page():

    if 'fitnessmachines_add' in request.form:
        ido = request.form['ID']
        name = request.form['NAME']
        working_muscles = request.form['WORKING_MUSCLES']

        add_fitnessmachine(ido, name, working_muscles)    

    return render_template('fitnessmachines.html') 

@app.route('/fitnessawards', methods=['GET', 'POST']) 
def fitnessawards_page():
    
    if 'fitnessawards_add' in request.form:
        ido = request.form['ID']
        branch = request.form['BRANCH']

        add_fitnessaward(ido, branch) 
    
    return render_template('fitnessawards.html') 

def add_menfitness(ido, name, age, height, weight, favmachine, award, program):
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        cursor.execute("""INSERT INTO MENSFITNESS (ID, NAME, AGE, HEIGHT, WEIGHT, FAV_MACHINE, LAST_AWARD, NUT_PROGRAM)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s)""", (ido, name, age, height, weight, favmachine, award, program))

        connection.commit()

        return True
    
def get_menfitness():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM MENSFITNESS")
        menfitness = cursor.fetchall()
        
        connection.commit()
        
        return menfitness
    
def add_womenfitness(ido, name, age, height, weight, favmachine, award, program):
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        cursor.execute("""INSERT INTO WOMENSFITNESS (ID, NAME, AGE, HEIGHT, WEIGHT, FAV_MACHINE, LAST_AWARD, NUT_PROGRAM)
        VALUES(%s, %s, %s, %s, %s, 302, 902, 202)""", (ido, name, age, height, weight))

        connection.commit()

        return True
    
def get_womenfitness():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM WOMENSFITNESS")
        womenfitness = cursor.fetchall()
        
        connection.commit()
        
        return womenfitness
    
def add_nutritionprogram(ido, name, calories):
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        cursor.execute("""INSERT INTO NUTRITIONPROGRAMS (ID, NAME, CALORIES)
        VALUES(%s, %s, %s)""", (ido, name, calories))

        connection.commit()

        return True
    
def get_nutritionprogram():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM NUTRITIONPROGRAMS")
        nutritionprograms = cursor.fetchall()
        
        connection.commit()
        
        return nutritionprograms
    
def add_fitnessmachine(ido, name, working_muscle):
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        cursor.execute("""INSERT INTO FITNESSMACHINES (ID, NAME, WORKING_MUSCLES)
        VALUES(%s, %s, %s)""", (ido, name, working_muscle))

        connection.commit()

        return True
    
def get_fitnessmachine():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM FITNESSMACHINES")
        fitnessmachine = cursor.fetchall()
        
        connection.commit()
        
        return fitnessmachine
    
def add_fitnessaward(ido, branch):
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        cursor.execute("""INSERT INTO FITNESSAWARDS (ID, BRANCH)
        VALUES(%s, %s)""", (ido, branch))

        connection.commit()

        return True

def get_fitnessaward():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM FITNESSAWARDS")
        fitnessaward = cursor.fetchall()
        
        connection.commit()
        
        return fitnessaward

@app.route('/ftypes') 
def ftypes_page():
    return render_template('ftypes.html')

@app.route('/frecords') 
def frecords_page():
    return render_template('frecords.html')

@app.route('/fdiet', methods=['GET', 'POST']) 
def fdiet_page():    
    
    if 'fdiet_add' in request.form:
        ido = request.form['DID']
        name = request.form['DNAME']
        age = request.form['DAGE']
        height = request.form['DIETFROM']
        weight = request.form['DIETSTART']
    

        add_fdiet(ido, name, age, dfrom, dstart)
    
    return render_template('fdiet.html') 

def add_fdiet(ido, name, age, dfrom, dstart):
     with dbapi2.connect(app.config['dsn']) as connection:
         cursor = connection.cursor()
         
         cursor.execute("""INSERT INTO DIETT (DID, DNAME, DAGE, DIETFROM, DIETSTART)
         VALUES(%s, %s, %s, %s, %s)""", (ido, name, age, dfrom, dstart))
         
         connection.commit()
         
         return True

@app.route('/muinf') 
def muinf_page():
    return render_template('muinf.html')

@app.route('/ffitnessers') 
def ffitnessers_page():
    return render_template('ffitnessers.html')

@app.route('/update_DIETT')
def update_DIETT():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        query = """UPDATE DIETT
        SET DNAME = 'jORGE W BUSH'
        WHERE DID = 3000"""
        cursor.execute(query)
    
        connection.commit()
    return redirect(url_for('home'))


@app.route('/delete_values')
def delete_values():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        query = """DELETE FROM MENSFITNESS
        WHERE ID = 001"""
        cursor.execute(query)
    
        connection.commit()
    return redirect(url_for('home'))

@app.route('/delete_DIETT')
def delete_DIETT():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        query = """DELETE FROM DIETT
        WHERE DID = 1000"""
        cursor.execute(query)
    
        connection.commit()
    return redirect(url_for('home'))


@app.route('/initdatabase')
def initialize_database():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        query = """DROP TABLE IF EXISTS MENSFITNESS CASCADE"""
        cursor.execute(query)
        
        query = """DROP TABLE IF EXISTS WOMENSFITNESS CASCADE"""
        cursor.execute(query)
        
        query = """DROP TABLE IF EXISTS NUTRITIONPROGRAMS CASCADE"""
        cursor.execute(query)
        
        query = """DROP TABLE IF EXISTS FITNESSMACHINES CASCADE"""
        cursor.execute(query)
        
        query = """DROP TABLE IF EXISTS FITNESSAWARDS CASCADE"""
        cursor.execute(query)
        
        query = """DROP TABLE IF EXISTS DIETT CASCADE"""
        cursor.execute(query)
        
        query = """DROP TABLE IF EXISTS FITNESSTYPES CASCADE"""
        cursor.execute(query)
        
        query = """CREATE TABLE NUTRITIONPROGRAMS
        (
        ID   INT              NOT NULL,
        NAME VARCHAR (30)     NOT NULL,
        CALORIES INT,
        PRIMARY KEY(ID)
        )"""
        cursor.execute(query)
        
        query = """CREATE TABLE FITNESSMACHINES
        (
        ID   INT              NOT NULL,
        NAME VARCHAR (30)     NOT NULL,
        WORKING_MUSCLES VARCHAR(50),
        PRIMARY KEY(ID)
        )"""
        cursor.execute(query)
        
        query = """CREATE TABLE FITNESSAWARDS
        (
        ID   INT              NOT NULL,
        BRANCH VARCHAR(50)    NOT NULL,
        PRIMARY KEY(ID)
        )"""
        cursor.execute(query)
        
        query = """CREATE TABLE MENSFITNESS
        (
        ID   INT              NOT NULL,
        NAME VARCHAR (30)     NOT NULL,
        AGE  INT,
        HEIGHT INT,
        WEIGHT INT,
        FAV_MACHINE INT,
        LAST_AWARD INT,
        NUT_PROGRAM INT,
        PRIMARY KEY (ID),
        FOREIGN KEY (FAV_MACHINE) REFERENCES FITNESSMACHINES(ID),
        FOREIGN KEY (LAST_AWARD) REFERENCES FITNESSAWARDS(ID),
        FOREIGN KEY (NUT_PROGRAM) REFERENCES NUTRITIONPROGRAMS(ID)
        )"""
        cursor.execute(query)
        
        query = """CREATE TABLE WOMENSFITNESS
        (
        ID   INT              NOT NULL,
        NAME VARCHAR (30)     NOT NULL,
        AGE  INT,
        HEIGHT INT,
        WEIGHT INT,
        FAV_MACHINE INT,
        LAST_AWARD INT,
        NUT_PROGRAM INT,
        PRIMARY KEY (ID),
        FOREIGN KEY (FAV_MACHINE) REFERENCES FITNESSMACHINES(ID),
        FOREIGN KEY (LAST_AWARD) REFERENCES FITNESSAWARDS(ID),
        FOREIGN KEY (NUT_PROGRAM) REFERENCES NUTRITIONPROGRAMS(ID)
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
        
        query = """INSERT INTO NUTRITIONPROGRAMS (ID, NAME, CALORIES)
        VALUES(201, 'EGG PROGRAM', 2400)"""
        cursor.execute(query)
        
        query = """INSERT INTO NUTRITIONPROGRAMS (ID, NAME, CALORIES)
        VALUES(202, 'CEREALS PROGRAM', 1500)"""
        cursor.execute(query)
        
        query = """INSERT INTO FITNESSMACHINES (ID, NAME, WORKING_MUSCLES)
        VALUES(301, 'BARFIKS MACHINE', 'SHOULDERS')"""
        cursor.execute(query)
        
        query = """INSERT INTO FITNESSMACHINES (ID, NAME, WORKING_MUSCLES)
        VALUES(302, 'ROWING MACHINE', 'BACK')"""
        cursor.execute(query)
        
        query = """INSERT INTO FITNESSAWARDS (ID, BRANCH)
        VALUES(901, 'SWIMMING')"""
        cursor.execute(query)
        
        query = """INSERT INTO FITNESSAWARDS (ID, BRANCH)
        VALUES(902, 'RUNNING')"""
        cursor.execute(query)
        
        query = """INSERT INTO MENSFITNESS (ID, NAME, AGE, FAV_MACHINE, LAST_AWARD, NUT_PROGRAM)
        VALUES(001, 'GEORGE ARNOLD', 22, 301, 901, 201)"""
        cursor.execute(query)
        
        query = """INSERT INTO WOMENSFITNESS (ID, NAME, AGE, FAV_MACHINE, LAST_AWARD, NUT_PROGRAM)
        VALUES(101, 'VICTORIA SCHARZKOPF', 19, 302, 902, 202)"""
        cursor.execute(query)
        
        query = """INSERT INTO DIETT (DID, DNAME, DAGE, DIETFROM, DIETSTART)
        VALUES(3000, 'OBAMA', 52,'FISH', '52 MAR' )"""
        cursor.execute(query)
        
        query = """INSERT INTO DIETT (DID, DNAME, DAGE,DIETFROM, DIETSTART)
        VALUES(4000, 'MICHEL JAKSON', 38, 'COW MEAT','82 APR' )"""
        cursor.execute(query)
        
        query = """INSERT INTO DIETT (DID, DNAME, DAGE, DIETFROM,DIETSTART)
        VALUES(1000, 'GEORGE ARNOLD', 22, 'MILK','2 FEB' )"""
        cursor.execute(query)
        
        query = """INSERT INTO DIETT (DID, DNAME, DAGE,DIETFROM, DIETSTART)
        VALUES(2000, 'GEORGE CLONI', 32, 'SUGAR','2 FEB' )"""
        cursor.execute(query)
        
        query = """SELECT * FROM DIETT"""
        cursor.execute(query)
      
        query = """SELECT * FROM FITNESSTYPES"""
        cursor.execute(query)
        
        connection.commit()
        
        print("Database Created")
        
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