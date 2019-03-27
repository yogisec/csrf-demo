from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_wtf.csrf import CSRFProtect
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
engine = create_engine('sqlite:///app.db', echo=True)
 
app = Flask(__name__)
csrf = CSRFProtect(app)


 
@app.route('/')
def home():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return redirect ('/admin')

@app.route('/admin')
def admin():
	if not session.get('logged_in'):
		return redirect ('/')
	else:
		return render_template('admin.html')

@app.route('/logout')
def logout():
	session['logged_in'] = False
	return home()
 
@app.route('/login', methods=['POST'])
def do_admin_login():
 
	POST_USERNAME = str(request.form['username'])
	POST_PASSWORD = str(request.form['password'])
 
	Session = sessionmaker(bind=engine)
	s = Session()
	query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
	result = query.first()
	if result:
		session['logged_in'] = True
	else:
		flash('wrong password!')
	return home() 

@app.route('/adduser')
def adduser():
	return render_template('adduser.html')

@app.route('/makeuser', methods=['POST', 'GET'])
def makeuser():
	if request.method == 'POST':
		POST_USERNAME = str(request.form['username'])
		POST_PASSWORD = str(request.form['password'])
	if request.method == 'GET':
		POST_USERNAME = request.args.get('username')
		POST_PASSWORD = request.args.get('password')
	
	print(POST_USERNAME + ' - ' + POST_PASSWORD)
	Session = sessionmaker(bind=engine)
	session = Session()
	user = User(POST_USERNAME, POST_PASSWORD)
	session.add(user)
	session.commit()

	return home()

if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(debug=True,host='0.0.0.0', port=80)
