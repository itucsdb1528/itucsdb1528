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
        
    elif 'delete_id' in request.form:
        delete_id = request.form['deleted_id']
        
        delete_menfitness(delete_id)
        
        menfitnesses = get_menfitness()
        
    elif 'menfitness_find' in request.form:
        ido = request.form['FIND_ID']
        name = request.form['FIND_NAME']
        age = request.form['FIND_AGE']
        height = request.form['FIND_HEIGHT']
        weight = request.form['FIND_WEIGHT']
        favmachine = request.form['FIND_FAV_MACHINE']
        award = request.form['FIND_LAST_AWARD']
        program = request.form['FIND_NUT_PROGRAM']
        
        menfitnesses = find_menfitness(ido, name, age, height, weight, favmachine, award, program)
        
    elif 'menfitness_find_all' in request.form:
        menfitnesses = get_menfitness()
        
    print(menfitnesses)
    return render_template('mensfitness.html', menfitnesser = menfitnesses) 

@app.route('/mensfitnesswithprogram', methods=['GET', 'POST']) 
def mensfitnesswithprogram_page():    
    
    if request.method == 'GET':
        print("Step 1")
        menfitnesswithprogram = get_menfitnesswithprogram()
        
    print(menfitnesswithprogram)
    return render_template('menjoinnutprogram.html', menfitnesswthprg = menfitnesswithprogram) 

def get_menfitnesswithprogram():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        query = """SELECT MEN_NAME, AGE, WEIGHT, HEIGHT, CALORIES FROM MENSFITNESS INNER JOIN NUTRITIONPROGRAMS
        ON MENSFITNESS.NUT_PROGRAM = NUTRITIONPROGRAMS.ID"""
        cursor.execute(query)
        
        menfitnesswithprogram = cursor.fetchall()
        
        connection.commit()
        
        return menfitnesswithprogram
    
@app.route('/join', methods=['GET', 'POST']) 
def jointables_page():    
    
    if request.method == 'GET':
        join = get_join()
        
    print(join)
    return render_template('jointable.html', joina = join) 

def get_join():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        
        query = """SELECT RCID ,WNAME, RKG FROM FITNESSRECORDS FULL OUTER JOIN FAMFITNESSERS
                ON FITNESSRECORDS.RCID = FAMFITNESSERS.RECORDNO  """
        cursor.execute(query)
        
        join = cursor.fetchall()
        
        connection.commit()
        
        return join
    

@app.route('/womensfitness', methods=['GET', 'POST']) 
def womensfitness_page():  
        
    if request.method == 'GET':
        womenfitnesses = get_womenfitness()
        
    elif 'womenfitness_add' in request.form:
        ido = request.form['ID']
        name = request.form['NAME']
        age = request.form['AGE']
        height = request.form['HEIGHT']
        weight = request.form['WEIGHT']
        favmachine = request.form['FAV_MACHINE']
        award = request.form['LAST_AWARD']
        program = request.form['NUT_PROGRAM']

        add_womenfitness(ido, name, age, height, weight, favmachine, award, program)
        
        womenfitnesses = get_womenfitness()
        
    elif 'delete_id' in request.form:
        delete_id = request.form['deleted_id']
        
        delete_womenfitness(delete_id)
        
        womenfitnesses = get_womenfitness()
        
    elif 'womenfitness_find' in request.form:
        ido = request.form['FIND_ID']
        name = request.form['FIND_NAME']
        age = request.form['FIND_AGE']
        height = request.form['FIND_HEIGHT']
        weight = request.form['FIND_WEIGHT']
        favmachine = request.form['FIND_FAV_MACHINE']
        award = request.form['FIND_LAST_AWARD']
        program = request.form['FIND_NUT_PROGRAM']
        
        womenfitnesses = find_womenfitness(ido, name, age, height, weight, favmachine, award, program)
        
    elif 'womenfitness_find_all' in request.form:
        womenfitnesses = get_womenfitness()
        
    print(womenfitnesses)
    return render_template('womensfitness.html', womenfitnesser = womenfitnesses) 

