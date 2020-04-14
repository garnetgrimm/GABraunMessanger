from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import time

#the below 3 lines simply causes only errors and print statements to be logged to console
#otherwise every freakin request will be logged
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__, static_url_path = "", static_folder = "static")
#dialect+driver://username:password@host:port/database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Chimneyswift@localhost/postgres'
	
#all the line below does is stop a warning message from comming up	
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Log(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	machine = db.Column(db.String)
	tempature = db.Column(db.Integer)
	water_level = db.Column(db.Integer)
	step_number = db.Column(db.Integer)
	extra_change_info = db.Column(db.String)
	date_time = db.Column(db.String)
	def __init__(self, machine, tempature, water_level, step_number, extra_change_info):
		self.machine = machine
		self.tempature = tempature
		self.water_level = water_level
		self.step_number = step_number
		self.extra_change_info = extra_change_info
		date_time = time.strftime("%H:%M:%S_%m/%d/%Y")
	def __repr__(self):
		return str(self.id)

class Machine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    tempature = db.Column(db.Integer)
    water_level = db.Column(db.Integer)
    step_number = db.Column(db.Integer)
    weight = db.Column(db.Integer)
	
    def __init__(self, name, tempature, water_level, step_number, weight):
        self.name = name
        self.tempature = tempature
        self.water_level = water_level
        self.step_number = step_number
        self.weight = weight
    def __repr__(self):
        return str(self.id)
		
def log_change(machine_name, tempature, water_level, step_number, changeInfo):
	current_log = Log(machine_name, tempature, water_level, step_number, changeInfo)
	db.session.add(current_log)
	db.session.commit()

def change_machine(machine_id, temp_inc, water_inc, step_inc):
	current_machine = Machine.query.filter_by(id=machine_id).first()
	current_machine.tempature = temp_inc
	current_machine.water_level = water_inc
	current_machine.step_number = step_inc
	
	#this has will log every change to the database
	#log_change(current_machine.name, temp_inc, water_inc, step_inc, "")
	
	db.session.commit()
	
@app.route('/')
def index():
	machine_ids = Machine.query.all()
	machine_names = []
	
	for i in (0, len(machine_ids) - 1):
		machine_names.append(Machine.query.filter_by(id=str(machine_ids[i - 1])).first().name)
	
	return render_template('index_complex.html', machine_ids=machine_ids, machine_names=machine_names)
	
@app.route('/getMachineStats')
def machineStats():
	#machine_num = request.form['machine_num']
	id = request.args.get('id', 0, type=int)
	
	current_machine = Machine.query.filter_by(id=id).first()
	
	try:
		tempature=current_machine.tempature
		water_level=current_machine.water_level
		step_number=current_machine.step_number
		weight=current_machine.weight
	except:
		tempature="null"
		water_level="null"
		step_number="null"
		weight="null"
	return jsonify(tempature=tempature, water_level=water_level, step_number=step_number, weight=weight)