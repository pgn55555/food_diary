from flask import Flask, render_template, send_file, request, redirect

import os
from configparser import ConfigParser

from sources.database_api import DataBase

config = ConfigParser()
config.read('config.ini')
app = Flask(__name__)
app.secret_key = config['FLASK']['key']

db_path = f"postgresql+psycopg2://{config['DATABASE']['POSTGRES_USER']}:\
{config['DATABASE']['POSTGRES_PASSWORD']}@{config['DATABASE']['HOST']}:\
{config['DATABASE']['PORT']}/{config['DATABASE']['POSTGRES_DB']}"
db = DataBase(db_path)

def delete_files() -> None:
    for filename in os.listdir("files"):
        file_path = os.path.join("files", filename)
        os.remove(file_path)

@app.route("/")
def add():
    return render_template('add.html')

@app.route('/submit_new', methods=['POST'])
def submit_new():
    values = {
        'name': request.form['name'],
        'calories': request.form['calories'],
        'proteins': request.form['proteins'],
        'fats': request.form['fats'],
        'carbohydrates': request.form['carbohydrates']
    }
    db.add_dish(values)
    return redirect('/')

@app.route("/choose")
def choose():
     return render_template('choose.html',
                            dishes=db.get_all_dishes())

@app.route('/submit_old', methods=['POST'])
def submit_old():
    name = request.form['name']
    row = db.get_dishes(name)
    values = {
        'name': name,
        'calories': row.first().calories,
        'proteins': row.first().proteins,
        'fats': row.first().fats,
        'carbohydrates': row.first().carbohydrates
    }
    db.add_dish(values)
    return redirect('/')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        name = request.form['name']
        results = db.get_dishes(name)
        return render_template('search_results.html', 
                               results=results, 
                               dish=results[0].name)
    return render_template('search.html')

@app.route('/update', methods=['POST'])
def update():
    updated_values = {
        'name': request.form['name'],
        'calories': request.form['calories'],
        'proteins': request.form['proteins'],
        'fats': request.form['fats'],
        'carbohydrates': request.form['carbohydrates']
    }
    db.edit_dish(updated_values)
    return redirect('/')

@app.route("/analytics")
def analytics():
    return render_template('analytics.html')

"""
@app.route('/submit_encrypt', methods=['POST'])
def submit_encrypt():
    uploaded_file = request.files['fileInput']
    file_path = os.path.join("files", uploaded_file.filename)
    uploaded_file.save(file_path)

    algo = request.form['selectAlgo']
    key = request.form['keyAlgo']
    if key == "":
        key = "generate"

    program = Main([file_path, algo, 'encrypt', key])
    program.start()
    
    return send_file(file_path, as_attachment=True)

@app.route('/submit_decrypt', methods=['POST'])
def submit_decrypt():
    uploaded_file = request.files['fileInput']
    file_path = os.path.join("files", uploaded_file.filename)
    uploaded_file.save(file_path)

    algo = request.form['selectAlgo']
    key = request.form['keyAlgo']

    program = Main([file_path, algo, 'decrypt', key])
    program.start()

    return send_file(file_path, as_attachment=True)

@app.route('/submit_hackermode', methods=['POST'])
def submit_hackermode():
    uploaded_file = request.files['fileInput']
    file_path = os.path.join("files", uploaded_file.filename)
    uploaded_file.save(file_path)

    program = Main([file_path, 'caesar', 'decrypt', 'hackermode'])
    program.start()
    
    return send_file(file_path, as_attachment=True)"""