@app.route('/nutritionprograms', methods=['GET', 'POST']) 
def nutritionprograms_page():
    
    if request.method == 'GET':
        nutritionprogram = get_nutritionprogram()

    elif 'nutritionprograms_add' in request.form:
        ido = request.form['ID']
        name = request.form['NAME']
        calories = request.form['CALORIES']

        add_nutritionprogram(ido, name, calories)
        
        nutritionprogram = get_nutritionprogram()
        
    elif 'delete_id' in request.form:
        delete_id = request.form['deleted_id']
        
        delete_nutritionprogram(delete_id)
        
        nutritionprogram = get_nutritionprogram()
        
    elif 'nutritionprogram_find' in request.form:
        ido = request.form['FIND_ID']
        name = request.form['FIND_NAME']
        calory = request.form['FIND_CALORIES']
        
        nutritionprogram = find_nutritionprogram(ido, name, calory)
        
    elif 'nutritionprogram_find_all' in request.form:
        nutritionprogram = get_nutritionprogram()
            
    return render_template('nutritionprograms.html', nutritionprograms = nutritionprogram) 

@app.route('/fitnessmachines', methods=['GET', 'POST']) 
def fitnessmachines_page():
    
    if request.method == 'GET':
        fitnessmachine = get_fitnessmachine()  

    elif 'fitnessmachines_add' in request.form:
        ido = request.form['ID']
        name = request.form['NAME']
        working_muscles = request.form['WORKING_MUSCLES']

        add_fitnessmachine(ido, name, working_muscles)
        
        fitnessmachine = get_fitnessmachine()  
        
    elif 'delete_id' in request.form:
        delete_id = request.form['deleted_id']
        
        delete_fitnessmachine(delete_id)
        
        fitnessmachine = get_fitnessmachine()  
        
    elif 'fitnessmachines_find' in request.form:
        ido = request.form['FIND_ID']
        name = request.form['FIND_NAME']
        working_muscles = request.form['FIND_WORKING_MUSCLES']
        
        fitnessmachine = find_fitnessmachine(ido, name, working_muscles)
        
    elif 'fitnessmachines_find_all' in request.form:
        fitnessmachine = get_fitnessmachine()
          
    return render_template('fitnessmachines.html', fitnessmachines = fitnessmachine) 

@app.route('/fitnessawards', methods=['GET', 'POST']) 
def fitnessawards_page():
    
    if request.method == 'GET':
        fitnessaward = get_fitnessaward()
    
    elif 'fitnessawards_add' in request.form:
        ido = request.form['ID']
        branch = request.form['BRANCH']

        add_fitnessaward(ido, branch) 
        
        fitnessaward = get_fitnessaward()
        
    elif 'delete_id' in request.form:
        delete_id = request.form['deleted_id']
        
        delete_fitnessaward(delete_id)
        
        fitnessaward = get_fitnessaward()
        
    elif 'fitnessaward_find' in request.form:
        ido = request.form['FIND_ID']
        branch = request.form['FIND_BRANCH']
        
        fitnessaward = find_fitnessaward(ido, branch)
        
    elif 'fitnessaward_find_all' in request.form:
        fitnessaward = get_fitnessaward()
    
        
    return render_template('fitnessawards.html', fitnessawards = fitnessaward) 

