from flask import Flask, jsonify
import pymongo
from pymongo import MongoClient
import os

app = Flask(__name__)


def get_db(dbhost,dbport,dbuser,dbpass):
    client = MongoClient(host= dbhost,
                         port= dbport, 
                         username= dbuser, 
                         password= dbpass,
                        authSource="admin")
    db = client["animal_db"]
    return db

@app.route('/')
def ping_server():
    return "Welcome to the world of animals."

@app.route('/animals')
def get_stored_animals():
    db=""
    dbhost = os.environ["dbhost"]
    dbport = os.environ["dbport"]
    dbuser = os.environ["dbuser"]
    dbpass = os.environ["dbpass"]
    print(f"db connection details are {dbhost} - {int(dbport)} - {dbuser} - {dbpass}")
    try:
        db = get_db(dbhost,int(dbport),dbuser,dbpass)
        _animals = db.animal_tb.find()
        animals = [{"id": animal["id"], "name": animal["name"], "type": animal["type"]} for animal in _animals]
        return jsonify({"animals": animals})
    except:
        print("Not able to connect to database")
        pass
    finally:
        if type(db)==MongoClient:
            db.close()

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)
