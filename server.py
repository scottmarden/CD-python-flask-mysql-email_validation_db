from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import MySQLConnector
import re

app = Flask(__name__)
app.secret_key = "LSDKnG:klnakdnKSNDGkjNDSg124"
mysql = MySQLConnector(app, 'email_validation_db')

@app.route('/')
def index():
	if 'error' not in session:
		session['error'] = 0
	print session['error']
	return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
	email_check = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
	email = request.form['email']
	if len(email) < 4:
		print "Email too short"
		flash("Please enter a valid email")
		return redirect('/')
	elif not email_check.match(email):
		print "Email not valid"
		flash("Please enter a valid email")
		return redirect('/')
	else:
		query = "INSERT INTO emails(email, created_at, updated_at) VALUES (:email, NOW(), NOW())"
		data = {
			'email': request.form['email']
		}
		confirmation = "This is your email: {}".format(email)
		mysql.query_db(query, data)
		return redirect('/success')

@app.route('/success')
def success():
	query1="SELECT * FROM emails ORDER BY id DESC LIMIT 1"
	confirmation = mysql.query_db(query1)
	query2 = "SELECT * FROM emails"
	emails = mysql.query_db(query2)
	print emails
	return render_template('success.html', confirmation=confirmation[0]['email'], emails=emails)

@app.route('/delete', methods=['POST'])
def delete():
	email_id = request.form['id']
	print email_id
	query = "DELETE FROM emails WHERE id = :id"
	data = {
		'id': request.form['id']
	}
	mysql.query_db(query, data)
	return redirect('/success')


app.run(debug=True)