def add_menfitness(ido, name, age, height, weight, favmachine, award, program):
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        cursor.execute("""INSERT INTO MENSFITNESS (ID, MEN_NAME, AGE, HEIGHT, WEIGHT, FAV_MACHINE, LAST_AWARD, NUT_PROGRAM)
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
    
def delete_menfitness(ido):
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        query = """DELETE FROM MENSFITNESS WHERE ID={}""".format(ido)
        cursor.execute(query)
        
        connection.commit()
        
        return True
    
def find_menfitness(ido, name, age, height, weight, favmachine, award, program):
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        query = """SELECT * FROM MENSFITNESS WHERE ( CAST(ID AS TEXT) LIKE '{}%') AND (MEN_NAME LIKE  '{}%' ) AND ( CAST(AGE AS TEXT) LIKE '{}%') AND ( CAST(HEIGHT AS TEXT) LIKE '{}%') AND ( CAST(WEIGHT AS TEXT) LIKE '{}%') AND ( CAST(FAV_MACHINE AS TEXT) LIKE '{}%') AND ( CAST(LAST_AWARD AS TEXT) LIKE '{}%') AND ( CAST(NUT_PROGRAM AS TEXT) LIKE '{}%')""".format(ido, name, age, height, weight, favmachine, award, program)
        cursor.execute(query)
        mensfitness = cursor.fetchall()
        
        connection.commit()
        
        return mensfitness
    
def add_womenfitness(ido, name, age, height, weight, favmachine, award, program):
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        cursor.execute("""INSERT INTO WOMENSFITNESS (ID, NAME, AGE, HEIGHT, WEIGHT, FAV_MACHINE, LAST_AWARD, NUT_PROGRAM)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s)""", (ido, name, age, height, weight, favmachine, award, program))

        connection.commit()

        return True
    
def get_womenfitness():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM WOMENSFITNESS")
        womenfitness = cursor.fetchall()
        
        connection.commit()
        
        return womenfitness
    
def delete_womenfitness(ido):
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        query = """DELETE FROM WOMENSFITNESS WHERE ID={}""".format(ido)
        cursor.execute(query)
        
        connection.commit()
        
        return True
    
def find_womenfitness(ido, name, age, height, weight, favmachine, award, program):
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        query = """SELECT * FROM WOMENSFITNESS WHERE ( CAST(ID AS TEXT) LIKE '{}%') AND (NAME LIKE  '{}%' ) AND ( CAST(AGE AS TEXT) LIKE '{}%') AND ( CAST(HEIGHT AS TEXT) LIKE '{}%') AND ( CAST(WEIGHT AS TEXT) LIKE '{}%') AND ( CAST(FAV_MACHINE AS TEXT) LIKE '{}%') AND ( CAST(LAST_AWARD AS TEXT) LIKE '{}%') AND ( CAST(NUT_PROGRAM AS TEXT) LIKE '{}%')""".format(ido, name, age, height, weight, favmachine, award, program)
        cursor.execute(query)
        womensfitness = cursor.fetchall()
        
        connection.commit()
        
        return womensfitness
    
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
        nutritionprogram = cursor.fetchall()
        
        connection.commit()
        
        return nutritionprogram
    
def delete_nutritionprogram(ido):
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        query = """DELETE FROM NUTRITIONPROGRAMS WHERE ID={}""".format(ido)
        cursor.execute(query)
        
        connection.commit()
        
        return True
    
def find_nutritionprogram(ido, name, calories):
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        query = """SELECT * FROM NUTRITIONPROGRAMS WHERE ( CAST(ID AS TEXT) LIKE '{}%') AND (NAME LIKE  '{}%' ) AND ( CAST(CALORIES AS TEXT) LIKE '{}%')""".format(ido, name, calories)
        cursor.execute(query)
        nutritionprogram = cursor.fetchall()
        
        connection.commit()
        
        return nutritionprogram
    
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
    
def delete_fitnessmachine(ido):
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        query = """DELETE FROM FITNESSMACHINES WHERE ID={}""".format(ido)
        cursor.execute(query)
        
        connection.commit()
        
        return True
    
def find_fitnessmachine(ido, name, working_muscles):
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        query = """SELECT * FROM FITNESSMACHINES WHERE ( CAST(ID AS TEXT) LIKE '{}%') AND (NAME LIKE  '{}%' ) AND ( WORKING_MUSCLES LIKE '{}%')""".format(ido, name, working_muscles)
        cursor.execute(query)
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
    
def delete_fitnessaward(ido):
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        query = """DELETE FROM FITNESSAWARDS WHERE ID={}""".format(ido)
        cursor.execute(query)
        
        connection.commit()
        
        return True
    
def find_fitnessaward(ido, branch):
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        query = """SELECT * FROM FITNESSAWARDS WHERE ( CAST(ID AS TEXT) LIKE '{}%') AND (BRANCH LIKE  '{}%' )""".format(ido, branch)
        cursor.execute(query)
        fitnessaward = cursor.fetchall()
        
        connection.commit()
        
        return fitnessaward



@app.route('/ftypes', methods=['GET', 'POST']) 
def ftypes_page():    
    
    if request.method == 'GET':
        ftypes = get_ftypes()  
        
    elif 'ftypes_add' in request.form:
        ido = request.form['FTID']
        diet = request.form['RECOMMENDED_DIET']
        name = request.form['FTNAME']
        age = request.form['FTAGE']
        fees = request.form['FTFEES']
        
        add_ftypes(ido, diet,name, age, fees)
        ftypes = get_ftypes()
    elif 'delete_id' in request.form:
        delete_id = request.form['deleted_id']
        
        delete_fdiet(delete_id)
        
        ftypes = get_ftypes()
        
    elif 'ftypes_find' in request.form:
        ido = request.form['FTID']
        diet = request.form['RECOMMENDED_DIET']
        name = request.form['FTNAME']
        age = request.form['FTAGE']
        fees = request.form['FTFEES']
        
        ftypes = find_ftypes(ido, diet,name, age, fees)
        
    elif 'ftypes_find_all' in request.form:
        ftypes = get_ftypes()
    
    return render_template('ftypes.html', ftypeser = ftypes) 
    

def add_ftypes(ido, diet,name, age, fees):
     
    with dbapi2.connect(app.config['dsn']) as connection:
         cursor = connection.cursor()
         
         cursor.execute("""INSERT INTO FITNESSTYPES (FTID, RECOMMENDED_DIET, FTNAME, FTAGE, FTFEES)
         VALUES(%s, %s, %s, %s, %s)""", (ido, diet,name, age, fees))
         
         connection.commit()
         
         return True
     
def get_ftypes():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM FITNESSTYPES")
        ftypes = cursor.fetchall()
        
        connection.commit()
        
        return ftypes
    
def delete_ftypes(ido):
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        query = """DELETE FROM FITNESSTYPES WHERE FTID={}""".format(ido)
        cursor.execute(query)
        
        connection.commit()
        
        return True
    
def find_ftypes(ido, diet,name, age, fees):
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        query = """SELECT * FROM FITNESSTYPES WHERE ( CAST(FTID AS TEXT) LIKE '{}%') AND (RECOMMENDED_DIET LIKE  '{}%' ) AND ( CAST(FTNAME AS TEXT) LIKE '{}%') AND ( CAST(FTAGE AS TEXT) LIKE '{}%') AND ( CAST(FTFEES AS TEXT) LIKE'{}%')""".format(ido, diet,name, age, fees)
        cursor.execute(query)
        ftypes = cursor.fetchall()
        
        connection.commit()
        
        return ftypes

@app.route('/frecords', methods=['GET', 'POST']) 
def frecords_page():    
    if request.method == 'GET':
        frecords = get_frecords()
        
    
    elif 'frecords_add' in request.form:
        ido = request.form['RCID']
        name = request.form['WNAME']
        kg = request.form['RKG']
        
        add_frecords(ido, name, kg)
        frecords = get_frecords()
        
    elif 'delete_id' in request.form:
        delete_id = request.form['deleted_id']
        
        delete_frecords(delete_id)
        
    frecords = get_frecords()
        
    print(frecords)
    return render_template('frecords.html', frecordser = frecords) 
    

def add_frecords(ido, name, kg):
     with dbapi2.connect(app.config['dsn']) as connection:
         cursor = connection.cursor()
         
         cursor.execute("""INSERT INTO FITNESSRECORDS (RCID, WNAME, RKG)
         VALUES(%s, %s, %s)""", (ido, name, kg))
         
         connection.commit()
         
         return True
     
def get_frecords():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM FITNESSRECORDS")
        frecords = cursor.fetchall()
        
        connection.commit()
        
        return frecords
    
def delete_frecords(ido):
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        query = """DELETE FROM FITNESSRECORDS WHERE RCID={}""".format(ido)
        cursor.execute(query)
        
        connection.commit()
        
        return True

@app.route('/fdiet', methods=['GET', 'POST']) 
def fdiet_page():    
    if request.method == 'GET':
        fdiet = get_fdiet()
        
    elif 'fdiet_add' in request.form:
        ido = request.form['DID']
        name = request.form['DNAME']
        age = request.form['DAGE']
        dfrom = request.form['DIETFROM']
        dstart = request.form['DIETSTART']

        add_fdiet(ido, name, age, dfrom, dstart)
        fdiet = get_fdiet()
    elif 'delete_id' in request.form:
        delete_id = request.form['deleted_id']
        
        delete_fdiet(delete_id)
        
        fdiet = get_fdiet()
    print(fdiet)
    return render_template('fdiet.html', fdieter = fdiet) 
    

def add_fdiet(ido, name, age, dfrom, dstart):
     with dbapi2.connect(app.config['dsn']) as connection:
         cursor = connection.cursor()
         
         cursor.execute("""INSERT INTO DIETT (DID, DNAME, DAGE, DIETFROM, DIETSTART)
         VALUES(%s, %s, %s, %s, %s)""", (ido, name, age, dfrom, dstart))
         
         connection.commit()
         
         return True
     
def get_fdiet():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM DIETT GROUP BY DIETFROM")
        fdiet = cursor.fetchall()
        
        connection.commit()
        
        return fdiet
    
def delete_fdiet(ido):
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        query = """DELETE FROM DIETT WHERE DID={}""".format(ido)
        cursor.execute(query)
        
        connection.commit()
        
        return True


@app.route('/muinf', methods=['GET', 'POST']) 
def muinf_page():    
    if request.method == 'GET':
        muinf = get_muinf()
        
    elif 'muinf_add' in request.form:
        ido = request.form['MDID']
        name = request.form['MDNAME']
    
        add_muinf(ido, name)
        muinf = get_muinf()
    elif 'delete_id' in request.form:
        delete_id = request.form['deleted_id']
        
        delete_muinf(delete_id)
        
        muinf = get_muinf()
    print(muinf)
    return render_template('muinf.html', muinfer = muinf) 
    

def add_muinf(ido, name):
     with dbapi2.connect(app.config['dsn']) as connection:
         cursor = connection.cursor()
         
         cursor.execute("""INSERT INTO FITNESSMD (MDID, MDNAME)
         VALUES(%s, %s)""", (ido, name))
         
         connection.commit()
         
         return True
     
def get_muinf():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM FITNESSMD ORDER BY MDNAME")
        muinf = cursor.fetchall()
        
        connection.commit()
        
        return muinf
    
def delete_muinf(ido):
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        query = """DELETE FROM FITNESSMD WHERE MDID={}""".format(ido)
        cursor.execute(query)
        
        connection.commit()
        
        return True

@app.route('/ffitnessers', methods=['GET', 'POST']) 
def ffitnessers_page():    
    if request.method == 'GET':
        ffitnessers = get_ffitnessers()
        
    elif 'ffitnessers_add' in request.form:
        ido = request.form['FAMID']
        name = request.form['FNAME']
        rno = request.form['RECORDNO']
       
        add_ffitnessers(ido, name, rno)
        ffitnessers = get_ffitnessers()
        
    elif 'delete_id' in request.form:
        delete_id = request.form['deleted_id']
        
        delete_ffitnessers(delete_id)
        
    ffitnessers = get_ffitnessers()
    print(ffitnessers)
    return render_template('ffitnessers.html', ffitnesserser = ffitnessers) 
    
        
def add_ffitnessers(ido, name, rno):
     with dbapi2.connect(app.config['dsn']) as connection:
         cursor = connection.cursor()
         
         cursor.execute("""INSERT INTO FAMFITNESSERS (FAMID, FNAME, RECORDNO)
         VALUES(%s, %s, %s)""", (ido, name, rno))
         
         connection.commit()
         
         return True
     
def get_ffitnessers():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM FAMFITNESSERS")
        ffitnessers = cursor.fetchall()
        
        connection.commit()
        
        return ffitnessers
    
def delete_ffitnessers(ido):
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        query = """DELETE FROM FAMFITNESSERS WHERE FAMID={}""".format(ido)
        cursor.execute(query)
        
        connection.commit()
        
        return True


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
        
        query = """DROP TABLE IF EXISTS FAMFITNESSERS CASCADE"""
        cursor.execute(query)
        
        query = """DROP TABLE IF EXISTS FITNESSMD CASCADE"""
        cursor.execute(query)
        
        query = """DROP TABLE IF EXISTS FITNESSRECORDS CASCADE"""
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
        NAME VARCHAR (30)     ,
        WORKING_MUSCLES VARCHAR(50),
        PRIMARY KEY(ID)
        )"""
        cursor.execute(query)
        
        query = """CREATE TABLE FITNESSAWARDS
        (
        ID   INT              NOT NULL,
        BRANCH VARCHAR(50)    ,
        PRIMARY KEY(ID)
        )"""
        cursor.execute(query)
        
        query = """CREATE TABLE MENSFITNESS
        (
        ID   INT              NOT NULL,
        MEN_NAME VARCHAR (30)     NOT NULL,
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
        FTID   INT              NOT NULL,
        RECOMMENDED_DIET INT,
        FTNAME VARCHAR (30),
        FTAGE  INT,
        FTFEES   DECIMAL (18, 2),
        PRIMARY KEY (FTID),       
        FOREIGN KEY (RECOMMENDED_DIET) REFERENCES DIETT (DID)
        )"""
        cursor.execute(query)
        
        
        
        query = """CREATE TABLE FITNESSRECORDS
        (
        RCID   INT              NOT NULL,
        WNAME VARCHAR (30)     ,
        RKG VARCHAR (50)  ,
        PRIMARY KEY (RCID)
        )"""
        cursor.execute(query)
        
        query = """CREATE TABLE FITNESSMD
        (
        MDID   INT              NOT NULL,
        MDNAME VARCHAR (30)    ,
        PRIMARY KEY (MDID)
        )"""
        cursor.execute(query)
        
        query = """CREATE TABLE FAMFITNESSERS
        (
        FAMID   INT              NOT NULL,
        FNAME VARCHAR (30)   ,
        RECORDNO INT,
        PRIMARY KEY (FAMID), 
        FOREIGN KEY (RECORDNO) REFERENCES FITNESSRECORDS(RCID)
        )"""
        cursor.execute(query)
        
        query="""INSERT INTO FITNESSRECORDS (RCID, WNAME, RKG)
        VALUES(20, 'EGG PROGRAM', 2400)"""
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
        
        query = """INSERT INTO MENSFITNESS (ID, MEN_NAME, AGE, WEIGHT, HEIGHT, FAV_MACHINE, LAST_AWARD, NUT_PROGRAM)
        VALUES(001, 'GEORGE ARNOLD', 75, 180, 22, 301, 901, 201)"""
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